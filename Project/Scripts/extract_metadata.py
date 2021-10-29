import warnings
warnings.filterwarnings('always')
warnings.simplefilter('always')
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=DeprecationWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")
import glob, os, sys
# import matplotlib.pylab as plt
# from matplotlib import pyplot
import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None
import csv
import pickle
import math
from bs4 import BeautifulSoup
import nltk
import shutil

import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
import gensim



def save_df(df, file_name, append=False):
    if append:
        df.to_csv(file_name, index=False, quotechar='"', quoting=csv.QUOTE_NONNUMERIC, mode="a", header=False)
    else:
        df.to_csv(file_name, index=False, quotechar='"', quoting=csv.QUOTE_NONNUMERIC)


def load_obj(base_dir, name):
    file_path = os.path.join(base_dir, "pickle", name + ".pkl")
    with open(file_path, 'rb') as f:
        return pickle.load(f)

def save_obj(obj, base_dir, name):
    dir_path = os.path.join(base_dir, "pickle")
    create_director(dir_path)
    file_path = os.path.join(dir_path, name + ".pkl")
    with open(file_path, 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
    print("Saved object to a file: %s" % (str(file_path)))

def save_df(df, base_dir, file_name):
    file_name = os.path.join(base_dir, file_name)
    df.to_csv(file_name, index=False, quotechar='"', quoting=csv.QUOTE_NONNUMERIC)

def remove_directory(path):
    if os.path.exists(path):
        print("%s path exists and removing it." % path)
        shutil.rmtree(path)

def remove_file(file_name):
    if (os.path.isfile(file_name)):
        print("Output file %s exists and removing it." % file_name)
        os.remove(output_csv_file)

def create_director(dir):
    if(not os.path.exists(dir)):
        print("Creating directory %s." % dir)
        os.makedirs(dir)
    else:
        print("Directory %s already exists and so returning." % dir)



def extract_meta_data(BASE_DIR, file="Posts.csv", columns={}, dtypes={}):
    file_name = os.path.join(BASE_DIR, file)
    df = pd.read_csv(file_name, usecols=columns, dtype=dtypes)
    print("dataframe has been loaded: %d" % len(df))
    print(df.info(memory_usage="deep"))
    save_obj(df, BASE_DIR, "DF_metadata")
    print("Metadata has been stored")

BASE_DIR = sys.argv[1]

COLS = ['Id', 'PostTypeId', "AcceptedAnswerId", "ParentId", "CreationDate", "ViewCount", "Score"]
Types = {'Id': 'Int64', 'PostTypeId': 'Int64', "AcceptedAnswerId": 'Int64', "ParentId":'Int64', "CreationDate": "str", "ViewCount": 'Int64', "Score": 'Int64'}
# extract_meta_data(BASE_DIR, columns=COLS, dtypes = Types)
# extract_meta_data(BASE_DIR="/work/disa_lab/Alamin/SOTorrent/SO/", columns=COLS, dtypes = Types)
extract_meta_data(BASE_DIR, columns=COLS, dtypes = Types)
print("Extracting metadata finished")

