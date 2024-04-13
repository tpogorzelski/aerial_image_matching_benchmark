#!/bin/bash

if [ ! -d "third_party/SGMNet/weights" ]; then
    tar -xzf third_party/SGMNet/weights.tar.gz -C third_party/SGMNet
fi

DATASET_PATH="/mnt/d/Pobrane/dataset"
# matchers_list=("loftr" "topicfm" "aspanformer" "dedode" "superpoint+superglue" "superpoint+lightglue" "disk" "disk+dualsoftmax" "superpoint+dualsoftmax" "disk+lightglue" "superpoint+mnn" "sift+sgmnet" "sosnet" "hardnet" "d2net" "rord" "alike" "lanet" "r2d2" "darkfeat" "sift" "roma" "DKMv3" "gluestick" "sold2")
matchers_list=("disk" "disk+dualsoftmax" "disk+lightglue" "d2net" "rord" "lanet" "DKMv3" "gluestick")

for matcher in "${matchers_list[@]}"; do
    echo "$matcher"
    python3 matcher.py $DATASET_PATH $matcher
done
