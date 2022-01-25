"""
This script calculates the number of papers in each year
by calling calHistogram method of MAKES and saves the result.
"""

import sys
sys.path.append('..')
from utils.microsoft_academic_makes import calcHistogram
from utils.pkl_io import *
from utils.excel_io import *
from utils.directories import *
import argparse
import pandas as pd

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--fos', default='physics', type=str, choices=('physics', 'cs', 'sociology', 'math'),
                      help='field of study')
    args = parser.parse_args()
    print(args.fos)
    directories = Directory(args.fos)
    directories.refresh()

    year_papernum = {}
    year_papernum_data = []
    start_year = 1800
    end_year = 2018

    for year in range(end_year, start_year-1, -1):
        papernum = calcHistogram(directories.field_of_study.replace('_', ' '), year)
        if papernum == 0:
            continue
        year_papernum[year] = papernum
        year_papernum_data.append([year, papernum])
        print(year, papernum)

    save_pkl_file(directories.directory_dataset_description, 'year_papernum', year_papernum)
    pd.DataFrame(year_papernum_data).to_csv(
        os.path.join(directories.directory_dataset_description, 'year_papernum.csv'),
        columns=['year', 'num'],
        index=False)
