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
  
  
## Action classification model (Training)


### Installation

Completing this installation step is necessary for the training process.


1. Download **slowfast.yml** into your local device, then create a conda environment.
  ```bash
  conda env create -f  slowfast.yml
  conda activate slowfast
  ```   
2. To initiate the installation process, first, download **detectron2_repo.zip** and **pytorchvideo.zip**, and proceed with their installation.
  ```bash
  unzip detectron2_repo.zip
  pip install -e detectron2_repo
  unzip pytorchvideo.zip
  cd pytorchvideo
  pip install -e .
  ```  
3. To configure slowfast, obtain the **slowfast_train** and begin setting it up.
  ```bash
  cd slowfast_train
  python setup.py build develop
  ```  
4. Install the remaining dependencies. 
  ```bash
  pip install scipy
  pip install scikit-learn
  ```  
  
  
### Training procedure

  1. Dataset preparation <br/>
    - **Trimming Videos** the input videos should be a trimmed videos i.e., contains only one action in each video. <br/>
      ```bash
      python trim_videos.py --vid_path 'the path where the videos are saved in' --dist_path     'the path where the trimmed videos will be save' --view 'the needed video view to trim 1 for dashboard, 2 for right-side and 3 for rear view'
      ```   
     - **Prepare csv Files** for the training and validation sets.
  2. Download checkpoints from [here](https://drive.google.com/drive/folders/1RmWFoL_d-i2o83nXtXNZ3uLEH6UPa3Wk?usp=share_link)
  3. Prepare the configuration file and start training.
  
  
  
  
## Action classification model (Inference) 
  
### Installation

This installation step is needed for inference ..


1. Download **slowfast_inference.yml** into your local device, then create a conda environment
  ```bash
  conda env create -f  slowfast_inference.yml
  conda activate slowfast_inference
  ```   
2. Install detectron and pytorchvideo, download them from our repository, then start to install them
  ```bash
  unzip detectron2_repo.zip
  pip install -e detectron2_repo
  unzip pytorchvideo.zip
  cd pytorchvideo
  pip install -e .
  ```  
3. To configure slowfast, obtain the **slowfast_train** from our repository and begin setting it up.
  ```bash
  cd slowfast_Inference
  python setup.py build develop
  ```  
4. Install the remaining dependencies 
  ```bash
  pip install scipy
  pip install scikit-learn
  ```  

### The Inference steps for our framework as follow:
  1.
  2.
  3.
  4.
  

