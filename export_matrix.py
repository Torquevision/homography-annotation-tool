
import numpy as np
import cv2
import os
import argparse
import json

def main(args):
    json_path = os.path.join(args.data_path, 'output.json')
    data = json.load(open(json_path))
    w = open(os.path.join(args.data_path, 'annotations.txt'), 'w')
    for file in data:
        file_path = os.path.join(args.data_path, file)
        src_points, dest_points = [], []
        for i in range(0, len(data[file]['points']), 2):
            src_points.append(data[file]['points'][i])
            dest_points.append(data[file]['points'][i+1])
        
        src_points = np.array(src_points)
        dest_points = np.array(dest_points)
        h = None
        if len(src_points) >= 4:
            h, status = cv2.findHomography(src_points, dest_points)

        if h is not None:
            s = ' '.join([file] + [str(k) for k in h.reshape(9).tolist()][:-1])
            #print(s)
            w.write(s + '\n')
        else:
            print('--> Skipping ', file, h)
    w.close()
    print('output saved at', os.path.join(args.data_path, 'annotations.txt'))

def parse_it():
    parser = argparse.ArgumentParser()

    parser.add_argument('-data_path', help='Path to dataset')
    parser.add_argument('-rink_path', default='rink.jpg', help='Rink image path')

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_it()
    main(args)