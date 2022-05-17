import sys
import json
import argparse
import random
import csv
import numpy as np
from scipy.signal import argrelextrema
from pandas import read_csv


argument_parser = argparse.ArgumentParser(description="A script used to replay the game session.")

# participants-path = .../toadstool/participants
# groundtruth-path = .../GroundTruth
argument_parser.add_argument("-p", "--participants-path", type=str, default=None)
argument_parser.add_argument("-i", "--participant-idx", type=str, default=None)
argument_parser.add_argument("-g", "--groundtruth-path", type=str, default=None)
argument_parser.add_argument("-o", "--output-path", type=str, default= None)


def read_file(file_path, type):
    if type == "csv":
        data = read_csv(file_path)
        return data.values
    elif type == "json":
        f = open(file_path)
        data = json.load(f)
        return data


if __name__ == "__main__":
    # parser
    args = argument_parser.parse_args()
    participants_path = args.participants_path
    participant_idx = args.participant_idx
    groundtruth_path = args.groundtruth_path
    output_path = f'{args.output_path}/participant_{args.participant_idx}_events.csv'
    

    
    random_para = 10
    # file path
    session_path = f'{participants_path}/participant_{participant_idx}/participant_{participant_idx}_session.json'
    bvp_path = f'{participants_path}/participant_{participant_idx}/participant_{participant_idx}_sensor/BVP.csv'
    acc_path = f'{participants_path}/participant_{participant_idx}/participant_{participant_idx}_sensor/ACC.csv'
    eda_path = f'{participants_path}/participant_{participant_idx}/participant_{participant_idx}_sensor/EDA.csv'
    hr_path = f'{participants_path}/participant_{participant_idx}/participant_{participant_idx}_sensor/HR.csv'
    ibi_path = f'{participants_path}/participant_{participant_idx}/participant_{participant_idx}_sensor/IBI.csv'
    temp_path = f'{participants_path}/participant_{participant_idx}_sensor/TEMP.csv'
    gt_path = f'{groundtruth_path}/participant_{participant_idx}/participant_{participant_idx}_events.json'
    

    # event we have
    event = {0:"new_stage", 1:"flag_reached", 2:"status_up", 3:"stauts_down", 4:"life_lost"}

    # game frame number
    game = read_file(session_path, "json")
    game_len = int(game["obs_n"])
        
    
    
    # read data
    bvp = read_file(bvp_path, "csv")
    

    # find local maxima index
    local_max_idx = argrelextrema(bvp, np.greater)

    result = []
    for i in local_max_idx[0]:
        event_idx = random.randint(0, random_para)
        if event_idx < len(event):
            event_name = event[event_idx]
            frame_number = i
            row = [frame_number, event_name]
            result.append(row)

    # write output
    with open(output_path, 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        writer.writerows(result)
