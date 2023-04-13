# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 00:08:00 2023

@author: talhussan
"""

import argparse 
import glob 
import pandas as pd
import os


def make_csv_file(all_vids, val_ids):
    train_list = []
    val_list = []
    
    for row in all_vids : 
        
        label = row.split('_')[-2]
        vid_id = row.split(os.sep)[-4].split('_')[-1]
        if vid_id in val_ids:
            val_list.append([row, label])
        else:
            train_list.append([row, label])
    
        
    return pd.DataFrame(train_list), pd.DataFrame(val_list)  
      

def make_dir(base_path, dir_name):
    dir_path = base_path+"/"+ dir_name 
    isExist = os.path.exists(dir_path)
    if not isExist:
       # Create a new directory because it does not exist
       os.makedirs(dir_path)
    return dir_path
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='make csv file for training and validation dataset')
    
    
    parser.add_argument('--vid_path', metavar='path', required=True,
                        help='the parent path of trimmed ..')
    
    parser.add_argument('--out_path', metavar='path', required=True,
                        help='the path of csv files to be saved ..')
    
    parser.add_argument('--view', required=True, type=int,
                        help='the needed video view 1 for dashboard, 2 for right-side and 3 for rear view ..')
     
    args = parser.parse_args()
    
    vid_path = args.vid_path
    out_path = args.out_path
    view = args.view
    
    
    val_ids = ["30932", "60768", "61962", "83756", "96269"]
    views = ['Dashboard', 'Right', 'Rearview']
    view = views[view-1]
    out_path = make_dir(out_path, "data")
    out_path = make_dir(out_path, view)
    
    
    all_vids = glob.glob(f'{vid_path}\*\{view}*\*\*.mp4')
    df_train, df_val = make_csv_file(all_vids, val_ids)
    
    
    
    df_train.to_csv(out_path + "/train.csv", index=False, header = False)
    df_val.to_csv(out_path + "/val.csv", index=False, header = False)

    