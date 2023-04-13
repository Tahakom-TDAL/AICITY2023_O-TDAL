import glob 
import os 
import numpy 
import pandas
import cv2
import argparse 
import math 
import subprocess



config_path = '/mnt/lustre/talhussan/TDAL/slowfast_Inference/configs/SLOWFAST_8x8_R50.yaml'
checkpoint_path = '/mnt/lustre/talhussan/TDAL/slowfast_Inference/checkpoints/checkpoint_epoch_01010_rear.pyth'
checkpoint_type = 'pytorch'
angle = 'Rear'
videos_segments = glob.glob(f'/mnt/lustre/TAHAKOM/ActionRecognition/A2_v2_segmentation/t1/{angle}/*')
Out = '' 

def main (config_path, checkpoint_path, checkpoint_type, model_name, angle, videos_segments, Out) : 

    videos_segments =  glob.glob(videos_segments+'/*')
    
    
    
    if angle == 3: 
        angle_name = 'Rear'
    elif angle == 2:
        angle_name = 'Right'
    else:
        angle_name = ''


    for video_segments in videos_segments:

        data_path = video_segments
        saved_path_for_features_and_probability = Out + '/' + angle_name+'_features_and_probability_t1/' + data_path.split("/")[-1]
        os.makedirs(saved_path_for_features_and_probability, exist_ok = True)

        print("========saved_path_for_features_and_probability========")
        print(saved_path_for_features_and_probability)


        args = 'python tools/run_net.py --cfg '+ config_path +' --opts DATA.PATH_TO_DATA_DIR '+data_path +' TEST.CHECKPOINT_FILE_PATH '+checkpoint_path+' TEST.CHECKPOINT_TYPE '+checkpoint_type
        args = args + ' OUTPUT_DIR ' + saved_path_for_features_and_probability
        subprocess.call(args, shell=True)

        print("end")


    
        
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='extract features and probability')
    
    parser.add_argument('--config_path', metavar='path',
                        help='the path to the configration file.. ')
    
    parser.add_argument('--checkpoint_path', metavar='path',
                        help='the path to the checkpoint.. ')
    
    parser.add_argument('--angle', metavar='view type',
                        help='view type 2 for Right and 3 for Rear ..')
    
    parser.add_argument('--videos_segments', metavar='path',
                        help='the path of parent where the segments folders will be saved..')
    
    parser.add_argument('--dist_path', metavar='path', 
                        help='view type Rear or Right ..')

    args = parser.parse_args()

    checkpoint_type = 'pytorch'
    
    main(args.config_path, args.checkpoint_path, checkpoint_type, args.model_name, args.angle, args.videos_segments, args.dist_path)
