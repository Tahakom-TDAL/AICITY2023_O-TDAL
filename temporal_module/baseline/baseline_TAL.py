#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 07:07:49 2023

@author: Taghreed
"""
import argparse 
import os
import csv
from glob import glob
import numpy as np
from tqdm import tqdm


vid_name_mapping = {}
is_vid_mapping = True



def get_vid_mapping(vid_ids):
   # global vid_ids
    global vid_name_mapping
    
    reader = csv.reader(open(vid_ids, 'r'))
    ignore_header = True
    for row in reader:
        if ignore_header:
            ignore_header = False
            continue
        video_id1, dashboard, rear, right = row
        video_id2 = rear[:-4].split('_')[-3] + '_' + rear[:-4].split('_')[-1]
        vid_name_mapping[video_id1] = video_id2  
        vid_name_mapping[video_id2] = video_id1         



def get_classes_dict():
    return {'1': [], '2': [], '3': [], '4': [], 
            '5': [], '6': [], '7': [], '8': [], 
            '7': [], '9': [], '10': [], '11': [], 
            '12': [], '13': [], '14': [], '15': []}
 
           

def get_vid_dict(vid_path):
    vids = glob(f'{vid_path}/*/Re*.MP4' )  
    vids_dict = {}
    for i in vids:
        vid_name = i.split(os.sep)[-1].split('.')[0]
        vid_id = vid_name.split('_')[-3] +'_'+ vid_name.split('_')[-1]
        vids_dict[vid_id] = get_classes_dict()
       
    return vids_dict 
   


def get_prob_files(prob_path):
    prob_files = {}
    for k in prob_path:
        vid_base_name = os.path.basename(k) 
        vid_name = vid_base_name.split('_')[-3]+'_'+vid_base_name.split('_')[-1]
        prob_files[vid_name] = glob(k+'/P_*')
        
    return prob_files



def get_classess_prob(prob_files):
    prob_files.sort()

    clip_num = []
    classes_prob = { '0': [], '1': [], '2': [], '3': [],
                 '4': [], '5': [], '6': [], '7': [],
                 '8': [], '9': [], '10': [], '11': [],
                 '12': [], '13': [], '14': [], '15': []}
   
        
    for npz_file in prob_files:
        file_name = os.path.basename(npz_file)[:-4]
        file_name = int(file_name[2:])
        clip_num.append(file_name)
        prob = np.load(npz_file)
        prob = prob['arr_0']
        counter = 0
        for num in classes_prob:
            classes_prob[num].append({'clip_num': file_name, 'prob':prob[0][counter]})
            counter += 1
    return classes_prob



def get_top_k_peaks(classes_prob, action, topk):
    classes_prob = classes_prob[action]
    
    top_class_prob = sorted(classes_prob, key=lambda d: d['prob'], )[-topk:]
           
    return top_class_prob



def get_action_time(rear_class_prob, right_class_prob, action):
    
    # rear_class_prob = rear_top_class_prob
    # right_class_prob = right_top_class_prob 
    
    rear_clip_num = [d['clip_num'] for d in rear_class_prob]
    rear_class_prob = [d['prob'] for d in rear_class_prob]
    
    right_clip_num = [d['clip_num'] for d in right_class_prob]
    right_class_prob = [d['prob'] for d in right_class_prob]
    
    if action == '13':
               
        peak_time_info = {'rear_peak_rank': 1, 'right_peak_clip_num': rear_clip_num[-1], 
                          'rear_peak_prob': rear_class_prob[-1], 'right_peak_rank': 1,
                          'rear_peak_clip_num' : rear_clip_num[-1], 'right_peak_prob': rear_class_prob[-1]}
            
        return peak_time_info
    
    
    peak_time_info = [-1] 
    
    for j in range(len(rear_clip_num)):
        for k in range(len(right_clip_num)):
            
            rear_peak_rank = len(rear_clip_num) - j 
            rear_time_prob = rear_class_prob[j] 

            
            right_peak_rank = len(right_clip_num) - k
            right_time_prob = right_class_prob[k]
            
            if right_clip_num[k] == rear_clip_num[j]:
                peak_time_info = {'rear_peak_rank': rear_peak_rank, 'right_peak_clip_num': right_clip_num[k], 
                                  'rear_peak_prob': rear_time_prob, 'right_peak_rank': right_peak_rank,
                                  'rear_peak_clip_num' : rear_clip_num[j], 'right_peak_prob': right_time_prob}
                 

                break
            elif (right_clip_num[k] + 2 == rear_clip_num[j]) or \
                  (right_clip_num[k] == rear_clip_num[j] + 2):
                
                  peak_time_info = {'rear_peak_rank': rear_peak_rank, 'right_peak_clip_num': right_clip_num[k], 
                                    'rear_peak_prob': rear_time_prob, 'right_peak_rank': right_peak_rank,
                                    'rear_peak_clip_num' : rear_clip_num[j], 'right_peak_prob': right_time_prob}
                  
    return peak_time_info



def get_start_end_time(classess_prob, peak_clip_num, action):

    # classess_prob = rear_classess_prob
    # peak_clip_num = rear_peak_clip
    
    # classess_prob = right_classess_prob
    # peak_clip_num = right_peak_clip

    wnd = 15
    peak_ind = [i for i in range(len(classess_prob[action])) if classess_prob[action][i]['clip_num'] == peak_clip_num][0]

    peak_prob = classess_prob[action][peak_ind]['prob']

    bef_clip_prob = classess_prob[action][peak_ind-min(wnd,peak_ind):peak_ind+1]                             
    aft_clip_prob = classess_prob[action][peak_ind:peak_ind+wnd]
    
    peak_clip_prob  = bef_clip_prob + aft_clip_prob
    
    
    
    cand_start = [j for j in range(len(bef_clip_prob)) if (bef_clip_prob[j]['prob'] < peak_prob * 0.60) ]
    if len(cand_start) != 0:
        if len(cand_start) != 1 and  cand_start[-2] <= cand_start[-1] - 3:
            start = cand_start[-2] + 1
        else: 
            start = cand_start[-1] 
    else:   
        start = 0

   
    cand_end = [j for j in range(len(aft_clip_prob)) if (aft_clip_prob[j]['prob'] <  peak_prob * 0.60) ]
    if len(cand_end) !=0:

        if len(cand_end) != 1 and  cand_end[1] >= cand_end[0] + 3:
            end = cand_end[1] - 1 
        else: 
            end = cand_end[0] - 1
    else :    
        end = -1
        
        
    interval = [bef_clip_prob[start]['clip_num'], aft_clip_prob[end]['clip_num']]
    
    return interval, peak_clip_prob



def write_txt_file(vid_peaks_info, out_file):
    
    if not os.path.exists(os.path.dirname(out_file)):
        os.makedirs(os.path.dirname(out_file))
    with open (out_file, "a") as file:
        for vid in vid_peaks_info:
            for action in vid_peaks_info[vid]:
                if vid_peaks_info[vid][action] == [-1] :
                    continue

                file.write("%s " % vid_name_mapping[vid] )
                file.write("%s " % action )
                if action == '13' or action == '4':
                    file.write("%s " % str(vid_peaks_info[vid][action]['ps, pe'][0] * 2 +1 ) )
                else: 
                    file.write("%s " % str(vid_peaks_info[vid][action]['ps, pe'][0] * 2 ) )

                
                if action == '13':
                    file.write("%s \n" % str(vid_peaks_info[vid][action]['ps, pe'][1] * 2 +1))
                else:
                    file.write("%s \n" % str(vid_peaks_info[vid][action]['ps, pe'][1] * 2 ))

    

def main(vid_path, vid_ids, probabilities_path, out_file):
    
    topk = 7
    vid_peaks_info = get_vid_dict(vid_path)

    right_prob_files = get_prob_files(glob(probabilities_path+'/Right_features_and_probability_t1/*'))
    rear_prob_files = get_prob_files(glob(probabilities_path+'/Rear_features_and_probability_t1/*'))
    


    for vid in tqdm(vid_peaks_info):      
        
        for action in vid_peaks_info[vid]:
           
            
            right_classess_prob = get_classess_prob(right_prob_files[vid])
            rear_classess_prob= get_classess_prob(rear_prob_files[vid])

            
            right_top_class_prob = get_top_k_peaks(right_classess_prob, action, topk)
            rear_top_class_prob = get_top_k_peaks(rear_classess_prob, action, topk)
            
            
            vid_peaks_info[vid][action] = get_action_time(rear_top_class_prob, right_top_class_prob, action)
            
            if vid_peaks_info[vid][action] == [-1]:
                continue
            
            
            right_peak_clip = vid_peaks_info[vid][action]['right_peak_clip_num']
            rear_peak_clip = vid_peaks_info[vid][action]['rear_peak_clip_num']

            right_interval, right_peak_clip_prob = get_start_end_time(right_classess_prob, right_peak_clip, action)
            rear_interval, rear_peak_clip_prob = get_start_end_time(rear_classess_prob, rear_peak_clip, action)
            vid_peaks_info[vid][action]['ps, pe'] = [min(right_interval[0], rear_interval[0]), \
                                                     max(right_interval[1], rear_interval[1])]
           
    
    get_vid_mapping(vid_ids)
    write_txt_file(vid_peaks_info, out_file)



if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='get temporal localization by baseline method')
    
    
    parser.add_argument('--vid_path', metavar='path', required=True,
                        help='the parent path where the videos are in ..')
    
    parser.add_argument('--vid_ids', metavar='path', required=True,
                        help='the path for csv file where vidoes mapping are saved ..')
    
    parser.add_argument('--probabilities_path', metavar='path', required=True,
                        help='the parent path of probabilities of videos segments ..')
    

    args = parser.parse_args()
    # vid_path = args.vid_path
    # vid_path = r'G:\7th_AI_City_Challange\Dataset\A2\Data_reference\IDs' 
    # vid_ids = r'G:/7th_AI_City_Challange/scripts/video_ids.csv' 
    # probabilities_path = r'G:\7th_AI_City_Challange\Inferences\A2\feat_prob' 
    # out_file = r'G:\7th_AI_City_Challange\github\temporal_module\baseline'+os.sep+'baseline_temp_out.txt'
    
    # main(vid_path, vid_ids, probabilities_path, out_file)
    main(args.vid_path, args.vid_ids, args.probabilities_path, os.getcwd()+os.sep+'temporal_out'+os.sep+'baseline_temp_out.txt')

    
    
    