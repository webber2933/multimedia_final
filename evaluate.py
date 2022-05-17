from email import header
import json
import argparse
import pandas as pd
import numpy as np
import csv

argument_parser = argparse.ArgumentParser(
    description="The evaluation script for the Emotional Mario Task at MediaEval 2021")

argument_parser.add_argument("-i", "--run-path", type=str, default=None)
argument_parser.add_argument("-t", "--truth-path", type=str, default=None)
argument_parser.add_argument("-n", "--video-no", type=int, nargs='+', default=None)


def evaluate(run, truth, df, runid="undefined", filename="undefined", max_distance=25):
    # compare everyone with everything ...

    # for all events in the run data:
    matches = []
    cumulative_distance = 0
    for truth_evt in truth:
        # find the closest event in the truth data:
        curr_dist = max_distance
        curr_run_evt = None
        for run_evt in run:
            distance = abs(truth_evt['frame_number'] - run_evt['frame_number'])
            if abs(truth_evt['frame_number'] - run_evt['frame_number']) < curr_dist:  # use this line for just matching an arbitrary event
                if abs(truth_evt['frame_number'] - run_evt['frame_number']) < curr_dist and truth_evt['event'] == run_evt['event']:  # use this line for exact matches
                    curr_run_evt = truth_evt
                    curr_dist = distance
        if curr_run_evt is not None:  # add it to the list if it is considered a find
            matches.append([truth_evt, curr_run_evt])
            cumulative_distance += curr_dist  # sum them up for the avg. distance

    # print(len(matches))
    # get all the numbers ...
    precision = len(matches) / len(run)
    recall = len(matches) / len(truth)
    if len(matches) > 0:
        avg_distance = cumulative_distance / len(matches)
    else:
        avg_distance = -1
    # print("%s, %s, %d, %d, %d, %0.4f, %0.4f, %0.4f, %0.4f"%(runid, filename, len(run), len(truth), len(matches), avg_distance, precision, recall, 2*(precision*recall)/(precision+recall)))
    f1 = 0
    if recall + precision > 0:
        f1 = 2 * (precision * recall) / (precision + recall)
    df.loc[-1] = [runid, filename, len(run), len(truth), len(matches), avg_distance, precision, recall, f1]
    df.index = df.index + 1  # shifting index
    df.sort_index()  # sorting by index

def load_run_csv(file):
    datas = []  
    with open(file) as f:
     
        csvReader = csv.reader(f, delimiter=',')
        # Convert each row into a dictionary
        # and add it to data
        for rows in csvReader:
            data = {}
            # Assuming a column named 'No' to
            # be the primary key
            # key = rows['frame_number']
            data["frame_number"] = int(rows[0])
            data["event"] = rows[1]
            datas.append(data)
    return json.dumps(datas)
if __name__ == '__main__':
    args = argument_parser.parse_args()

    run_path = args.run_path
    truth_path = args.truth_path
    video_no = args.video_no
    print(video_no)
    df = pd.DataFrame(columns="run identifier, file, events in run, events in truth, number of matches, avg. distance, precision, recall, f1 score".split(sep=", "))
    my_max_distance = 25
    
    for i in video_no:
        file_name = f'participant_{i}_events'
        tmp = f'{file_name}.csv'
        run = json.loads(load_run_csv(run_path+tmp))
        tmp = f'{file_name}.json'
        f2 = open(truth_path+tmp)
        truth = json.load(f2)

        evaluate(run, truth, df, tmp, tmp, max_distance=my_max_distance)

    grouped = df.groupby('run identifier')
    mp = grouped['precision'].agg(np.mean)
    mr = grouped['recall'].agg(np.mean)
    t1 = pd.DataFrame([mp, mr])
    evaluation = t1.T.assign(f1=lambda x: 2 * x['precision'] * x['recall'] / (x['precision'] + x['recall']))  # computing the f1 score from the averaged values.
    # print results
    print(df.sort_values('run identifier').to_csv())
    print(evaluation.to_csv())
    # write results to file
    file_header = 'team_random'
    df.sort_values('run identifier').to_csv('%s_detailed_%s_frames.csv' % ((file_header, my_max_distance)), index=None)
    evaluation.to_csv('%s_overall_%s_frames.csv' % ((file_header, my_max_distance)))