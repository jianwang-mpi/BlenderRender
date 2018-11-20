"""
Demo of HMR.

Note that HMR requires the bounding box of the person in the image. The best performance is obtained when max length of the person in the image is roughly 150px.

When only the image path is supplied, it assumes that the image is centered on a person whose length is roughly 150px.
Alternatively, you can supply output of the openpose to figure out the bbox and the right scale factor.

Sample usage:

# On images on a tightly cropped image around the person
python -m demo --img_path data/im1963.jpg
python -m demo --img_path data/coco1.png

# On images, with openpose output
python -m demo --img_path data/random.jpg --json_path data/random_keypoints.json
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys

# Create renderer
import numpy as np
import skimage.io as io
import tensorflow as tf
from absl import flags

import src.config
# Assign attributes to renderer
from smpl_webuser.serialization import load_model
from src.RunModel import RunModel
from src.util import image as img_util
from src.util import openpose as op_util
from src.util import renderer as vis_util

flags.DEFINE_string('img_path',
                    '/home/wangjian02/Projects/BlenderRender/images/in/0110_c5s1_035226_01.jpg',
                    'Image to run')
flags.DEFINE_string(
    'json_path', None,
    'If specified, uses the openpose output to crop the image.')


class Renderer:
    def __init__(self, model_path):
        # Load SMPL model (here we load the female model)
        self.body = load_model(model_path)

        self.num_cam = 3
        self.num_theta = 72
        self.num_beta = 10

    def render(self, thetas):
        """
        get the rendered image and rendered silhouette
        :param thetas: model parameters, 3 * camera parameter + 72 * body pose + 10 * body shape
        :param texture_bgr: texture image in bgr format
        :return: the rendered image and deviation of rendered image to texture image
        (rendered image, deviation of rendered image, silhouette)
        """
        thetas = thetas.reshape(-1)
        cams = thetas[:self.num_cam]
        theta = thetas[self.num_cam: (self.num_cam + self.num_theta)]
        beta = thetas[(self.num_cam + self.num_theta):]

        # for A pose
        # theta = np.zeros(72)
        # theta[0] = np.pi
        # theta[53] = 1.2
        # theta[50] = -1.2

        # theta = np.load('pose.npy')

        self.body.pose[:] = theta
        self.body.betas[:] = beta

        return self.body



def preprocess_image(img_path, json_path=None):
    img = io.imread(img_path)
    if img.shape[2] == 4:
        img = img[:, :, :3]

    if json_path is None:
        if np.max(img.shape[:2]) != config.img_size:
            print('Resizing so the max image size is %d..' % config.img_size)
            scale = (float(config.img_size) / np.max(img.shape[:2]))
        else:
            scale = 1.
        center = np.round(np.array(img.shape[:2]) / 2).astype(int)
        # image center in (x,y)
        center = center[::-1]
    else:
        scale, center = op_util.get_bbox(json_path)

    crop, proc_param = img_util.scale_and_crop(img, scale, center,
                                               config.img_size)

    # Normalize image to [-1, 1]
    crop = 2 * ((crop / 255.) - 0.5)

    return crop, proc_param, img


def main(img_path, json_path=None):
    sess = tf.Session()
    model = RunModel(config, sess=sess)

    input_img, proc_param, img = preprocess_image(img_path, json_path)
    # Add batch dimension: 1 x D x D x 3
    input_img = np.expand_dims(input_img, 0)

    joints, verts, cams, joints3d, theta = model.predict(
        input_img, get_theta=True)

    theta = theta.reshape(-1)

    render = Renderer(model_path='models/neutral.pkl')
    v = render.render(theta)

    print(v.shape)

    with open('/home/wangjian02/untitled.obj', mode='r') as f:
        lines = f.readlines()
        count = 0
        for i in range(len(lines)):
            if lines[i].startswith('v '):
                new_line = 'v {} {} {}\n'.format(float(v[count][0]), float(v[count][1]), float(v[count][2]))
                lines[i] = new_line
                count += 1

        with open('/home/wangjian02/Projects/BlenderRender/models/out.obj', mode='w') as f:
            f.writelines(lines)
    print('finish obj!')

def write_mtl(img_path):
    uv_path = img_path.replace('in', 'out_uv_market1501')
    with open('/home/wangjian02/untitled.mtl') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            if lines[i].startswith('map_Kd'):
                lines[i] = 'map_Kd {}'.format(uv_path)

    with open('/home/wangjian02/Projects/BlenderRender/models/untitled.mtl', 'w') as f:
        f.writelines(lines)
    print('finish mtl!')


if __name__ == '__main__':
    config = flags.FLAGS
    config(sys.argv)
    # Using pre-trained model, change this to use your own.
    config.load_path = src.config.PRETRAINED_MODEL

    config.batch_size = 1

    main(config.img_path, config.json_path)

    write_mtl(config.img_path)
