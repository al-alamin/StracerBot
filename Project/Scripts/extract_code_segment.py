import warnings
warnings.filterwarnings('always')
warnings.simplefilter('always')
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=DeprecationWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")
import glob, os
# import matplotlib.pylab as plt
# from matplotlib import pyplot
import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None
import csv
import math
import sys
from bs4 import BeautifulSoup


def save_df(df, file_name, append=False):
    if append:
        df.to_csv(file_name, index=False, quotechar='"', quoting=csv.QUOTE_NONNUMERIC, mode="a", header=False)
    else:
        df.to_csv(file_name, index=False, quotechar='"', quoting=csv.QUOTE_NONNUMERIC)


def get_code_segment(html, min_code_length = 10):
    # print(html)
    parsed_html = BeautifulSoup(html, 'html.parser')
    result = ""
    for code in parsed_html.find_all("code"):
        result += code.get_text()        
    if len(result) < min_code_length:
        return np.nan
    return result


def extract_code_segment(input_file, chunk_size=10000000):
    output_csv_file = input_file[:-4] + "_code.csv"
    ids = []
    codes = []


    if (os.path.isfile(output_csv_file)):
        print("Output file %s exists and removing it." % output_csv_file)
        os.remove(output_csv_file)

    append = False
    with pd.read_csv(input_file, usecols=['Id', 'Body'], dtype={'Id': str, 'Body': str}, chunksize=chunk_size) as reader:
        for chunk in reader:
            print(type(chunk))
            print(len(chunk))
            # df = chunk[['Id', 'Body']]
            df = chunk
            df['Body'] = df['Body'].astype(str)            
            df['code'] = df.Body.apply(get_code_segment)
            df = df.drop('Body', axis = 1)
            df.dropna(subset = ["code"], inplace=True)
            save_df(df, output_csv_file, append)
            append = True


input_file = sys.argv[1]
print("input_file: %s" % (input_file))
extract_code_segment(input_file, chunk_size=20000000)