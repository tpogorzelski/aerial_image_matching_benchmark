import common.utils as utils
import cv2
import csv
import os
import torch
import time
import json 
import argparse
import gc

# os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'max_split_size_mb:30'

headers = {'folder': None}
list_of_matchers = utils.matcher_zoo.keys()
headers.update(dict.fromkeys(list_of_matchers, None))
field_names = list(headers.keys())
    
class File():
    def __init__(self, file_name):
        self.file = open(file_name, 'a')
        self.writer = csv.DictWriter(self.file, fieldnames = field_names, delimiter=",")
        if os.stat(file_name).st_size == 0:
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
    parser = argparse.ArgumentParser(description='folder path, map provider')
    parser.add_argument('file_path', type=str, help='Path to the folder containing the dataset.')
    parser.add_argument('map_provider', type=str, help='Specify map provider from folder.')
    parser.add_argument('rotation', type=str, help='Specify if map should be rotated.')
    args = parser.parse_args()
  
    file_name = os.path.basename(args.file_path)
    dataset_folder = os.path.dirname(os.path.dirname(args.file_path))
    map_provider = args.map_provider
    map_rotation = args.rotation
    
    match_threshold = 0.1
    extract_max_keypoints = 1000
    keypoint_threshold = 0.015
    DEFAULT_RANSAC = "USAC_MAGSAC"

    if map_rotation == 'True':
        print('Map rotation is enabled.')
        raw_matches = File(dataset_folder + '/raw_matches_' + map_provider + '_rotated' + '.txt')
        ransac_matches = File(dataset_folder + '/ransac_matches_' + map_provider + '_rotated' + '.txt')
        time_matches = File(dataset_folder + '/time_matches_' + map_provider + '_rotated' + '.txt')
    elif map_rotation == 'False':
        raw_matches = File(dataset_folder + '/raw_matches_' + map_provider + '.txt')
        ransac_matches = File(dataset_folder + '/ransac_matches_' + map_provider + '.txt')
        time_matches = File(dataset_folder + '/time_matches_' + map_provider + '.txt')
        
    image0 = cv2.imread(args.file_path)
    # image0 = cv2.resize(image0, (0,0), fx=0.1, fy=0.1)
    
    image1 = cv2.imread(dataset_folder + "/" + map_provider + "/" + file_name)
    # image1 = cv2.resize(image1, (0,0), fx=0.1, fy=0.1)
    
    with open(args.file_path[:-4] + '.json', 'r') as file:
        parameters = json.load(file)
    
    if map_rotation:
        image1 = rotate_image(image1, parameters['yaw'])
    
    raw_row = {'folder': file_name}
    ransac_row = {'folder': file_name}
    time_row = {'folder': file_name}
    
    remaining_matchers = list(list_of_matchers)
    
    for matcher in list_of_matchers:
        print("\033[92mMatcher: {} \033[0m".format(matcher))
        
        input = image0, image1, match_threshold, extract_max_keypoints, keypoint_threshold, matcher, None
        
        try:
            torch.cuda.empty_cache()
            start_time = time.time()
            output = utils.run_matching(*input)
            raw_row.update({matcher:output[3]['number raw matches']})         
            ransac_row.update({matcher:output[3]['number ransac matches']})
            time_row.update({matcher:round(time.time() - start_time, 2)})
            remaining_matchers.remove(matcher)
            
            del output
            gc.collect()
            
        except Exception as e:
            print(e)
            continue
     
    if len(remaining_matchers) > 0:
        print('### failed:', remaining_matchers, ' ###')
    else:
        print('### all success ###')
      
    raw_matches.write_row(raw_row)    
    ransac_matches.write_row(ransac_row)
    time_matches.write_row(time_row)
             
    raw_matches.close()
    ransac_matches.close()
    time_matches.close()

