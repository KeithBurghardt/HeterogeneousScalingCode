import sys
sys.path.append('..')
from utils.entity_io import open_affiliation, open_pkl_file
from utils.directories import *
import pandas as pd
import tarfile
import argparse


def make_targz(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--fos', default='physics', type=str, choices=('physics', 'cs', 'sociology', 'math'),
                        help='field of study')
    args = parser.parse_args()
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
        for year in years:
            size = affiliation.year_size[year]
            internal_collab = affiliation.year_internal_collab[year]
            external_collab = affiliation.year_external_indiv_collab[year]
            production = affiliation.year_production[year]
            productivity = affiliation.year_productivity[year]
            avg_impact = affiliation.year_avg_impact[year] if year in affiliation.year_avg_impact else 0
            avg_impact_oneauthor = affiliation.year_avg_impact_oneauthor[year] if year in affiliation.year_avg_impact_oneauthor else 0
            avg_impact_twoauthor = affiliation.year_avg_impact_twoauthor[year] if year in affiliation.year_avg_impact_twoauthor else 0
            avg_impact_three2sixauthor = affiliation.year_avg_impact_three2sixauthor[year] if year in affiliation.year_avg_impact_three2sixauthor else 0
            avg_teamsize = affiliation.year_avg_teamsize[year]
            avg_internal_teamsize = affiliation.year_avg_internal_teamsize[year]
            cumul_size = affiliation.year_cumul_size[year]
            cumul_internal_collab = affiliation.year_cumul_internal_collab[year]
            cumul_external_indiv_collab = affiliation.year_cumul_external_indiv_collab[year]
            cumul_production = affiliation.year_cumul_production[year]
            cumul_productivity = affiliation.year_cumul_productivity[year]
            seniority_5 = affiliation.year_authorIds_5[year] if year in affiliation.year_authorIds_5 else 0
            seniority_10 = affiliation.year_authorIds_10[year] if year in affiliation.year_authorIds_10 else 0
            seniority_15 = affiliation.year_authorIds_15[year] if year in affiliation.year_authorIds_15 else 0
            seniority_20 = affiliation.year_authorIds_20[year] if year in affiliation.year_authorIds_20 else 0
            data.append([year, size, internal_collab, external_collab, production, productivity,
                         avg_impact, avg_impact_oneauthor, avg_impact_twoauthor, avg_impact_three2sixauthor,
                         avg_teamsize, avg_internal_teamsize,
                         cumul_size, cumul_internal_collab, cumul_external_indiv_collab,
                         cumul_production, cumul_productivity,
                         seniority_5, seniority_10,
                         seniority_15, seniority_20])
        df = pd.DataFrame(data, columns=['year', 'size', '#internal_collab', '#external_collab', 'production', 'productivity',
                                         'avg_impact', 'avg_impact_oneauthor', 'avg_impact_twoauthor', 'avg_impact_three2sixauthor',
                                         'teamsize', 'internal_teamsize',
                                         'cumul_size', '#cumul_internal_collab', '#cumul_external_collab',
                                         'cumul_production', 'cumul_productivity',
                                         'seniority_5', 'seniority_10',
                                         'seniority_15', 'seniority_20'])
        path = os.path.join(directories.directory_institution_description, '{}.csv'.format(affId))
        df.to_csv(path, index=False)

    directories.refresh()
    make_targz(os.path.join(directories.directory_dataset_description, 'institution_description.tar.gz'),
               directories.directory_institution_description)