"""
This script records the publication year and references of each paper.
"""

import sys
sys.path.append('..')
from utils.directories import *
from utils.pkl_io import save_pkl_file, open_pkl_file
import time
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--fos', default='physics', type=str, choices=('physics', 'cs', 'sociology', 'math'),
                      help='field of study')
    args = parser.parse_args()
    print(args.fos)
    directories = Directory(args.fos)
    directories.refresh()


    paperId_year = {}
    paperId_references = {}

    num = 0
    for filename in os.listdir(directories.directory_mag_data):
        paper_entities = open_pkl_file(directories.directory_mag_data, filename[0:-4])
        for paper_entity in paper_entities:
            num += 1
            if num % 1000 == 0:
                print(num, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            paperId = paper_entity['Id']
            year = paper_entity['Y']
            references = paper_entity['RId'] if 'RId' in paper_entity else []
            paperId_year[paperId] = year
            paperId_references[paperId] = references

    save_pkl_file(directories.directory_dataset_description, 'paperId_year', paperId_year)
    save_pkl_file(directories.directory_dataset_description, 'paperId_references', paperId_references)
