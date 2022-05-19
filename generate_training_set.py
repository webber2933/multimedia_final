import sys
import json
import argparse
import random
import csv
import numpy as np
from scipy.signal import argrelextrema
from pandas import read_csv
import shutil
import os.path

file_path = f'GroundTruth/participant_9_events.json'

f = open(file_path)
data = json.load(f)

for i in data:
    frame_num = i['frame_number']
    classes = i['event']
    source = f'toadstool/toadstool/participants/participant_9/gameframe/game_{frame_num}.png'
    des = f'training set/{classes}/game_{frame_num}_9.png'

    if os.path.isfile(source):
        shutil.copyfile(source,des)