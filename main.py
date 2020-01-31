
import os
import numpy as np
import cv2
import argparse
import random
import math
import json

btn_down = False
global_points = []
global_item = None
image = None

def get_points():
    x,y = random.randint(50, 200), random.randint(50, 200)
    xx,yy = random.randint(250, 450), random.randint(250, 450)
    return [(x, y), (xx, yy)]

def euc_dist(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2  + (p1[1] - p2[1])**2)

def update_view(p1, p2, img):
    img = cv2.circle(img, tuple(p1), 10, (255, 0, 0), 3)
    img = cv2.circle(img, tuple(p2), 10, (0, 0, 255), 3)
    img = cv2.line(img, tuple(p1), tuple(p2), (0, 255, 0), 3)
    cv2.imshow('Image', img)

    return img

def mouse_handler(event, x, y, flags, data):
    global btn_down, global_item

    if event == cv2.EVENT_LBUTTONUP and btn_down:
        if global_item is not None:
            global_points[global_item] = (x, y)
        btn_down = False

    elif event == cv2.EVENT_MOUSEMOVE and btn_down:
        global_points[global_item] = (x, y)
        update_all_view(global_points)


    elif event == cv2.EVENT_LBUTTONDOWN:
        item = None
        p_dist = 1000
        cnt = 0
        for p in global_points:
            d = euc_dist((x, y), p)
            if d < 8 and d < p_dist:
                p_dist = d
                item = cnt
            cnt += 1
        if item is not None:
            btn_down = True
        global_item = item

def update_all_view(global_points):
    global image
    img = image.copy()
    for i in range(0, len(global_points), 2):
        img = update_view(global_points[i], global_points[i+1], img)

def add_data(key, val, imsize, file_name = 'output.json'):
    if len(val) == 0:
        return
    if not os.path.exists(file_name):
        data = {}
        json.dump(data, open(file_name, 'w'))
    data = json.load(open(file_name, 'r'))
    data[key] = {}
    data[key]['points'] = val
    data[key]['width'] = imsize[1]
    data[key]['height'] = imsize[0]
    json.dump(data, open(file_name, 'w'))
    del data

def read_data(key, file_name = 'output.json'):
    if not os.path.exists(file_name):
        return []
    data = json.load(open(file_name, 'r'))
    if key in data:
        #print(data, data[key]['points'])
        return data[key]['points']
    return []


def main(args):
    global global_points, image
    cv2.namedWindow('Image')
    cv2.setMouseCallback("Image", mouse_handler)
    rink_img = cv2.imread(args.rink_path)
    #args.data_path = os.path.abspath(args.data_path)
    if not os.path.exists(args.data_path):
        print(args.data_path, ' -- Path not exists')
    #cv2.imshow('rink', rink_img)
    output_path = os.path.join(args.data_path, 'output.json')
    for file in os.listdir(args.data_path):
        print(file)
        full_path =os.path.join(args.data_path, file)
        img = cv2.imread(full_path)
        blank = np.zeros(img.shape, np.uint8)
        blank[0:rink_img.shape[0], 0: rink_img.shape[1]] = rink_img
        vis = np.concatenate((img, blank), axis=1)
        image = vis.copy()
        global_points = read_data(file, file_name = output_path)
        cv2.imshow('Image', image)
        update_all_view(global_points)
        fuck_this_loop = False
        while True:
            key = cv2.waitKey(1)
            if key == ord('n'):
                break
            elif key == ord('p'):
                p1, p2 = get_points()
                global_points += [p1, p2]
                #print('-->', p1, p2, global_points)
                update_all_view(global_points)
            elif key ==  ord('f'):
                fuck_this_loop = True
                break
        add_data(file, global_points, img.shape, file_name = output_path)
        if fuck_this_loop:
            break
    cv2.destroyAllWindows()

def parse_it():
    parser = argparse.ArgumentParser()

    parser.add_argument('-data_path', help='Path to dataset')
    parser.add_argument('-rink_path', default='rink.jpg', help='Rink image path')

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_it()
    main(args)


'''
[(1109, 139), (1298, 36), (888, 678), (1293, 280), (3, 209), (1495, 36), (10, 682), (1523, 294), (1274, 638), (1311, 117), (192, 116), (429, 250)]
'''