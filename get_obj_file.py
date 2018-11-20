from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os
import sys
from tqdm import tqdm
# Create renderer
import numpy as np
import skimage.io as io

# Assign attributes to renderer
from smpl_webuser.serialization import load_model


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

        # theta = np.load('pose.npy')

        self.body.pose[:] = theta
        self.body.betas[:] = beta

        return self.body


def main(out_path):
    pose = np.load('pose_standing.npy')
    theta = np.concatenate((np.array([np.pi, 0, 0]), pose, np.zeros(10)))

    theta = theta.reshape(-1)

    render = Renderer(model_path='models/neutral.pkl')
    v = render.render(theta)

    with open('untitled.obj', mode='r') as f:
        lines = f.readlines()
        count = 0
        for i in range(len(lines)):
            if lines[i].startswith('v '):
                new_line = 'v {} {} {}\n'.format(float(v[count][0]), float(v[count][1]), float(v[count][2]))
                lines[i] = new_line
                count += 1

        with open(os.path.join(out_path, 'out.obj'), mode='w') as f:
            f.writelines(lines)


def write_mtl(uv_path, out_path):
    with open('untitled.mtl') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            if lines[i].startswith('map_Kd'):
                lines[i] = 'map_Kd {}'.format(uv_path)

    with open(os.path.join(out_path, 'untitled.mtl'), 'w') as f:
        f.writelines(lines)


if __name__ == '__main__':
    path = '1001/UV'
    for uv_path in tqdm(os.listdir(path)):
        uv_path = os.path.join(path, uv_path)
        out_path = uv_path.replace('UV', 'obj')[:-4]
        if not os.path.exists(out_path):
            os.mkdir(out_path)
        main(out_path)
        write_mtl(uv_path, out_path)
