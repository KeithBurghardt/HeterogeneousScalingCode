"""
This script records the affiliation and its published papers
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
    affId_paperIds = {}
    num = 0
    for paperId in paperIds:
        paper = open_paper(paperId, args.fos)
        num += 1
        if num % 1000 == 0:
            print(num, '/', len(paperIds), ',', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        authorIds = set()
        for author in paper.authors:
            authorId = author.authorId
            if authorId in authorIds:
                continue
            authorIds.add(authorId)
            affId = author.affId
            if affId not in affId_paperIds:
                affId_paperIds[affId] = []
            affId_paperIds[affId].append(paperId)

    save_pkl_file(directories.directory_dataset_description, 'affId_paperIds', affId_paperIds)
    save_pkl_file(directories.directory_dataset_description, 'affIds', list(affId_paperIds.keys()))
