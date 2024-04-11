#!/bin/bash

DATASET_PATH="/mnt/d/Pobrane/dataset"
PYTHON_INTERPRETER="python3"
PYTHON_SCRIPT="./matcher.py"

matchers_list=("loftr" "topicfm" "aspanformer" "dedode" "superpoint+superglue" "superpoint+lightglue" "disk" "disk+dualsoftmax" "superpoint+dualsoftmax" "disk+lightglue" "superpoint+mnn" "sift+sgmnet" "sosnet" "hardnet" "d2net" "rord" "alike" "lanet" "r2d2" "darkfeat" "sift" "roma" "DKMv3" "gluestick" "sold2")
matchers_list=("loftr" "topicfm")

for matcher in "${matchers_list[@]}"; do
    echo "$matcher"
    $PYTHON_INTERPRETER $PYTHON_SCRIPT $DATASET_PATH $matcher
done

