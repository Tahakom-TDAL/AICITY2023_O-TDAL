#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 12:23:23 2023

@author: M
"""


'''
this script read frames of videos and save each 30 + 2 frames in single video, then get the next 30 + 2 frame 
as so on. 
the 2 in the end of the previous video will be the first frames in the next video ..
'''

import glob 
import os 
import numpy 
import pandas
import cv2
import argparse 
import math 


num_frames = 64


def init(video_path):
    cap = cv2.VideoCapture(video_path)
    full_rate =  rate = cap.get(cv2.CAP_PROP_FPS)
    width  = cap.get(cv2.CAP_PROP_FRAME_WIDTH )   # float `width`
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float `height`
    vid_length = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    # width = vcap.get(3)
    # height = vcap.get(4)
    # fps = vcap.get(5)
    return full_rate, width, height, vid_length



    

def video_segment_type1(file_paths, out_file) : 
    
    videos_paths = file_paths
    
    for path in videos_paths:
        # path = path[0].replace("/workspace", 'VideosD')
        video_name = os.path.basename(path)[:-4]
        # parent_name = os.path.basename(os.path.dirname(os.path.dirname(path)))
        print(video_name)
        # out_file_name = os.path.join(video_out_file, parent_name+'_'+video_name)
        out_file_name = os.path.join(out_file, video_name)
        print(out_file_name)
        
        if not os.path.exists(out_file_name) :
            print("create path ")
            os.makedirs(out_file_name)
             
        full_rate, width, height, vid_length = init(path)
        print(full_rate, width, height, vid_length )
        reminder = vid_length % 60
        print('reminder', reminder)
        sub_videos_number = math.ceil(vid_length / 60)
        print('sub_videos_number', reminder)

        stream = cv2.VideoCapture(path)

        frame_counter = 0
        sub_videos = 0
        prev_frames_list = []
        sub_video_frame_counter = 0
        sub_videos = 0
        while (1):
            
            ret, frame = stream.read()

            if not ret:
                break

            if sub_video_frame_counter == num_frames or sub_videos == 0 :
                

                sub_videos += 1
                out_sub_video = os.path.join(out_file_name, '{:05d}.mp4'.format(sub_videos))
                output = cv2.VideoWriter(out_sub_video, 
                                     cv2.VideoWriter_fourcc(*'mp4v'), 
                                     full_rate, 
                                     (int(width), int(height)))
            
                print("starting new video = ", sub_videos)
                print('1 length  prev_frames_list = ', len(prev_frames_list))
                sub_video_frame_counter = 0
                for prev_frame in prev_frames_list:
                    
                    sub_video_frame_counter += 1
                    output.write(prev_frame)
                prev_frames_list = []
            # sub_videos += 1
            
            output.write(frame)
            sub_video_frame_counter += 1

        
            if reminder != 0 and sub_videos_number-1 == sub_videos:
                
                print("reminder = ",  reminder)
                max_frame = num_frames - reminder
            else:
                
                max_frame = num_frames - 4

            if sub_video_frame_counter > max_frame:
                
                print('appending prev frame = ', frame_counter)
                print(' max_frame = ', max_frame)
                prev_frames_list.append(frame)
                print('2 length  prev_frames_list = ', len(prev_frames_list))

            frame_counter += 1


def video_segment_type2(file_paths, out_file) : 
    
    for f in file_paths : 
    
        f_frames = glob.glob(f+"/*")
        f_frames.sort()
        pre_frame_index = 0 
        secs = len(f_frames) / 30
        vid_id = 1  
        ind = 45 

        while ( vid_id < secs ) : 
            f_name = f.split("/")[-1]  # get folder name 
            f_out_path = os.path.join(out_file, f_name) # out folder 
            # create folder for this video 
            if not os.path.exists(f_out_path) :
                os.mkdir(f_out_path)
    
            video_name = f_name+"/"+str(vid_id) # video name 
            # video mp4 path 
            video_out_path = os.path.join(out_file, video_name+'.mp4') # or f_out_path + "/" + vid_id + ".mp4"
        
            img =  cv2.imread(f_frames[0])
            width = img.shape[1]
            height = img.shape[0]
            #print('width, height', width, height)
            output = cv2.VideoWriter(os.path.join(f_out_path, '{:05d}.mp4'.format(vid_id)), 
                                    cv2.VideoWriter_fourcc(*'mp4v'), 
                                    30, 
                                    (width, height))
        
        
            # get last index frame for the file 
        
            if vid_id == 1 :
                post_frame_index = 64 
            elif vid_id < secs  :
                pre_frame_index = ind - 32
                post_frame_index = ind + 32
                ind = ind + 30 
            else :     
                pre_frame_index = ind - 32 
                post_frame_index = len(f_frames) # get last index 
            
            # Handling : to double check after elif post_frame_index value not exceed len(f_frames)
            
            if (vid_id > secs ) : 
                post_frame_index = len(post_frame_index)

            # get the id of the frames that will be wrtien     
            img_ids = f_frames[pre_frame_index : post_frame_index ]

            # write frames in the created video 
            for img in img_ids:
                img = cv2.imread(img)
                output.write(img)
                

            # update values for next iteration 
            vid_id = vid_id + 1 


def video_segment_type3(file_paths, out_file) : 

    videos_paths = file_paths
    
    for path in videos_paths:
        video_name = os.path.basename(path).split(".")[0]
        print(video_name)
        out_file_name = os.path.join(out_file, video_name)
        print(out_file_name)
        if not os.path.exists(out_file_name) :
            os.makedirs(out_file_name, )
             
        full_rate, width, height, vid_length = init(path)
        print(vid_length)
        
        #=================================== Shahad 
        
        number_of_seg = vid_length/full_rate 
        number_of_seg = int(number_of_seg)
        print(f"number_of_seg == {number_of_seg}")
        stream = cv2.VideoCapture(path)
        seg_count = 1
        saved_seg_count = 0
        one_seg_frames_count = 0
        
        first_frames_list = []
        second_frames_list = [] 
        third_frames_list = [] 
        
        while (1):
            
            ret, frame = stream.read()

            # if not ret:
            #     break
            
            if seg_count == 1 and len(first_frames_list) < full_rate:
                first_frames_list.append(frame)
                if len(first_frames_list) == full_rate:
                    seg_count =+1

            elif seg_count == 2 and len(second_frames_list) < full_rate:
               second_frames_list.append(frame)
               if len(second_frames_list) == full_rate:
                    seg_count =+1
                    
            elif seg_count == 3:
                # save first segment
                # TODO: Handel first case
                # create segment video 
                third_frames_list.append(frame)
                if len(third_frames_list) != full_rate:
                    continue
            
                seg_count =+1
                saved_seg_count +=1
                out_seg_video = os.path.join(out_file_name, '{:05d}.mp4'.format(saved_seg_count))
                output = cv2.VideoWriter(out_seg_video, cv2.VideoWriter_fourcc(*'mp4v'), full_rate, (int(width), int(height)))
                print(f"start creating new video segment = {saved_seg_count}")
                
                # write full first list frames
                for f_frame in first_frames_list:
                    one_seg_frames_count += 1
                    output.write(f_frame)
                    
                # write full second list frames
                for s_frame in second_frames_list:
                    one_seg_frames_count += 1
                    output.write(s_frame)          
                
                # write only 4 frames from third list frames
                for t_frame in third_frames_list:
                    one_seg_frames_count += 1
                    output.write(t_frame)
                    
                    if one_seg_frames_count == num_frames:
                        print(f"Check number of written frames == {one_seg_frames_count}")
                        
                
                # lists switchs 
                first_frames_list = second_frames_list
                second_frames_list = third_frames_list
                third_frames_list = [] 
                one_seg_frames_count = 0 
                
            elif (saved_seg_count+1) == (number_of_seg-1): #last second will be ignored, and from prev iter I have frames
            
                saved_seg_count +=1
                out_seg_video = os.path.join(out_file_name, '{:05d}.mp4'.format(saved_seg_count))
                output = cv2.VideoWriter(out_seg_video, cv2.VideoWriter_fourcc(*'mp4v'), full_rate, (int(width), int(height)))
                #print(f"start creating new video segment = {saved_seg_count}")
                
                # write only 4 frames from first list frames
                for i in range(-4,0):
                    one_seg_frames_count += 1
                    print(i)
                    f_frame = first_frames_list[i]
                    output.write(f_frame)
            
                # write full second list frames
                for s_frame in second_frames_list:
                    one_seg_frames_count += 1
                    output.write(s_frame)          
                
                # write full frames from third list frames
                for t_frame in third_frames_list:
                    one_seg_frames_count += 1
                    output.write(t_frame)
            
                
                print(f"Check number of written frames == {one_seg_frames_count}")
                break
                
            else:

                
                third_frames_list.append(frame)
                if len(third_frames_list) != full_rate:
                    continue
            
                seg_count =+1
                
                saved_seg_count +=1
                out_seg_video = os.path.join(out_file_name, '{:05d}.mp4'.format(saved_seg_count))
                output = cv2.VideoWriter(out_seg_video, cv2.VideoWriter_fourcc(*'mp4v'), full_rate, (int(width), int(height)))
                print(f"start creating new video segment = {saved_seg_count}")
                
                # write full first list frames
                for f_frame in first_frames_list:
                    one_seg_frames_count += 1
                    output.write(f_frame)
                    
                # write full second list frames
                for s_frame in second_frames_list:
                    one_seg_frames_count += 1
                    output.write(s_frame)          
                
                # write only 4 frames from third list frames
                for t_frame in third_frames_list:
                    one_seg_frames_count += 1
                    output.write(t_frame)
                    
                    if one_seg_frames_count == num_frames:
                        print(f"Check number of written frames == {one_seg_frames_count}")
                        break
                
                # lists switchs 
                if (saved_seg_count+1) != (number_of_seg-1):
                    first_frames_list = second_frames_list
                    second_frames_list = third_frames_list
                    third_frames_list = [] 
                    
                one_seg_frames_count = 0 
            
            
def main (file_paths_frames, file_paths_video, out_file, segmentation_type) : 
    
    if segmentation_type == '1' : 
        video_segment_type1(file_paths_video, out_file)
    elif segmentation_type == '2' : 
        video_segment_type2(file_paths_frames, out_file)
    else :
        video_segment_type3(file_paths_video, out_file)

    
    
        
    
        
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='video segmentation')
    
    parser.add_argument('--file_paths_frames', metavar='path',
                        help='the path to the folder that contains folders for all video frames .. ')
    
    parser.add_argument('--file_paths_video', metavar='path',
                        help='the path to the folder that contains for all video in .mp4 format .. ')
    
    parser.add_argument('--out_file', metavar='path', required=False,
                        help='the path where the segments will be saved ..')
    
    parser.add_argument('--segmentation_type', metavar='path', required=False,
                        help='segmentation type 1 or 2, 3 ..')
    
    parser.add_argument('--veiw_type', metavar='path', required=False,
                        help='view type Rear or Right ..')

    args = parser.parse_args()
    
    if args.segmentation_type == '1' or args.segmentation_type == '3'  : 

        file_paths_video = glob.glob(args.file_paths_video+"/*/"+args.veiw_type+"*")  
        print(file_paths_video)
        file_paths_frames = ''  
        
    else :
    	file_paths_frames = glob.glob(args.file_paths_frames+"/*")
        file_paths_video = ''
        
    out_file = args.out_file
    

    segmentation_type = args.segmentation_type
    main(file_paths_frames, file_paths_video, out_file+os.sep+args.veiw_type, segmentation_type)

