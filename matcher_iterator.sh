#!/bin/bash

if [ ! -d "third_party/SGMNet/weights" ]; then
    tar -xzf third_party/SGMNet/weights.tar.gz -C third_party/SGMNet
fi

dataset_path="/path/to/Czajka_dataset"
matchers_list=("LoFTR" "TopicFM" "AspanFormer" "DeDoDe" "SuperPoint+SuperGlue" "SuperPoint+LightGlue" "DISK" "DISK+dualsoftmax" "superpoint+dualsoftmax" "DISK+LightGlue" "SuperPoint+MNN" "SIFT+SGMNet" "SOSNet" "HardNet" "D2Net" "RORD" "ALIKE" "LANET" "R2D2" "DARKFeat" "SIFT" "ROMA" "DKMv3" "GlueStick" "SOLD2")

for folder in $dataset_path/*; do
    if [ -d "$folder" ]; then
        echo "Processing folder: $folder"
        for matcher in "${matchers_list[@]}"; do
            echo "$matcher"
            python3 matcher.py $folder $matcher
        done
    fi
done
