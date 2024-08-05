import pandas as pd
import os
import json
import altair as alt
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import random
import cv2
from math import *
import requests

def latlon2relativeXY(lat, lon):
    x = (lon + 180) / 360
    y = (1 - log(tan(radians(lat)) + sec(radians(lat))) / pi) / 2
    return(x,y)

def latlon2tiles_float(lat, lon, z):
    n = numTiles(z) 
    x,y = latlon2relativeXY(lat,lon)
    return [n*x, n*y]

def sec(x):
    return(1/cos(x))

def numTiles(z):
    return(pow(2,z))

def zoomFromAGL(agl):
    if agl < 0:
        print(f"ERROR: Altitude {agl} is below 0")
        exit()
    
    zoom = round(32*agl**(-0.11))
    
    if zoom > 20: #the highest value of ArcGIS maps in Rzeszów area
        zoom = 20

    return zoom 

def get_tile(z, x, y):
     
    url = f'https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'
    
    while True:
        response = requests.get(url)
        response.raise_for_status()  

        if response.content is not None:
            image = np.asarray(bytearray(response.content), dtype="uint8")
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
            return image

def concat_tile(im_list_2d):
    return cv2.vconcat([cv2.hconcat(im_list_h) for im_list_h in im_list_2d])

def map_from_center_tile(zoom, map_center_tile):
    tile_matrix = []

    x, y = map_center_tile
    map_center_tile = [round(x), round(y)]
    
    for y in range(map_center_tile[1]-3, map_center_tile[1]+4):         #oś y
        tile_matrix.append([])

        for x in range(map_center_tile[0]-3, map_center_tile[0]+4):     #oś x
            
            print(f'Try to download {x}, {y}, {z} tile')
            tile = get_tile(zoom, x, y) #TODO: zmienić 'Rzeszów' na zmienną
            
            tile_matrix[y - (map_center_tile[1] - 3)].append(tile)
        
    map_7x7 = concat_tile(tile_matrix)
    
    return map_7x7

def overlay_images(background, image):

    h, w, z = background.shape
    h2, w2, z2 = image.shape
    
    mask = np.where(image > 0, 255, 0)
    mask = cv2.convertScaleAbs(mask)

    background = cv2.subtract(background, mask[:, :, :3])

    return cv2.add(background, image)
    
altitudes = [150, 500, 1500]
matchers=("LoFTR", "TopicFM", "AspanFormer", "DeDoDe", "SuperPoint+SuperGlue", "SuperPoint+LightGlue", "DISK", "DISK+DualSoftmax", "SuperPoint+DualSoftmax", "DISK+LightGlue", "SuperPoint+MNN", "SIFT+SGMNet", "SOSNet", "HardNet", "D2Net", "RORD", "ALIKE", "LANET", "R2D2", "DARKFeat", "SIFT", "ROMA", "DKMv3", "GlueStick", "SOLD2")

image_folder = "/mnt/d/Pobrane/dataset/dataset_lot2/"
dataset_path = "./experiments/alt_1500/"

for matcher in matchers:
  
    data = pd.read_csv(dataset_path + str(matcher).lower() + ".csv", sep=";")
    
    # for i in range(len(data)):
    i = 0  
    # print(data['file_gopro'][i])  
    
    image = cv2.imread(image_folder + "gopro/" + data['file_gopro'][i])
    with open(dataset_path + "gopro/" + data['file_gopro'][i][:-3] + 'json', 'r') as file:
        json_data = json.load(file)
    
    lat = json_data['lat']
    lon = json_data['lon']
    z = zoomFromAGL(json_data['altitude_agl']) +1
    
    if not isinstance(data['H_arcgis'][i], str):
        print(matcher, "\t\t-", data['file_gopro'][i])
        continue
    else:
        print(matcher, "\t\t+", data['file_gopro'][i])

    H = np.array(data['H_arcgis'][i].replace("[", "").replace("]", "").split(",")).astype(np.float32).reshape(3, 3)
    
    H = np.linalg.inv(H)
    image_H = cv2.warpPerspective(image, H, (1792, 1792))
    
    map7x7 = map_from_center_tile(z, latlon2tiles_float(lat, lon, z))
    # map7x7 = cv2.imread("/mnt/d/Pobrane/dataset/dataset_lot2/gopro_H/100327_map.jpg")
    
    cv2.imwrite(image_folder + "gopro_H/" + data['file_gopro'][i][:-4] + "_map" + ".jpg", map7x7)
    exit()
    cv2.imwrite(image_folder + "gopro_H/" + data['file_gopro'][i][:-4] + "_" + matcher + ".jpg", overlay_images(map7x7, image_H))
    
    
  