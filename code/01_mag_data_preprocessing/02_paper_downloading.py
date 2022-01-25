"""
This script downloads the paper entities of each year by calling the evaluate method of MAKES.
Multi-threading is used to speed up the downloading process.
"""

import sys
sys.path.append('..')
import random as rd
import math
import threading
import numpy as np
from utils.microsoft_academic_makes import *
from utils.pkl_io import open_pkl_file, save_pkl_file
from utils.directories import *
import argparse


def paper_downloading(years, groups_num, group_num, directory_mag_data, field_of_study):

    length = math.ceil(len(years) / groups_num)
    start = (group_num - 1) * length
    end = min(group_num * length - 1, len(years)-1)

    for i in range(start, end+1):
        year = years[i]
        count = year_num[year]
        offsets = np.arange(0, count, step)
        for offset in offsets:
            if os.path.exists(os.path.join(directory_mag_data, 'paper_entities_{}_{}.pkl'.format(year, offset))):
                print('paper_entities_{}_{}'.format(year, offset), 'already exists')
                continue
            paper_entities = evaluate(field_of_study.replace('_', ' '), year, count, offset)
            if not paper_entities:
                continue
            save_pkl_file(directory_mag_data, 'paper_entities_{}_{}'.format(year, offset), paper_entities)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--fos', default='physics', type=str, choices=('physics', 'cs', 'sociology', 'math'),
                      help='field of study')
    args = parser.parse_args()
    print(args.fos)
    directories = Directory(args.fos)
    directories.refresh()


    year_num = open_pkl_file(directories.directory_dataset_description, 'year_papernum')
    years = list(year_num.keys())

    rd.shuffle(years)
    thread_num = 20
    threads = []

    for i in range(thread_num):
        threads.append(threading.Thread(target=paper_downloading, args=(years, thread_num, i+1,
                                                                        directories.directory_mag_data,
                                                                        directories.field_of_study)))
    for t in threads:
        t.setDaemon(True)
        t.start()
    for t in threads:
        t.join()


