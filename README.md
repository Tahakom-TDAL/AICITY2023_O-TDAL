# O-TDAL: Online Temporal Driver Action Localization
This repository includes the implementation of the O-TDAL framework, a solution for Track 3 Naturalistic Driving Action Recognition of the [NVIDIA AI City 2023 Challenge](https://www.aicitychallenge.org/). <br />

**Important Note:** <br />
For reproducibility, you must use all the code provided in this repo. Using any files from the different version may give different results (e.g., git clone detectrion2 from the official repository)  <br />

## Overview 

## Framework 

<p align="center">
  
  <img src="https://github.com/Tahakom-TDAL/AICITY2023_O-TDAL/blob/main/imgs/Proposed%20framework.png" width="600" />
</p>
  
## Development Environment 

The code has been tested with the following hardware and software specifications: <br />
  -	4 GPUs Tesla V100 with 32 GB memory. 
  -	Driver Version 470.129.06.
  -	Cuda 11.3 and cudnn 8.
 
## Inference
  To use O-TDAL framework and produce the same result in the leaderboard (baseline module) you need to **use the Right-side view and Rear angle view only** videos and follow the following steps:
  1. Configuring slowfast environment. 
  2. Dataset preparation. <br/>
    - **Video Segmentation** to divide the untrimmed video into equal-length clips. <br/>
    - **Prepare csv file** for the feature and classes probabilities extraction. 
  3. Extracting action clips probabilities.
  4. Temporal localization to get the start and end time for each predicted distracted action in an untrimmed video.

### Slowfast environment

Completing this installation step is necessary for the inference process.


1. Download **slowfast_inference.yml** into your local device, then create a conda environment
  ```bash
  conda env create -f  slowfast_inference.yml
  conda activate slowfast_inference
  ```   
2. To initiate the installation process, first, download **detectron2_repo.zip** and **pytorchvideo.zip**, and proceed with their installation.
  ```bash
  unzip detectron2_repo.zip
  pip install -e detectron2_repo
  unzip pytorchvideo.zip
  cd pytorchvideo
  pip install -e .
  ```  
3. To configure slowfast, obtain the **slowfast_Inference** from our repository and begin setting it up.
  ```bash
  cd slowfast_Inference
  python setup.py build develop
  ```  
4. Install the remaining dependencies 
  ```bash
  pip install scipy
  pip install scikit-learn
  ```  

### Video segmentation

The following command takes untrimmed video as input and generate equal-length clips. To produce the same result in the leaderboard you should use the segmentation type 1 setting. Type one setting will divide the untrimmed video into (video length in second/2) clips.
 ```bash
 python trim_videos.py --vid_path 'path to the root of folders that contains videos' --dist_path 'specify the output path' --view 'the needed video view to trim 1 for dashboard, 2 for right-side and 3 for rear view' --segmentation_type 1
 ```
 The vid_path directory should be as the following structure:
```bash
IDs
├───user_id_#####
│   │   Rear_view_user_id_#####_NoAudio_#.mp4
│   │   Rear_view_user_id_#####_NoAudio_#.mp4
│   │   Right_side_window_user_id_#####_NoAudio_#
│   │   Right_side_window_user_id_#####_NoAudio_#
│   │   
│   ├───user_id_#####
│   │   Rear_view_user_id_#####_NoAudio_#.mp4
│   │   Rear_view_user_id_#####_NoAudio_#.mp4
│   │   Right_side_window_user_id_#####_NoAudio_#
│   │   Right_side_window_user_id_#####_NoAudio_#
```

### The Inference steps for our framework as follow:
  1.
  2.
  3.
  4.
  

