# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 12:42:43 2023

@author: talhussan
"""

import argparse 
import glob 
import pandas as pd
import os
from tqdm import tqdm
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip


ftr = [3600,60,1]

def make_dir(base_path, dir_name):
    dir_path = base_path+"/"+ dir_name 
    isExist = os.path.exists(dir_path)
    if not isExist:
       # Create a new directory because it does not exist
       os.makedirs(dir_path)
    return dir_path


def trim_video(df, dist):
    df = df.fillna(method='ffill') 
  
    
    user_id = '_'.join(df['Filename'][df['Filename'].index[0]].split('_')[-4:-1]).lower()
    

    df['Filename'] = df.Filename.apply(lambda x: x if x[:4] != 'Rear' else 'Rear_view_'+user_id.capitalize() +'_'+ x.split('_')[-1])

    ref_vid_path = IDs_path+'\\'+user_id
    
    
    df['ref_name'] = df.Filename.apply(lambda x: ref_vid_path+'\\'+'_'.join(x.split('_')[:-1]) \
                                       .lower().capitalize()+'_NoAudio_'+ x.split('_')[-1]+'.mp4')
        

    
    dist_1 = make_dir(dist, user_id)
    for ind, row in tqdm(df.iterrows(), total=df.shape[0]):
        start_time = sum([a*b for a,b in zip(ftr, map(int,row['Start Time'].split(':')))])
        start_time_ed = row['Start Time'].replace(':','_')[2:]

        end_time = sum([a*b for a,b in zip(ftr, map(int,row['End Time'].split(':')))])
        end_time_ed = row['End Time'].replace(':','_')[2:]

        class_no = row['Label (Primary)'].replace(' ','_')
        appear_block = row['Appearance Block']
        
        dist_path = make_dir(dist_1, row['Camera View'].replace(' ', '_'))
        dist_path = make_dir(dist_path, row['Appearance Block'].replace(' ', '_'))

        trim_vid_name = row['Filename'].lower().capitalize() + '_' + start_time_ed + '_' + end_time_ed + '_' + class_no + '_' + appear_block+'.mp4'
       
        ffmpeg_extract_subclip(row['ref_name'], start_time, end_time, targetname=dist_path +'\\'+ trim_vid_name)

    print(f'[INFO] - {user_id} video has been trimmed')       


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='trim videos')
    
    
    parser.add_argument('--vid_path', metavar='path', required=True,
                        help='the path where the videos are in ..')
    
    parser.add_argument('--dist_path', metavar='path', required=True,
                        help='the path where the trimmed videos will be saved ..')
    
    parser.add_argument('--view', required=True, type=int,
                        help='the needed video view to trim 1 for dashboard, 2 for right-side and 3 for rear view ..')
    
    views = ['Dashboard', 'Rightside Window', 'Rearview']
    args = parser.parse_args()
    
    IDs_path = args.vid_path
    dist = args.dist_path
    view = args.view
    
    
    csv_files_ls = glob.glob(f'{IDs_path}\*\*.csv')
    csv_ls = [ pd.read_csv(i) for i in csv_files_ls ]
    [ trim_video(i[i['Camera View'] == views[view-1]] , dist) for i in tqdm(csv_ls) ]
    
    