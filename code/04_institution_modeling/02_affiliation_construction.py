"""
This script constructs affiliation in the form of pre-defined affiliation class
"""

import sys
sys.path.append('..')
from utils.entity_io import open_paper, save_affiliation, open_pkl_file, save_pkl_file
from entities.affiliation import Affiliation
from utils.directories import *
import time
import math
import threading
import argparse


# add multiple papers to an affiliation
def construct_affiliations_from_papers(paperIds, affId, field_of_study):
    aff_name = ''
    paper0 = open_paper(paperIds[0], field_of_study)
    for author in paper0.authors:
        if author.affId == affId:
            aff_name = author.aff_name
            break

    affiliation = Affiliation(affId, aff_name)

    for paperId in paperIds:
        paper = open_paper(paperId, field_of_study)
        year = paper.year
        authors = paper.authors
        contribution = paper.aff_contribution[affId]
        citations = paper.citations

        authorIds = set()
        internal_authorIds = set()
        external_authorIds = set()
        external_affIds = set()

        authorId_affId = []

        for author in authors:
            authorIds.add(author.authorId)
            authorId_affId.append((author.authorId, author.affId))
            if author.affId == affId:
                internal_authorIds.add(author.authorId)
            else:
                external_authorIds.add(author.authorId)
                external_affIds.add(author.affId)

        teamsize = len(authorIds)
        internal_teamsize = len(internal_authorIds)
        external_teamsize = len(external_authorIds)


        internal_collab = set()
        external_inst_collab = set()
        external_indiv_collab = set()
        indiv_collab = set()

        for authorId1 in internal_authorIds:
            for authorId2 in internal_authorIds:
                if authorId1 == authorId2:
                    continue
                internal_collab.add((authorId1, authorId2))
                internal_collab.add((authorId2, authorId1))
                indiv_collab.add((authorId1, authorId2))
                indiv_collab.add((authorId2, authorId1))

        for external_affId in external_affIds:
            external_inst_collab.add(external_affId)

        for internal_authorId in internal_authorIds:
            for external_authorId in external_authorIds:
                external_indiv_collab.add((internal_authorId, external_authorId))
                external_indiv_collab.add((external_authorId, internal_authorId))
                indiv_collab.add((internal_authorId, external_authorId))
                indiv_collab.add((external_authorId, internal_authorId))

        affiliation.add_paper(year=year,
                              authorIds=internal_authorIds,
                              external_authorIds=external_authorIds,
                              paperId=paperId,
                              contribution=contribution,
                              teamsize=teamsize,
                              internal_teamsize=internal_teamsize,
                              external_teamsize=external_teamsize,
                              citations=citations,
                              internal_collab=internal_collab,
                              external_inst_collab=external_inst_collab,
                              external_indiv_collab=external_indiv_collab,
                              indiv_collab=indiv_collab,
                              )

    affiliation.update_affiliation(authorId_first_year)
    save_affiliation(affId, affiliation, field_of_study)


# construct affiliations with multi-threading, n out of m threads
def construct_affiliations(affId_paperIds, affIds, m, n, field_of_study):
    affnum = len(affIds)
    length = math.ceil(affnum / m)
    start = (n - 1) * length
    end = min(n * length - 1, affnum-1)

    _affIds = affIds[start:end+1]
    num = 0
    for affId in _affIds:
        num += 1
        if num % 100 == 0:
            print(n, ',', num, '/', length, ',', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        paperIds = affId_paperIds[affId]
        construct_affiliations_from_papers(paperIds, affId, field_of_study)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--fos', default='physics', type=str, choices=('physics', 'cs', 'sociology', 'math'),
                      help='field of study')
    args = parser.parse_args()
    print(args.fos)
    directories = Directory(args.fos)
    directories.refresh()

    affId_paperIds = open_pkl_file(directories.directory_dataset_description, 'affId_paperIds')
    affIds = list(affId_paperIds.keys())
    print(len(affIds))
    threads = []
    thread_num = 20

    authorId_first_year = open_pkl_file(directories.directory_dataset_description, 'authorId_first_year')

    for i in range(thread_num):
        threads.append(threading.Thread(target=construct_affiliations, args=(affId_paperIds, affIds, thread_num, i+1, args.fos)))
    for t in threads:
        t.setDaemon(True)
        t.start()
    for t in threads:
        t.join()
