from utils.pkl_io import *
from utils.directories import *


# open a paper entity
def open_paper(paperId, field_of_study):
    directories = Directory(field_of_study)
    paper = open_pkl_file(directories.directory_papers, paperId)
    return paper


# save a paper entity
def save_paper(paperId, paper, field_of_study):
    directories = Directory(field_of_study)
    save_pkl_file(directories.directory_papers, paperId, paper)


# open an affiliation entity
def open_affiliation(affId, field_of_study):
    directories = Directory(field_of_study)
    affiliation = open_pkl_file(directories.directory_institutions, affId)
    return affiliation


# save an affiliation entity
def save_affiliation(affId, affiliation, field_of_study):
    directories = Directory(field_of_study)
    save_pkl_file(directories.directory_institutions, affId, affiliation)
