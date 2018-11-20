import os
import cv2
import numpy as np
from tqdm import tqdm
texture_path = '/home/wangjian02/tmp/textures'
textures = []
for root, dirs, filenames in os.walk(texture_path):
    for filename in tqdm(filenames):
        if filename.endswith('.jpg') and 'nongrey' in filename:
            texture = cv2.imread(os.path.join(root, filename))
            textures.append(texture)
mean_texture = np.mean(textures, axis=0).astype(np.uint8)
cv2.imshow('mean', mean_texture)
cv2.waitKey()
