from flask import Flask, render_template, request
import os, sys
import time

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
import xml.etree.ElementTree as ET
import pickle
import math
from bs4 import BeautifulSoup
import nltk
import shutil

import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
import gensim



app = Flask(__name__)
print("Flask App initiated.")



import textwrap
from summarizer import Summarizer,TransformerSummarizer
GPT2_model = TransformerSummarizer(transformer_type="GPT2",transformer_model_key="gpt2-medium")
print("GPT2 Model loaded")


class URL:
    def __init__(self, url, similarity_score, title, summary):
        self.url = url
        self.similarity_score = similarity_score
        self.title = title        
        self.body_summary = summary

    def __str__(self):
        return "Similarity Score: %0.1f\nTitle: %s\nlink: %s\nPost Summary:\n%s\n" % (self.similarity_score, self.title, self.url, self.body_summary)

def get_question_meta_information(df, question_id):
    ques = df[df['Id'] == int(question_id)]
    if(len(ques) < 1):
        return None
    return ques.iloc[0]

def get_matched_post_ids(input, N, Dictionary, TDIDF, Sims, PostIds):
    tokens = word_tokenize(input.lower())
    # print(tokens)
    query_bow = Dictionary.doc2bow(tokens)
    # print(query_bow)
    # perform a similarity query against the corpus
    query_tf_idf = TDIDF[query_bow]
    res = Sims[query_tf_idf]
    indx = res.argsort()[-N:][::-1] # biggest matched Id first
    sim_scores = res[indx] * 100

    post_ids = [PostIds[i] for i in indx]
    print(post_ids)
    return (post_ids, sim_scores)

def get_post_ranking(similarity_tuple, metadata):
    def update_ranking(qid, score):
        if qid not in Map_ranking:
            Map_ranking[qid] = 0.0
        Map_ranking[qid] = Map_ranking[qid] + score

    Map_ranking = {}
    # rank_score = N
    post_ids, similarity_scores = similarity_tuple
    for post_id, post_score in zip(post_ids, similarity_scores):
        post = get_question_meta_information(metadata, post_id)
        rank_score = post_score
        # metadata[metadata['Id'] == post_id].iloc[0]
        # print(post.PostTypeId)
        if(post.PostTypeId == 1):
            # print(type(post.AcceptedAnswerId))
            # Ranking heuristics: If the post does not have accepted answer then deduct some score)
            # Also consider the score of the post in the ranking
            if(pd.isna(post.AcceptedAnswerId) ):
                update_ranking(post.Id, rank_score * 0.95)
                print("===============================> Method updated")
            else:                
                update_ranking(post.Id, rank_score)
        else:
            update_ranking(post.ParentId, rank_score * 0.25)
    # Map_ranking = sorted(Map_ranking.items(), key=lambda x: x[1], reverse=True)
    Map_ranking = dict(sorted(Map_ranking.items(), key=lambda item: item[1], reverse=True))
    return Map_ranking

def generate_url(website, type, qid):
    url = "https://%s.com/%s/%d" % (website, type, qid)
    return url

def gerenerate_results(question_map, website, DF_metadata, N_max=5):
    urls = []
    count = 0
    for qid, similarity_score in question_map.items(): 
        post = get_question_meta_information(DF_metadata, qid)
        if post is not None:
            url_link = generate_url(website, 'q', qid)
            url = URL(url_link, similarity_score, post.Title, prettyfy_long_string(get_body_summary(post.Body)))
            urls.append(url)
            count += 1
        if (count >= N_max):
            break
    return urls

def get_cleaned_text(body):
    soup = BeautifulSoup(body,'html.parser')
    paragraphs = soup.find_all('p')
    res = ""
    for paragraph in paragraphs:
        res += " " + paragraph.get_text()
    return res

def get_text_summary(text, ratio=0.25, min_length=10):
    summary = ''.join(GPT2_model(text, ratio=ratio, min_length=min_length))
    return summary

def get_body_summary(post_body):
    post_body_cleaned = get_cleaned_text(post_body)
    # print(post_body_cleaned)
    post_body_summary = get_text_summary(post_body_cleaned)
    return post_body_summary

def prettyfy_long_string(text, width=100):
    return textwrap.fill(text, width)

def setup_environment():
        print("#" * 20)
        print("Expensive setup method")
        os.environ["INITIALIZED"] = "True"
        time.sleep(1)
        print("Environment setup finished")
        return 1, 2, 3, 4, 5, 6

# ALL_IDs, Dictionary, Corpus, TDIDF, Sims, DF_metadata = (1, 2, 3, 4, 5, 6)
# ALL_IDs, Dictionary, Corpus, TDIDF, Sims, DF_metadata = load_related_variables(BASE_DIR)










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
        os.remove(file_name)

