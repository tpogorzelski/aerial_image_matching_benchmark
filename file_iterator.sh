#!/bin/bash

DATASET_PATH="/mnt/d/Pobrane/dataset/"
PYTHON_INTERPRETER="/home/tomek/anaconda3/envs/imw/bin/python3"
PYTHON_SCRIPT="matcher.py"

find "$DATASET_PATH"gopro -mindepth 1 -maxdepth 1 -type f -name "*.jpg" | while read file
do
    $PYTHON_INTERPRETER $PYTHON_SCRIPT "$file" "arcgis" "False" #file_path, map_provider, map_rotation
    $PYTHON_INTERPRETER $PYTHON_SCRIPT "$file" "google" "False"
    $PYTHON_INTERPRETER $PYTHON_SCRIPT "$file" "geoportal" "False"

    $PYTHON_INTERPRETER $PYTHON_SCRIPT "$file" "arcgis" "True"
    $PYTHON_INTERPRETER $PYTHON_SCRIPT "$file" "google" "True"
    $PYTHON_INTERPRETER $PYTHON_SCRIPT "$file" "geoportal" "True"
  
done
