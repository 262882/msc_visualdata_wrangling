#!/usr/bin/env python3
"""Select image to set ball sighted to false"""

import json
import os
import glob
import numpy as np
import cv2
from decode import decode, add_bb_frmcamsph

output_dir = "vis_false"
try:
    os.makedirs(output_dir)
except FileExistsError:
    pass

img_list = glob.glob(os.path.join('./',"*.json"))

for count, name in enumerate(img_list):
    print(count+1, "/", len(img_list), "Images processed")

    with open(name, 'r') as input_file:
        img_dict = json.load(input_file)

    output_img = decode(img_dict['img'], img_dict['h_img'], img_dict['w_img'])

    ball_vector = np.asarray(img_dict["ball_locate"])
    if img_dict["ball_sighted"]==1 and np.sum(np.abs(ball_vector)) != 0 :
        add_bb_frmcamsph(output_img, ball_vector, color = (0,0,255))

        # Display and sort
        cv2.imshow('Frame', output_img)
        des = print("s - Set not visible? q - Quit? - Otherwise any key)")
        key = cv2.waitKey()

        # Process file
        if key==ord('s'):
            print("Set not visible")
            img_dict["ball_sighted"]=0
            img_dict["ball_locate"]=[0, 0, 0]

            with open("./" + output_dir + "/" + name[2:], 'w') as out_file:
                json.dump(img_dict, out_file)

        if key==ord('q'):
            break

        else: 
            print("Pass")