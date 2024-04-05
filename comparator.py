import common.utils as utils
import cv2
import csv
import os
import torch
import time
import json 
import argparse

# os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'max_split_size_mb:21'

dataset_path = '/mnt/d/Pobrane/dataset/'
headers = {'folder': None}
list_of_matchers = utils.matcher_zoo.keys()
headers.update(dict.fromkeys(list_of_matchers, None))
field_names = list(headers.keys())
    
class File():
    def __init__(self, file_name):
        self.file = open(dataset_path + file_name, 'w')
        self.writer = csv.DictWriter(self.file, fieldnames = field_names, delimiter=",")
        self.writer.writeheader()
    
    def write_row(self, row):
        self.writer.writerow(row)
        self.file.flush()
           
    def close(self):
        self.file.close()

def rotate_image(image, angle):
    height, width = image.shape[:2]
    center = (width // 2, height // 2)

    return cv2.warpAffine(image, cv2.getRotationMatrix2D(center, angle, scale=1.0), (width, height))
   
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='dataset path')
    
    parser.add_argument('dataset_path', type=str, help='Path to the folder containing the dataset.')

    args = parser.parse_args()
    
    folders = os.listdir(args.dataset_path)
    
    match_threshold = 0.1
    extract_max_keypoints = 1000
    keypoint_threshold = 0.015
    DEFAULT_RANSAC = "USAC_MAGSAC"

    raw_matches = File('raw_matches.txt')
    ransac_matches = File('ransac_matches.txt')
    ransac_matches_rotated = File('ransac_matches_rotated.txt')
    time_matches = File('time_matches.txt')
    
    for folder in folders:
        print('\n', folder, end=': ')
        image0 = cv2.imread(dataset_path + folder + "/camera.jpg")
        image0 = cv2.resize(image0, (0,0), fx=0.25, fy=0.25)
        
        image1 = cv2.imread(dataset_path + folder + "/map.jpg")
        image1 = cv2.resize(image1, (0,0), fx=0.25, fy=0.25)
        
        with open(dataset_path + folder + '/parameters.json', 'r') as file:
            parameters = json.load(file)
        
        image1_rotated = rotate_image(image1, parameters['yaw'])
        
        raw_row = {'folder': folder}
        ransac_row = {'folder': folder}
        ransac_row_rotated = {'folder': folder}
        time_row = {'folder': folder}
        
        remaining_matchers = list(list_of_matchers)
        
        for matcher in list_of_matchers:
            print("\033[92mMatcher: {} \033[0m".format(matcher))
            
            try:
                #check without rotation
                torch.cuda.empty_cache()
                start_time = time.time()
                output = utils.run_matching(image0, image1, match_threshold, extract_max_keypoints, keypoint_threshold, matcher, None)
                raw_row.update({matcher:output[3]['number raw matches']})         
                ransac_row.update({matcher:output[3]['number ransac matches']})
                time_row.update({matcher:round(time.time() - start_time, 2)})
                remaining_matchers.remove(matcher)
                
                #check after rotation
                output = utils.run_matching(image0, image1_rotated, match_threshold, extract_max_keypoints, keypoint_threshold, matcher, None)
                ransac_row_rotated.update({matcher:output[3]['number raw matches']})  
                
            except Exception as e:
                print(e)
                continue
           
        raw_matches.write_row(raw_row)    
        ransac_matches.write_row(ransac_row)
        ransac_matches_rotated.write_row(ransac_row_rotated)
        time_matches.write_row(time_row)
        
        if len(remaining_matchers) > 0:
            print('### failed:', remaining_matchers, ' ###')
        else:
            print('### all success ###')
                   
    raw_matches.close()
    ransac_matches.close()
    ransac_matches_rotated.close()
    time_matches.close()
