import sys
sys.path.append('..')
from utils.entity_io import open_affiliation, open_pkl_file
from utils.directories import *
import pandas as pd
import numpy as np
import argparse
import tarfile


def make_targz(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--fos', default='physics', type=str, choices=('physics', 'cs', 'sociology', 'math'),
                      help='field of study')
    args = parser.parse_args()
    print(args.fos)
    directories = Directory(args.fos)
    directories.refresh()

    affIds = open_pkl_file(directories.directory_dataset_description, 'affIds')
    length = len(affIds)
    num = 0
    for affId in affIds:
        num += 1
        print('{}/{}'.format(num, length))
        data = []
        affiliation = open_affiliation(affId, args.fos)
        years = list(affiliation.year_size.keys())
        years.sort(reverse=True)
        year_authorIds = affiliation.year_authorIds
        for year in years:
            authorId_paperIds = affiliation.year_authorId_paperIds[year]
            for authorId in authorId_paperIds:
                internal_collab = affiliation.year_authorId_internal_collab[year][authorId]
                external_collab = affiliation.year_authorId_external_collab[year][authorId]
                indiv_collab = affiliation.year_authorId_indiv_collab[year][authorId]
                avg_teamsize = affiliation.year_authorId_avg_teamsize[year][authorId]
                avg_impact = affiliation.year_authorId_avg_impact[year][authorId]
                if year in affiliation.year_authorId_avg_impact_oneauthor and authorId in affiliation.year_authorId_avg_impact_oneauthor[year]:
                    avg_impact_oneauthor = affiliation.year_authorId_avg_impact_oneauthor[year][authorId]
                else:
                    avg_impact_oneauthor = None
                data.append([year, authorId, internal_collab, external_collab, indiv_collab, avg_teamsize, avg_impact, avg_impact_oneauthor])
        df = pd.DataFrame(data, columns=['year', 'authorId',
                                         '#internal_collab',
                                         '#external_collab',
                                         '#indiv_collab',
                                         'avg_teamsize',
                                         'avg_impact',
                                         'avg_impact_oneauthor'
                                         ])
        path = os.path.join(directories.directory_author_collab, '{}.csv'.format(affId))
        df.to_csv(path, index=False)

    directories.refresh()
    make_targz(os.path.join(directories.directory_dataset_description, 'author_collab.tar.gz'),
               directories.directory_author_collab)
