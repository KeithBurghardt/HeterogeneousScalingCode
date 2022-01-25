import sys
sys.path.append('..')
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

    year_affIds = open_pkl_file(directories.directory_data, 'year_affIds')
    years = list(year_affIds.keys())
    years.sort()

    year_cul_affIds = {}
    year_cul_affIds[years[0]] = year_affIds[years[0]]
    for i in range(len(years)-1):
        year_cul_affIds[years[i+1]] = year_cul_affIds[years[i]].union(year_affIds[years[i+1]])

    save_pkl_file(directories.directory_data, 'year_cul_affIds', year_cul_affIds)
