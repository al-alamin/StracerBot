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




def get_all_codes(BASE_DIR, file_name = "Posts_code.csv"):
    code_segment_file = os.path.join(BASE_DIR, file_name)
    df = pd.read_csv(code_segment_file)
    print("Len of code segment: %d" % len(df))
    ALL_CODE_SEGMENTS = df['code'].tolist()
    ALL_IDs = df['Id'].tolist()    
    print(len(ALL_CODE_SEGMENTS))
    return ALL_CODE_SEGMENTS, ALL_IDs





def get_similarity_metrics(Codes, BASE_DIR):
    Gen_docs = [ word_tokenize(text.lower()) for text in Codes] # tokenize
    Dictionary = gensim.corpora.Dictionary(Gen_docs) # word => Id
    print("Dictionary has been created %d" % len(Dictionary))
    # print(Dictionary.token2id) # word id and its frequency in each document
    Corpus = [Dictionary.doc2bow(gen_doc) for gen_doc in Gen_docs] # word id and its frequency in each document
    print("Corpus has been created")
    # print(word_tokenize(err1))
    TDIDF = gensim.models.TfidfModel(Corpus)
    print("TDIDF has been created") 

    sim_path = os.path.join(BASE_DIR, "TDIDF/")
    remove_directory(sim_path)
    create_director(sim_path)
    Sims = gensim.similarities.Similarity(sim_path, TDIDF[Corpus],
                                        num_features=len(Dictionary))
    print("Sims has been created")
    return Dictionary, Corpus, TDIDF, Sims



# BASE_DIR = "/work/disa_lab/Alamin/SOTorrent/serverfault/"
BASE_DIR = sys.argv[1]

ALL_CODE_SEGMENTS, ALL_IDs = get_all_codes(BASE_DIR)
save_obj(ALL_IDs, BASE_DIR, "ALL_IDs")
print("Code segment extracted")

Dictionary, Corpus, TDIDF, Sims = get_similarity_metrics(ALL_CODE_SEGMENTS, BASE_DIR)

save_obj(Dictionary, BASE_DIR, "Dictionary")
save_obj(Corpus, BASE_DIR, "Corpus")
save_obj(TDIDF, BASE_DIR, "TDIDF")
save_obj(Sims, BASE_DIR, "Sims")
print("Saved all objects")


