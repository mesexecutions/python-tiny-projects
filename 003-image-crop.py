import os
import cv2
import numpy as np
from typing import Counter
from modules.custom_functions import get_black_color

'''
    AUHTOR: ramepetla (at) g m a i l . c o m
            R A M E S H  P E T L A
     Version: 0.1
     Python: 3.9.0
     USAGE: To Crop the Images to Desired Size. Adjust the Parameters for Variable "cropped_image"

'''
source_images = os.listdir('C:\images')
destination_path = 'C:\images-output'

for image in source_images:
    black_color_freq = get_black_color(image)
    read_image = cv2.imread(image)
    if black_color_freq < 10000:
        cropped_image = read_image[103:729, 0:1366]
    else:
        cropped_image = read_image[0:729, 0:1366]
    dest_filename = 'cropped_' + image
    cv2.imwrite(os.path.join(destination_path, dest_filename), cropped_image)
    cv2.waitKey(0)




