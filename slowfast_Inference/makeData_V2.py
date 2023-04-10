#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  17 00:14:58 2022
@author: shahad
"""

'''

this script will generate a test.csv files for all videos segments

input: Segments_folders, path where the folders for each video segments exsits.
output: inside each video segments folder, test.csv file will be created.

'''


import glob 
import pandas as pd
import argparse 



def makeData(segments_folders):

    for segment_folder in segments_folders:

        segments = glob.glob(segment_folder+"/*.mp4")

        segments.sort()
        rows_list = []

        for segment in segments:
            rows_list.append([segment, 0])
    
        df_test = pd.DataFrame(rows_list)   
        df_test.to_csv(segment_folder+"/test.csv", index = False, header = False)



def main(segments_folders):

    makeData(glob.glob(segments_folders+"/*"))


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='video segmentation make data')
    
    parser.add_argument('--segments_folders', metavar='path',
                        help='the path to the folder that contains folders for all video segments .. ')
    
    args = parser.parse_args()
    
    main(args.segments_folders)
    