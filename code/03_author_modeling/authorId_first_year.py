"""
This script records each author and the first year the author appeared
"""

import sys
sys.path.append('..')
from utils.pkl_io import save_pkl_file, open_pkl_file
from utils.entity_io import open_paper
from utils.directories import *
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


    paperIds = open_pkl_file(directories.directory_dataset_description, 'paperIds')
    authorId_first_year = {}
    num = 0
    for paperId in paperIds:
        paper = open_paper(paperId, args.fos)
        num += 1
        if num % 1000 == 0:
            print(num, '/', len(paperIds), ',', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        year = paper.year
        for author in paper.authors:
            authorId = author.authorId
            if authorId not in authorId_first_year:
                authorId_first_year[authorId] = year
            else:
                authorId_first_year[authorId] = min(authorId_first_year[authorId], year)

    save_pkl_file(directories.directory_dataset_description, 'authorId_first_year', authorId_first_year)
