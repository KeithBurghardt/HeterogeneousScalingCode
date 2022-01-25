import sys
sys.path.append('..')
from utils.pkl_io import open_pkl_file, save_pkl_file
from utils.directories import *
from utils.entity_io import open_affiliation
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--fos', default='physics', type=str, choices=('physics', 'cs', 'sociology', 'math'),
                      help='field of study')
    args = parser.parse_args()
    print(args.fos)
    directories = Directory(args.fos)
    directories.refresh()


    affIds = open_pkl_file(directories.directory_data, 'affiliations').affIds
    year_affIds = {}

    for affId in affIds:
        affiliation = open_affiliation(affId)
        year_sizes = affiliation.year_size
        for year in year_sizes:
            if year not in year_affIds:
                year_affIds[year] = set()
            year_affIds[year].add(affId)

    save_pkl_file(directories.directory_data, 'year_affIds', year_affIds)
