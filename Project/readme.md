# Stack Exchange Error Post Finder

**Github link: https://github.com/al-alamin/SO-Error-Finder**

## Project Overview

## Dataset
Stack Exchange Data dump June, 2021. This contains all the data from 70+ stack exange websites such as (Stack Overflow, Server Fault)

## Folder Description
* Projects: This contains all the codes and documentation related to the the Project
* batch_jobs: This contains all the bash scripts that were submitted to complete this project. Details information for each file is provided below.
* Scripts: This contains the python files that contains necessary codes for data analytics of this project. SLURM bash scripts usually uses these python scripts to complete a task. Details information for each file is provided below.


## Tasks
* **Dataset Processing:**
    * Move Dataset to ARC cluster. [Completed]
    * Extracting Dataset using 7zip. [Completed]
    * Writing scripts to convert XML files to CSV file. [Completed]
    * Use Pandas to extract error messages or code segments from the CSV files. [Completed]
* **Search and Generate result**: 
    * Research on efficient way to text percentage matching, i.e., finding appropriate stack exchange posts from user provided error messages. [Ongoing]
        * This is the research part of the project. There may be multiple approach, i.e., algorithms to get better result with less computation.
        * First implement Term Frequency – Inverse Document Frequency(TF-IDF) and see the result.
    * Text Summarization: If mulple Stack exange Posts match the users error message, then provide a summarization.
* **Result presentation**
    * Develop User interface to take user input and present the result.
    * Configure ARC cluster to run computationally expensive distributed job using spark
        * Findout users statistics (reputation, Age, views) for specific domains or discussions, e.g., IoT, Low-code Software development, Android development etc.
    *
* High Computational tasks: I'll try to complete these tasks if I can manage time.
    * Rewrite some of the data preprocessing jobs with DASK instead of Pandas. This is supposed to be at least 10 times faster. Using the multi processing power of the DASK library will enable to process Significantly larger dataset than the current one used in this project.
    * Rewrite some of the result generation code with Apache Spark. Being able to write parallize code using Spack will enable to generate result in a very scalable manner.
    * Implement a distributed key-value storage with Spark. This system will help to quickly fetch important related information from around 60M Stack exchange posts.

## Batch Jobs Overview:
* data_extraction.sh:
        The original format of the dataset is .7z. We need to extract those zipped files. The this scripts takes input of the input zipped file and output folder and extracts that zipped file in the output folder. Some of the bigger zip file takes more than couple of hours to complete.

* csv_conversion.sh:
        The original dataset is in XML format. For future processing, its very helpful for us if the file format is in CSV. Because there are already lots of optimized python libraries that can work very efficiently with CSV file format. For example, Pandas and DUSK. DUSK is a wrapper over Pandas libarary but all of its APIs are designed for parallism, i.e., they make the best usage of available CPU cores and Memory.
        So this script takes input of a XML file and converts that to a CSV file. 
        Computation challenge: Some of the XML files are quite big (80GB). So, with clusters Big Mem this can be handled easily. Alternatively the code to read the big file chunk by chunk is quite complex. As it turns out for large file Pandas APIs does not work properly.

## Scripts:
*   csv_conversion.py:
        This contains necessary python code (Pandas) to convert a XML file to a CSV file. As it turns out the Pandas API for conversion of Large XML files does not work properly. So I had to write a different method that would read a large XML file iteratively and build Pandas dataframe from it and append it to the CSV file
*   extract_code_segment.py:
        Orginal Posts contains a lot of metadata information such as ["Id", "PostTypeId", "AcceptedAnswerId", "ParentId", "CreationDate", "DeletionDate", "Score", "ViewCount", "Body", "OwnerUserId", "OwnerDisplayName", "LastEditorUserId", "LastEditorDisplayName", "LastEditDate", "LastActivityDate", "Title", "Tags", "AnswerCount", "CommentCount", "FavoriteCount", "ClosedDate", "CommunityOwnedDate", "ContentLicense"]. The body contains the original posts html content. But for this project we are mostly interested in the error messages that are shared in the Stack Overflow posts. So, in this script I am extracting the code segment from the Post's HTML body. It is easy but computationally expensive to extract these code segments because the code segment resides under \<code> error message \</code> tag.
*   create_tdidf_document.py:
        This script contains necessary code to create Term Frequency – Inverse Document Frequency(TF-IDF). This TDIDF will help to find relevent posts with the user submitted errors messages very quickly. Because total dataset size contains more then 50M posts and more than 100M code segments.
*   extract_metadata.py:
        Our original Posts.csv is very large in size and for the most part we do not need all those information. So, this script will extact necessary metadata from the Posts.csv and store the information in python object. So that in the future this python object can be quickly loaded into memory and gerenerate search result.


## Dataset Overflow:
* Stack exchange has several Entities such as Posts, Comment, Users. Different attibutes of these entities are outlined below:
    * Posts: ["Id", "PostTypeId", "AcceptedAnswerId", "ParentId", "CreationDate", "DeletionDate", "Score", "ViewCount", "Body", "OwnerUserId", "OwnerDisplayName", "LastEditorUserId", "LastEditorDisplayName", "LastEditDate", "LastActivityDate", "Title", "Tags", "AnswerCount", "CommentCount", "FavoriteCount", "ClosedDate", "CommunityOwnedDate", "ContentLicense"]
    * Users: ["Id", "Reputation", "CreationDate", "DisplayName", "EmailHash", "LastAccessDate", "WebsiteUrl", "Location", "Age", "AboutMe", "Views", "UpVotes", "DownVotes"]
        => Comment: ["Id", "PostId", "Score", "Text", "CreationDate", "UserId"]




## Links:
* https://rcs.ucalgary.ca/Apache_Spark_on_ARC
* https://dev.to/coderasha/compare-documents-similarity-using-python-nlp-4odp
* https://towardsdatascience.com/calculating-string-similarity-in-python-276e18a7d33a