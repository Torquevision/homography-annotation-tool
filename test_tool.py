import os
import numpy as np
import cv2
import argparse
import random
import math
import json

def update_view(p1, p2, img):
    img = cv2.circle(img, tuple(p1), 10, (255, 0, 0), 3)
    img = cv2.circle(img, tuple(p2), 10, (0, 0, 255), 3)
    img = cv2.line(img, tuple(p1), tuple(p2), (0, 255, 0), 3)
    
    return img

def display(global_points, image):
    img = image.copy()
    for i in range(0, len(global_points), 2):
        img = update_view(global_points[i], global_points[i+1], img)
    cv2.imshow('img', img)
    cv2.waitKey(0)

def main(args):
    rink_img = cv2.imread(args.rink_path)
    #args.data_path = os.path.abspath(args.data_path)
    if not os.path.exists(args.data_path):
        print(args.data_path, ' -- Path not exists')
    #cv2.imshow('rink', rink_img)
    json_path = os.path.join(args.data_path, 'output.json')
    data = json.load(open(json_path))
    for file in data:
        file_path = os.path.join(args.data_path, file)
        image = cv2.imread(file_path)
        blank = np.zeros(image.shape, np.uint8)
        blank[0:rink_img.shape[0], 0: rink_img.shape[1]] = rink_img
        vis = np.concatenate((image, blank), axis=1)
        display(data[file]['points'], vis)

    cv2.destroyAllWindows()

def parse_it():
    parser = argparse.ArgumentParser()

    parser.add_argument('-data_path', help='Path to dataset')
    parser.add_argument('-rink_path', default='rink.jpg', help='Rink image path')

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_it()
    main(args)