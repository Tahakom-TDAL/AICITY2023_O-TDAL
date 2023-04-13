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
3. To configure slowfast, obtain the **slowfast_Inference** and begin setting it up.
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

The following command takes untrimmed video as input and generate equal-length clips. To produce the same result in the leaderboard you should use the segmentation type 1 setting. Type one setting will divide the untrimmed video into (video length in second/2) clips. You can use **“data_preparation/inference/videoSegmentation.py”** for that.
 ```bash
  python videoSegmentation.py --vid_path 'path to the root of folders that contains videos' --segmentation_type 1 --view 'the needed video view to trim 1 for dashboard, 2 for right-side and 3 for rear view'
 ```

 The vid_path directory should be as the following structure:
```bash
vid_path
├───user_id_*****
│   │   Rear_view_user_id_*****_NoAudio_*.mp4
│   │   Rear_view_user_id_*****_NoAudio_*.mp4
│   │   Right_side_window_user_id_*****_NoAudio_*.mp4
│   │   Right_side_window_user_id_*****_NoAudio_*.mp4
│   │   ...
│   │  
│   ├───user_id_#####
│   │   Rear_view_user_id_*****_NoAudio_*.mp4
│   │   Rear_view_user_id_*****_NoAudio_*.mp4
│   │   Right_side_window_user_id_*****_NoAudio_*.mp4
│   │   Right_side_window_user_id_*****_NoAudio_*.mp4
│   │   ...
│   │  
```

### Prepare csv file

After completing the video segmentation step, you need to generate a csv file for video's clips. The csv file should contain all clips paths for a single video sorted **in ascending order** with dummy labels. If the order of paths is changed then it will result in an unexpected and wrong results in last stage. You can use **“data_preparation/inference/prepare_csv.py”** for that.
  ```bash
  python prepare_csv.py --segments_folders 'path to the root of folders that contains videos clips'
  ``` 
The segments_folders directory should be as the following structure:
```bash
segments_folders
├───Rear_view_user_id_*****_NoAudio_*
│   │   P_00000.mp4
│   │   P_00001.mp4
│   │   P_00002.mp4
│   │   P_00003.mp4
│   │   ...
│   │  
│   ├───Rear_view_user_id_*****_NoAudio_*
│   │   P_00000.mp4
│   │   P_00001.mp4
│   │   P_00002.mp4
│   │   P_00003.mp4
│   │   ...
│   │  
```

### Extract features and probabilities
To extract the clips features and probabilities, run the following command after specifying the path for the test.csv generated in the previous step using DATA.PATH_TO_DATA_DIR argument. After that, specify the checkpoint of Right-side window (checkpoint_epoch_01035_right.pyth) or Rear view (checkpoint_epoch_01010_rear.pyth) using TEST.CHECKPOINT_FILE_PATH argument. If you do not have the checkpoints, you can download it from [here](https://drive.google.com/drive/folders/1EVJOy73PsG99p7EYZJEpextCDeQovldn)

  ```bash
python extract_features_probabilities.py --config_path configs/Kinetics/SLOWFAST_8x8_R50.yaml --checkpoint_path checkpoints/checkpoint_epoch_01035_right.pyth --angle '2 for right-side and 3 for rear view' --videos_segments 'path to the root of folders that contains videos clips' --dist_path 'specify the output path'
  ``` 

### Temporal localization
To generate the submission file that contains video id, action classes and the start and end time for each action. The baseline_TAL.py takes probabilities_path and vid_ids as input. probabilities_path is the path to the folder that contains the videos probabilities. Where, vid_ids is video_ids.csv contains the videos names and Ids.
```bash
python baseline_TAL.py --vid_path 'path to the root of folders that contains videos' --vid_ids 'The path for video_ids.csv file; need for mapping' --probabilities_path 'path to the folder that contains folders of videos probabilities' --out_file 'path to the folder where the temporal locations file to be saved'
``` 
The input file structure should be as the following:
```bash
probabilities_path
├───Rear_view_user_id_*****_NoAudio_*
│   │   P_00000.npz
│   │   P_00001.npz
│   │   P_00002.npz
│   │   P_00003.npz
│   │   ...
│   │  
│   ├───Right_side_window_user_id_*****_NoAudio_*
│   │   P_00000.npz
│   │   P_00001.npz
│   │   P_00002.npz
│   │   P_00003.npz
│   │   ...
```


---
## Acknowledgement
This repository depends heavily on [SlowFast]


## General Notes 
- Loading checkpoints from the google drive may take time due to the size of the checkpoint file.
- We have reproduced the results and run the code on different machines. So, if you find different results than ours, please contact us.

##  Contact information 
If you faced any issues please don't hesitate to contact us :
 > Munirahalyahya21@gmail.com <br />
 > Amalsu0@gmail.com <br />
 > Shahadaalghannam@gmail.com <br />
 > Taghreedalhussan@gmail.com <br />
  

