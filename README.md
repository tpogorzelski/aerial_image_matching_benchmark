<p align="center">
  <h1 align="center"><br>Aerial Image Matching Benchmark</h1> 
</p>

## Description
This tool compares many well-known image matching algorithms (implemented [here](https://github.com/Vincentqyw/image-matching-webui#image-matching-webuifind-matches-between-2-images)) in an automated manner. As a result of the work of this tool, a website is generated showing charts that can help you choose a specific algorithm for your goals. The repository also contains a set of aeronautical data for which tests have been performed.


The tool currently supports various popular image matching algorithms, namely:
- [x] [MASt3R](https://github.com/naver/mast3r), CVPR 2024
- [x] [DUSt3R](https://github.com/naver/dust3r), CVPR 2024
- [x] [OmniGlue](https://github.com/Vincentqyw/omniglue-onnx), CVPR 2024
- [x] [XFeat](https://github.com/verlab/accelerated_features), CVPR 2024
- [x] [RoMa](https://github.com/Vincentqyw/RoMa), CVPR 2024
- [x] [DeDoDe](https://github.com/Parskatt/DeDoDe), 3DV 2024
- [ ] [Mickey](https://github.com/nianticlabs/mickey), CVPR 2024
- [x] [GIM](https://github.com/xuelunshen/gim), ICLR 2024
- [ ] [DUSt3R](https://github.com/naver/dust3r), arXiv 2023
- [x] [LightGlue](https://github.com/cvg/LightGlue), ICCV 2023
- [x] [DarkFeat](https://github.com/THU-LYJ-Lab/DarkFeat), AAAI 2023
- [x] [SFD2](https://github.com/feixue94/sfd2), CVPR 2023
- [x] [IMP](https://github.com/feixue94/imp-release), CVPR 2023
- [ ] [ASTR](https://github.com/ASTR2023/ASTR), CVPR 2023
- [ ] [SEM](https://github.com/SEM2023/SEM), CVPR 2023
- [ ] [DeepLSD](https://github.com/cvg/DeepLSD), CVPR 2023
- [x] [GlueStick](https://github.com/cvg/GlueStick), ICCV 2023
- [ ] [ConvMatch](https://github.com/SuhZhang/ConvMatch), AAAI 2023
- [x] [LoFTR](https://github.com/zju3dv/LoFTR), CVPR 2021
- [x] [SOLD2](https://github.com/cvg/SOLD2), CVPR 2021
- [ ] [LineTR](https://github.com/yosungho/LineTR), RA-L 2021
- [x] [DKM](https://github.com/Parskatt/DKM), CVPR 2023
- [ ] [NCMNet](https://github.com/xinliu29/NCMNet), CVPR 2023
- [x] [TopicFM](https://github.com/Vincentqyw/TopicFM), AAAI 2023
- [x] [AspanFormer](https://github.com/Vincentqyw/ml-aspanformer), ECCV 2022
- [x] [LANet](https://github.com/wangch-g/lanet), ACCV 2022
- [ ] [LISRD](https://github.com/rpautrat/LISRD), ECCV 2022
- [ ] [REKD](https://github.com/bluedream1121/REKD), CVPR 2022
- [x] [CoTR](https://github.com/ubc-vision/COTR), ICCV 2021
- [x] [ALIKE](https://github.com/Shiaoming/ALIKE), TMM 2022
- [x] [RoRD](https://github.com/UditSinghParihar/RoRD), IROS 2021
- [x] [SGMNet](https://github.com/vdvchen/SGMNet), ICCV 2021
- [x] [SuperPoint](https://github.com/magicleap/SuperPointPretrainedNetwork), CVPRW 2018
- [x] [SuperGlue](https://github.com/magicleap/SuperGluePretrainedNetwork), CVPR 2020
- [x] [D2Net](https://github.com/Vincentqyw/d2-net), CVPR 2019
- [x] [R2D2](https://github.com/naver/r2d2), NeurIPS 2019
- [x] [DISK](https://github.com/cvlab-epfl/disk), NeurIPS 2020
- [ ] [Key.Net](https://github.com/axelBarroso/Key.Net), ICCV 2019
- [ ] [OANet](https://github.com/zjhthu/OANet), ICCV 2019
- [x] [SOSNet](https://github.com/scape-research/SOSNet), CVPR 2019
- [x] [HardNet](https://github.com/DagnyT/hardnet), NeurIPS 2017
- [x] [SIFT](https://docs.opencv.org/4.x/da/df5/tutorial_py_sift_intro.html), IJCV 2004

## How to use


### Requirements
``` bash
git clone --recursive https://github.com/tpogorzelski/aerial_image_matching_benchmark.git
cd aerial_image_matching_benchmark
conda env create -f environment.yaml
conda activate imw
```

### Configure script
``` bash
dataset_path="path/to/dataset"
matchers_list=("loftr" "topicfm" "aspanformer")
```

### Run computation
``` bash
./matcher_iterator.sh
```

### Run graphs
``` bash
streamlit run overview.py
```
then open http://localhost:8501 in your browser.


## Contributors

<a href="https://github.com/Vincentqyw/image-matching-webui/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Vincentqyw/image-matching-webui" />
</a>

## Resources
- [Image Matching: Local Features & Beyond](https://image-matching-workshop.github.io)
- [Long-term Visual Localization](https://www.visuallocalization.net)

## Acknowledgement

This code is built based on [Image Matching WebUI](https://github.com/Vincentqyw/image-matching-webui). 
