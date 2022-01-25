import pickle as pk
import time
import os

'''
This file defines some utility functions for opening and saving a pickle file.
'''


def open_pkl_file(directory, file_name):
    path = os.path.join(directory, '{}.pkl'.format(file_name))
    if not os.path.exists(path):
        print(path)
        return False
    with open(path, 'rb') as f:
        while 1:
            try:
                file = pk.load(f)
                break
            except AttributeError:
                time.sleep(1)
                print('successfully dealt with file opening AttributeError')
        return file


# def open_pkl_file(file_name):
#     return open_pkl_file('./', file_name)


def save_pkl_file(directory, file_name, file):
    path = os.path.join(directory, '{}.pkl'.format(file_name))
    with open(path, 'wb') as f:
        while 1:
            try:
                pk.dump(file, f)
                break
            except AttributeError:
                time.sleep(1)
                print('successfully dealt with file writing AttributeError')


# def save_pkl_file(file_name, file):
#     save_pkl_file('./', file_name, file)
