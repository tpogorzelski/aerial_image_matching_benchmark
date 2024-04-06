#!/bin/bash

# Definiowanie ścieżki do głównego katalogu do przeszukania
MAIN_FOLDER_PATH='/mnt/d/Pobrane/dataset/'

# Definiowanie ścieżki do interpretera Pythona i skryptu Pythona
PYTHON_INTERPRETER="/home/tomek/anaconda3/envs/imw/bin/python3"
MY_PYTHON_SCRIPT="matcher_iterator.py"

# Znajdowanie folderów i uruchamianie skryptu Python dla każdego z nich
find "$MAIN_FOLDER_PATH" -mindepth 1 -maxdepth 1 -type d | while read folder
do
    $PYTHON_INTERPRETER $MY_PYTHON_SCRIPT "$folder" "arcgis" "False" #folder_path, map_provider, map_rotation
    $PYTHON_INTERPRETER $MY_PYTHON_SCRIPT "$folder" "google" "False"
    $PYTHON_INTERPRETER $MY_PYTHON_SCRIPT "$folder" "geoportal" "False"

    $PYTHON_INTERPRETER $MY_PYTHON_SCRIPT "$folder" "arcgis" "True"
    $PYTHON_INTERPRETER $MY_PYTHON_SCRIPT "$folder" "google" "True"
    $PYTHON_INTERPRETER $MY_PYTHON_SCRIPT "$folder" "geoportal" "True"

done
