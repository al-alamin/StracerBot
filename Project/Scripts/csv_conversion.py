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


def save_df(df, file_name):
    df.to_csv(file_name, index=False, quotechar='"', quoting=csv.QUOTE_NONNUMERIC)

def convert_xml_to_csv(xml_file, output_csv_file = None):
    if output_csv_file is None:
        output_csv_file = xml_file[:-4] + ".csv"
    print(output_csv_file)
    df = pd.read_xml(xml_file)
    print("Org Datafrme size: %d" % len(df))
    df.drop_duplicates('Id',inplace=True)
    print("After removing duplicates Datafrme size: %d" % len(df))
    save_df(df, output_csv_file)
    print("Output file has been generated to %s" % output_csv_file)



file_name = r"E:\\Research\\stackexchange\\study\\raf\\"
file_name = os.path.join(file_name, "Posts.xml")
# convert_xml_to_csv(file_name)

xml_file = os.path.normpath(sys.argv[1])
csv_file = None
if len(sys.argv) > 2:
    csv_file = os.path.normpath(sys.argv[2])
print("xml_file: %s csv_file: %s" % (xml_file, csv_file))
convert_xml_to_csv(xml_file, csv_file)
print("%s file converted to CSV" % (xml_file))