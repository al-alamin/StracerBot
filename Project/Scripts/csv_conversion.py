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
# import lxml.etree  as ET
import lxml.etree  as ET
# import xml.etree.ElementTree as ET

def save_df(df, file_name, append=False):
    if append:
        df.to_csv(file_name, index=False, quotechar='"', quoting=csv.QUOTE_NONNUMERIC, mode="a", header=False)
    else:
        df.to_csv(file_name, index=False, quotechar='"', quoting=csv.QUOTE_NONNUMERIC)

# This uses official Panda method to convert XML files to CSV. 
# But unfortunately this method does not scale up for larger files and crashes
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





def append_to_file(rows, output_csv_file, append):
    df = pd.DataFrame(rows)
    df.drop_duplicates('Id', inplace=True)
    save_df(df, output_csv_file, append=append)
    print("%d rows has been appended to the CSV file %s" % (len(df), output_csv_file))
    return len(df)

def convert_xml_to_csv_iteratively(XML_file, columns, output_csv_file = None, threshold = 10000000):
    if output_csv_file is None:
        output_csv_file = XML_file[:-4] + ".csv"

    print("Going to Convert XML files to CSV file")
    context = ET.iterparse(XML_file, recover = True, events=("end",))
    # huge_tree = True

    # Variables to process the output
    total_questions = 0
    unique_rows = 0
    rows = []
    cur_count = 0    
    append = False
    _, root = next(context)
    for event, elem in context:
        if elem.tag == "row":
            dic = {}
            for col in COLS:
                dic[col] = elem.attrib.get(col, '')
            rows.append(dic)
             # progress
            if total_questions % 1000000 == 0:
                print('Total Questions: %d' % total_questions)
            elem.clear()
            root.clear()
            total_questions += 1
            cur_count += 1
        if cur_count > threshold:
            unique_rows +=  append_to_file(rows, output_csv_file, append)
            append = True
            cur_count = 0
            rows = []
    if(len(rows) > 0):
        unique_rows += append_to_file(rows, output_csv_file, append)
    print("Total number of rows: %d vs unique_rows: %d" % (total_questions, unique_rows))
    return total_questions

# df.to_csv('my_csv.csv', mode='a', header=False)








# file_name = r"E:\\Research\\stackexchange\\study\\raf\\"
# file_name = os.path.join(file_name, "Posts.xml")
# convert_xml_to_csv(file_name)

xml_file = sys.argv[1]
csv_file = None
print("xml_file: %s csv_file: %s" % (xml_file, csv_file))
# convert_xml_to_csv(xml_file, csv_file)


COLS = ["Id", "PostTypeId", "AcceptedAnswerId", "ParentId", "CreationDate", "DeletionDate", "Score", "ViewCount", "Body",
        "OwnerUserId", "OwnerDisplayName", "LastEditorUserId", "LastEditorDisplayName", "LastEditDate", "LastActivityDate",
        "Title", "Tags", "AnswerCount", "CommentCount", "FavoriteCount", "ClosedDate", "CommunityOwnedDate", "ContentLicense"]
convert_xml_to_csv_iteratively(xml_file, columns = COLS, output_csv_file = csv_file, threshold=1000000)

print("%s file converted to CSV" % (xml_file))