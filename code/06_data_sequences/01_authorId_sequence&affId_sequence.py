"""
This script creates authorId sequence and affiliation sequence ordered by date.
"""
import sys
sys.path.append('..')
from utils.directories import *
from utils.pkl_io import open_pkl_file, save_pkl_file
import time
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--fos', default='physics', type=str, choices=('physics', 'cs', 'sociology', 'math'),
                        help='field of study')
    args = parser.parse_args()
    print(args.fos)
    directories = Directory(args.fos)

    paperIds = open_pkl_file(directories.directory_dataset_description, 'paperIds')
    authorId_sequence = []  # (authorId, date)
    affId_sequence = []  # (affId, date)

    num = 0
    for filename in os.listdir(directories.directory_mag_data):
        paper_entities = open_pkl_file(directories.directory_mag_data, filename[0:-4])
        for paper_entity in paper_entities:
            num += 1
            if num % 1000 == 0:
                print(num, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            paperId = paper_entity['Id']
            if paperId not in paperIds:
                continue
            date = paper_entity['D']
            authors = paper_entity['AA']
            authorIds = set()
            for author in authors:
                authorId = author['AuId']
                if authorId in authorIds:
                    continue
                authorIds.add(authorId)
                affId = author['AfId']
                authorId_sequence.append((authorId, date))
                affId_sequence.append((affId, date))

    authorId_sequence.sort(key=lambda t: t[1])
    affId_sequence.sort(key=lambda t: t[1])

    save_pkl_file(directories.directory_urn_model, 'ordered_authorId_sequence', authorId_sequence)
    save_pkl_file(directories.directory_urn_model, 'ordered_affId_sequence', affId_sequence)

