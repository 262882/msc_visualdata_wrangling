#!/usr/bin/env python3
"""Seperate json dataset files into occluded, visible or discard sub sets"""

import json
import os
import glob
import numpy as np
import cv2
from decode import decode, add_bb_frmcamsph

output_dir1 = "occl_true"
try:
    os.makedirs(output_dir1)
except FileExistsError:
    pass

output_dir2 = "occl_false"
try:
    os.makedirs(output_dir2)
except FileExistsError:
    pass

output_dir3 = "discard"
try:
    os.makedirs(output_dir3)
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
        des = print("o - Occluded? d - Discard? q - Quit? - Otherwise any key)")
        key = cv2.waitKey()

        # Process file
        if key==ord('o'):
            print("Occluded")
            img_dict["occluded"]=True
            with open("./" + output_dir1 + "/" + name[2:], 'w') as out_file:
                json.dump(img_dict, out_file)

        elif key==ord('d'):
            print("Discarded")
            img_dict["occluded"]=False
            with open("./" + output_dir3 + "/" + name[2:], 'w') as out_file:
                json.dump(img_dict, out_file)

        elif key==ord('q'):
            break

        else: 
            print("Not occluded")
            img_dict["occluded"]=False
            with open("./" + output_dir2 + "/" + name[2:], 'w') as out_file:
                json.dump(img_dict, out_file)