"""
The script constructs the citation network among papers.
"""

import sys
sys.path.append('..')
import time
from utils.pkl_io import open_pkl_file, save_pkl_file
from utils.directories import *
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--fos', default='physics', type=str, choices=('physics', 'cs', 'sociology', 'math'),
                      help='field of study')
    args = parser.parse_args()
    print(args.fos)
    directories = Directory(args.fos)
    directories.refresh()


    paperId_year = open_pkl_file(directories.directory_dataset_description, 'paperId_year')
    paperId_references = open_pkl_file(directories.directory_dataset_description, 'paperId_references')
    paperIds = open_pkl_file(directories.directory_dataset_description, 'paperIds')

    num = 0
    cited_paper_citing_papers = {}
    for citing_paperId in paperIds:
        num += 1
        if num % 1000 == 0:
            print(num, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        cited_paperIds = paperId_references[citing_paperId]
        for cited_paperId in cited_paperIds:
            if cited_paperId not in paperId_year:
                continue
            if paperId_year[citing_paperId] - paperId_year[cited_paperId] > 10:
                continue
            if cited_paperId not in cited_paper_citing_papers:
                cited_paper_citing_papers[cited_paperId] = set()
            cited_paper_citing_papers[cited_paperId].add(citing_paperId)

    save_pkl_file(directories.directory_dataset_description, 'cited_paper_citing_papers', cited_paper_citing_papers)
