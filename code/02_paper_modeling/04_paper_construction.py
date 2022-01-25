"""
This script creates paper class from the paper entity.
"""

import sys
sys.path.append('..')
from utils.entity_io import save_paper, open_pkl_file
from utils.directories import *
from entities.paper import *
from entities.author import *
import time
import argparse


def read_paper(paper_file, citations, field_of_study):
    paperId = paper_file['Id']
    title = paper_file['Ti']
    year = int(paper_file['Y'])
    date = paper_file['D']
    references = paper_file['RId'] if 'RId' in paper_file else []

    authors = []
    for author in paper_file['AA']:
        authors.append(Author(author_name=author['DAuN'],
                              authorId=author['AuId'],
                              aff_name=author['DAfN'],
                              affId=author['AfId']))

    paper = Paper(paperId=paperId,
                  title=title,
                  authors=authors,
                  year=year,
                  date=date,
                  references=references,
                  citations=citations
                  )
    save_paper(paperId, paper, field_of_study)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--fos', default='physics', type=str, choices=('physics', 'cs', 'sociology', 'math'),
                      help='field of study')
    args = parser.parse_args()
    print(args.fos)
    directories = Directory(args.fos)
    directories.refresh()


    paperIds = open_pkl_file(directories.directory_dataset_description, 'paperIds')
    cited_paper_citing_papers = open_pkl_file(directories.directory_dataset_description, 'cited_paper_citing_papers')
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
            citations = len(cited_paper_citing_papers[paperId]) if paperId in cited_paper_citing_papers else 0
            read_paper(paper_entity, citations, args.fos)