def create_director(dir):
    if(not os.path.exists(dir)):
        print("Creating directory %s." % dir)
        os.makedirs(dir)
    else:
        print("Directory %s already exists and so returning." % dir)



def load_related_variables(root_dir):
    # return 1, 2, 3, 4, 5, 6
    ALL_IDs = load_obj(root_dir, "ALL_IDs")
    print("loaded ALL_IDs and size %d " % len(ALL_IDs))
    Dictionary = load_obj(root_dir, "Dictionary") # Must
    print("loaded Dictionary and size %d " %  len(Dictionary))
    Corpus = load_obj(root_dir, "Corpus")
    print("loaded Corpus and size %d " % len(Corpus ))
    TDIDF = load_obj(root_dir, "TDIDF") # Must
    print("loaded TDIDF and size %d " % sys.getsizeof(TDIDF))
    Sims = load_obj(root_dir, "Sims") # Must
    print("loaded Sims and size %d " % len(Sims))
    DF_metadata = load_obj(root_dir, "DF_metadata") # Must
    print("loaded DF_metadata and size %d " % len(DF_metadata))
    return ALL_IDs, Dictionary, Corpus, TDIDF, Sims, DF_metadata


BASE_DIR = "/home/mdabdullahal.alamin/alamin/courses/619_data/DATA/serverfault/"
BASE_DIR = "/home/mdabdullahal.alamin/alamin/courses/619_data/DATA/SO/"
print("About the load the expensive pre-processed models")
ALL_IDs, Dictionary, Corpus, TDIDF, Sims, DF_metadata = load_related_variables(BASE_DIR)
print("Expensive pre-processed models are loaded")

# ALL_IDs, Dictionary, Corpus, TDIDF, Sims, DF_metadata = setup_environment()
# This method uses global variables
def query_and_report_similar_posts(query_text, N_max=30, Dictionary=Dictionary, TDIDF=TDIDF, Sims=Sims, ALL_IDs=ALL_IDs):
    similarity_tuple = get_matched_post_ids(query_text, N_max, Dictionary, TDIDF, Sims, ALL_IDs)
    # print(len(list(similarity_tuple)))

    question_ranks = get_post_ranking(similarity_tuple, DF_metadata)
    print(question_ranks)
    urls = gerenerate_results(question_ranks, "stackoverflow", DF_metadata, N_max=3)
    for url in urls:
        print(url)
    return urls







        


def get_result(error_message):

    urls = [
        URL("https://stackoverflow.com/questions/11556958/s", 88.5, "Question 1", '''I am trying to get my first taste of Android development using Eclipse. Similar questions seem to
indicate that it's a 32-bit/64-bit conflict, but I'm 99% positive that I downloaded 64-bit versions
of both Eclipse and Java (RE 7u5), which I chose because I have 64-bit Windows 7. '''), 
        URL("https://stackoverflow.com/questions/11556958/s", 88.5, "Question 2 ", '''I am trying to get my first taste of Android development using Eclipse. Similar questions seem to
indicate that it's a 32-bit/64-bit conflict, but I'm 99% positive that I downloaded 64-bit versions
of both Eclipse and Java (RE 7u5), which I chose because I have 64-bit Windows 7. '''), 
        URL("https://stackoverflow.com/questions/11556958/s", 88.5, "Question 3 ", '''I am trying to get my first taste of Android development using Eclipse. Similar questions seem to
indicate that it's a 32-bit/64-bit conflict, but I'm 99% positive that I downloaded 64-bit versions
of both Eclipse and Java (RE 7u5), which I chose because I have 64-bit Windows 7. ''')
        ]

    return urls







@app.route("/", methods=['post', 'get'])
def home():
    result = [URL("https://github.com/al-alamin/SO-Error-Finder/", 0.0, "GitHub link to the source code", "Details result of the search query will appear here")]
    error_message = "After submission the original query will appear here"
    if request.method == 'POST':
        error_message = request.form.get('error_message')  # access the data inside
        # result = get_result(error_message)
        result = query_and_report_similar_posts(error_message)


    return render_template("index.html", result = result, query_message=error_message)

if __name__ == "__main__":
    print("================================> Main method.")
    # print(os.environ.get("INITIALIZED"))
    # if os.environ.get("INITIALIZED") != "True":    
    #     setup_environment()
    # else:
    #     print("The environment has been setup already")
    app.run(debug=True, host="0.0.0.0", port=5001, use_reloader=False)
    print("App has been started")