##packages code
from shapely.geometry import Point
import pandas as pd
from tqdm import tqdm
import streamlit as st
import numpy as np
import json, requests 
import pandas as pd
from pandas.io.json import json_normalize

import matplotlib.pyplot as plt
import seaborn as sns
from math import radians, cos, sin, asin, sqrt

import spacy
#!python -m spacy download en_core_web_lg


from sentence_transformers import SentenceTransformer, util

@st.cache_resource
def model_nlp():
    model = SentenceTransformer('all-MiniLM-L6-v2')
    return model

import unicodedata

from metaphone import doublemetaphone
from fuzzywuzzy import fuzz
from difflib import SequenceMatcher
import re

import geopandas as gpd
from geopandas import GeoDataFrame


@st.cache_data  # 👈 Add the caching decorator
def load_data():
    url = "Synapse_project/Climate_site/python_scripts/institutions.tsv"
    dic = pd.read_csv(url, delimiter = "\t" , index_col = 0).to_dict('index')
    return dic

dic_institutions = load_data()


#################### General Functions #############################

def URL(base_URL , entity_type , filters):
    url = base_URL + entity_type + filters 
    return url


def get_data(url):
    url = requests.get(url)
    text = url.text
    import json
    data = json.loads(text)
    return data

## encoding the abstract


def reconstruction_abstract(abstract_inverted_index):
    # return the abstract is the abstract exists in the database, else, return None
    
    if abstract_inverted_index != None:
        
        list_values = list(abstract_inverted_index.values())
        list_keys = list(abstract_inverted_index.keys())
        #from the words in the abstract (keys of abstract_inverted_index) and their position in the text (values of abstract_inverted_index), reconstruct the abstract
        
        size_abstract = max([ max(elem) for elem in abstract_inverted_index.values() ] )
        
        abstract = [""]*(size_abstract +1)
        
        for i in range(len(list_values)):
            for pos in list_values[i]:
                abstract[pos] = list_keys[i]
        
        return " ".join(list(abstract))
    
    else:
        return None
            
    
## calculate efficiently the dot product between two vectors

def norm(vector):
    return np.sqrt(sum(x * x for x in vector))    

def cosine_similarity2(vec_a, vec_b):
        norm_a = norm(vec_a)
        norm_b = norm(vec_b)
        dot = sum(a * b for a, b in zip(vec_a, vec_b))
        return dot / (norm_a * norm_b)




#################### Paper Functions #############################

def related_papers_own_research(  research_key_words , display  ):

    dic = {}

    max_count = 0
    base_URL_OA = f'https://api.openalex.org/'
    filter_works = f'works?'
    
        

    filter_openalex = f"search=" + research_key_words + "&per_page=200&mailto=emma_scharfmann@berkeley.edu"
        
        
    filter_openalex = filter_openalex.replace(" " , "%20")
    
    url = URL(base_URL_OA , filter_works, filter_openalex) 
    data = get_data(url)
    count = data["meta"]["count"] 



    if display == True:
        print(  data["meta"]["count"] , [elem[i] for i in range(1,len(elem))]  )
        print(url)
    
    for i in range(len(data["results"])):
        dic[ data["results"][i]["id"]] = {}
        dic[ data["results"][i]["id"]]["title"] = data["results"][i]["title"]
        dic[ data["results"][i]["id"]]["abstract"] = reconstruction_abstract(data["results"][i]["abstract_inverted_index"])
        dic[ data["results"][i]["id"]]["concepts"] = data["results"][i]["concepts"]
        dic[ data["results"][i]["id"]]["date"] = data["results"][i]["publication_date"]
        dic[ data["results"][i]["id"]]["authorships"] = data["results"][i]["authorships"]
        dic[ data["results"][i]["id"]]["cited_by_count"] = data["results"][i]["cited_by_count"]

        if len(data["results"][i]["authorships"]) > 0:
            if data["results"][i]["authorships"][0]["institutions"] != []:
                dic[ data["results"][i]["id"]]["countries"] = data["results"][i]["authorships"][0]["institutions"][0]["country_code"]
                dic[ data["results"][i]["id"]]["institutions"] = data["results"][i]["authorships"][0]["institutions"][0]["display_name"]
            else:
                dic[ data["results"][i]["id"]]["countries"] = ""
                dic[ data["results"][i]["id"]]["institutions"] = ""
            dic[ data["results"][i]["id"]]["authors"] = data["results"][i]["authorships"][0]["author"]["display_name"]

            for j in range(1 , len(data["results"][i]["authorships"])):
                if data["results"][i]["authorships"][j]["institutions"] != []:
                    dic[ data["results"][i]["id"]]["institutions"] += ", " + data["results"][i]["authorships"][j]["institutions"][0]["display_name"]
                    dic[ data["results"][i]["id"]]["countries"] = data["results"][i]["authorships"][j]["institutions"][0]["country_code"]
                dic[ data["results"][i]["id"]]["authors"] += ", " + data["results"][i]["authorships"][j]["author"]["display_name"]

    if display == True: 
        print(" ")
        
    return dic
        
    
        

## Ranking Papers

def ranking_own_research(research_key_words,  details  , display):
    
    model = model_nlp()
    
    dic_scores_papers = {}
    dic = related_papers_own_research( research_key_words , False)
    
    reference_text = details
        
    if display== True:
        print("Technology details: " , reference_text)
        print(" ")
    encoded_text = model.encode(reference_text, convert_to_tensor=False , show_progress_bar = False).tolist()
    

    
    for ids in list(dic.keys()):

        dic_scores_papers[ids] = {}
        
        if dic[ids]["title"] != None:
            encoded_title = model.encode(dic[ids]["title"], convert_to_tensor=False , show_progress_bar = False).tolist()
            score_title = cosine_similarity2(encoded_title, encoded_text)
        else:
            score_title = None

    

        if dic[ids]["abstract"] != None:
            encoded_abstract = model.encode(dic[ids]["abstract"], convert_to_tensor=False , show_progress_bar = False).tolist()
            score_abstract = cosine_similarity2(encoded_abstract, encoded_text)
        else:
            score_abstract = None


        #concepts = ""
        #for elem in dic[ids]["concepts"]:
        #    concepts += elem["display_name"] + " "
        #encoded_concepts = model.encode(concepts, convert_to_tensor=False).tolist()
        #score_concepts = cosine_similarity2(encoded_concepts, encoded_text)

        dic_scores_papers[ids]["title comparison"] = score_title
        dic_scores_papers[ids]["abstract comparison"] = score_abstract
        #dic_scores_papers[ids]["concepts comparision"] = score_concepts
        
        dic_scores_papers[ids]["title"] = dic[ids]["title"]
        dic_scores_papers[ids]["citations"] = dic[ids]["cited_by_count"]
        

        dic_scores_papers[ids]["date"] = dic[ids]["date"][:4]
        if "institutions" in dic[ids]:
            dic_scores_papers[ids]["institutions"] = dic[ids]["institutions"]
        #    dic_scores_papers[ids]["countries"] = dic[ids]["countries"]
            
        else:
            dic_scores_papers[ids]["institutions"] = None
        #    dic_scores_papers[ids]["countries"] = None
        
        if "authors" in dic[ids]:
            dic_scores_papers[ids]["number of co-authors"] = len(dic[ids]["authors"].split(","))
            dic_scores_papers[ids]["authors"] = dic[ids]["authors"]

    return dic , dic_scores_papers
    



    
    
    
def get_ranking_own_research(research_key_words,  details  , display , size):
    
    dic , dic_scores_papers = ranking_own_research(research_key_words,  details  , display)
    
    if dic_scores_papers == {}:
        return "No paper found"
    
    elif type(dic_scores_papers) == str:
        return dic_scores_papers
    
    else:
        return pd.DataFrame(dic_scores_papers).T.sort_values(by="abstract comparison" , ascending = False)[:size]
     
      
 
          
    


def extract_quantitative_data_paper(work_id):

    url = "https://api.openalex.org/works/" + str(work_id)
    url_google = "https://explore.openalex.org/works/" + str(work_id)
    
    data = get_data(url)
    date = data["publication_date"]
    title = data["title"]
    abstract = reconstruction_abstract(data["abstract_inverted_index"])
    concepts = ", ".join( [elem["display_name"] for elem in data["concepts"]] )
    authors = ", ".join( [elem["author"]["display_name"] for elem in data["authorships"]] )
    institutions = ", ".join( set([elem["institutions"][0]["display_name"] for elem in data["authorships"] if len(elem["institutions"]) > 0]) )
    return url_google , title , abstract , date , authors , institutions
            

    


## Mapping the authors

#merge the nobiliary particles with the last name
#ln_suff file can be modified if more or less nobiliary particles want to be suppressed

ln_suff = ['oster',
 'nordre',
 'vaster',
 'aust',
 'vesle',
 'da',
 'van t',
 'af',
 'al',
 'setya',
 'zu',
 'la',
 'na',
 'mic',
 'ofver',
 'el',
 'vetle',
 'van het',
 'dos',
 'ui',
 'vest',
 'ab',
 'vste',
 'nord',
 'van der',
 'bin',
 'ibn',
 'war',
 'fitz',
 'alam',
 'di',
 'erch',
 'fetch',
 'nga',
 'ka',
 'soder',
 'lille',
 'upp',
 'ua',
 'te',
 'ni',
 'bint',
 'von und zu',
 'vast',
 'vestre',
 'over',
 'syd',
 'mac',
 'nin',
 'nic',
 'putri',
 'bet',
 'verch',
 'norr',
 'bath',
 'della',
 'van',
 'ben',
 'du',
 'stor',
 'das',
 'neder',
 'abu',
 'degli',
 'vre',
 'ait',
 'ny',
 'opp',
 'pour',
 'kil',
 'der',
 'oz',
 'von',
 'at',
 'nedre',
 'van den',
 'setia',
 'ap',
 'gil',
 'myljom',
 'van de',
 'stre',
 'dele',
 'mck',
 'de',
 'mellom',
 'mhic',
 'binti',
 'ath',
 'binte',
 'snder',
 'sre',
 'ned',
 'ter',
 'bar',
 'le',
 'mala',
 'ost',
 'syndre',
 'sr',
 'bat',
 'sndre',
 'austre',
 'putra',
 'putera',
 'av',
 'lu',
 'vetch',
 'ver',
 'puteri',
 'mc',
 'tre',
 'st']

#suppress all the unwanted suffixes from a string. 
#name_del file can be modified if more or less suffixes want to be suppressed 

name_del = ['2nd', '3rd', 'Jr', 'Jr.', 'Junior', 'Sr', 'Sr.', 'Senior']


def name_delete(string):
    for elmt in name_del:
        if f" {elmt}" in string:
            return string.replace(f" {elmt}","")
    return string

def ln_suff_merge(string):
    for suff in ln_suff:
        if f" {suff} " in string or string.startswith(f"{suff} "):
            return string.replace(f"{suff} ",suff.replace(" ",""))
    return string

#normalize a string dat that represents often a name. 

def normalize(data):
    normal = unicodedata.normalize('NFKD', data).encode('ASCII', 'ignore')
    val = normal.decode("utf-8")
    # delete unwanted elmt
    val = name_delete(val)
    # lower full name in upper
    val = re.sub(r"[A-Z]{3,}", lambda x: x.group().lower(), val)
    # add space in front of upper case
    val = re.sub(r"(\w)([A-Z])", r"\1 \2", val)
    # Lower case
    val = val.lower()
    # remove special characters
    val = re.sub('[^A-Za-z0-9 ]+', ' ', val)
    # remove multiple spaces
    val = re.sub(' +', ' ', val)
    # remove trailing spaces
    val = val.strip()
    # suffix merge
    val = ln_suff_merge(val)

    return val


def main_authors( research_key_words  , details ,   size):
        
    dic_papers , dic_papers_ranked = ranking_own_research(  research_key_words  , details ,  False  )
    
    dic_papers_co_authors = {}
        
    for paper in list(dic_papers_ranked.keys())[:size]:

        for k in range(len(dic_papers[paper]["authorships"])):
            coauthor_id = dic_papers[paper]["authorships"][k]["author"]["id"]
            
            
            author_name = dic_papers[paper]["authorships"][k]["author"]["display_name"]
            author_name_norm = normalize(dic_papers[paper]["authorships"][k]["author"]["display_name"]).split()
            if len (author_name_norm) > 0:
                
                author_name_norm = author_name_norm[0] + " " + author_name_norm[-1]

                if author_name_norm not in dic_papers_co_authors:
                    dic_papers_co_authors[author_name_norm] = {}
                    dic_papers_co_authors[author_name_norm]["Author's name(s)"] = author_name
                    dic_papers_co_authors[author_name_norm]["Author's id(s)"] = coauthor_id[21:]
                    dic_papers_co_authors[author_name_norm]["Number of occurence within the 100 most related papers"] = 1
                    dic_papers_co_authors[author_name_norm]["Number of related citations"] = dic_papers[paper]["cited_by_count"]
                else:
                    dic_papers_co_authors[author_name_norm]["Number of occurence within the 100 most related papers"] += 1
                    if author_name not in dic_papers_co_authors[author_name_norm]["Author's name(s)"]:
                        dic_papers_co_authors[author_name_norm]["Author's name(s)"] += ", " + author_name
                    if coauthor_id[21:] not in dic_papers_co_authors[author_name_norm]["Author's id(s)"]:                                                              
                        dic_papers_co_authors[author_name_norm]["Author's id(s)"] += ", " + coauthor_id[21:]
                        dic_papers_co_authors[author_name_norm]["Number of related citations"] += dic_papers[paper]["cited_by_count"]



    if dic_papers_co_authors != {}:
        dic_papers_co_authors = {k: v for k, v in sorted(dic_papers_co_authors.items(), key=lambda item: item[1]["Number of occurence within the 100 most related papers"] , reverse = True)}

        for author_name_norm in list(dic_papers_co_authors.keys())[:size]:
            list_ids = dic_papers_co_authors[author_name_norm]["Author's id(s)"].split(", ")
            work_count = 0
            cited_by_count = 0
            institutions = ''
            for elem in list_ids:
                if len(elem) > 3:
                    
                    data = get_data("https://api.openalex.org/people/" + elem)
                    work_count += data["works_count"]
                    cited_by_count += data["cited_by_count"]
                    if data["last_known_institution"] != None and data["last_known_institution"]["display_name"] != None:
                        if institutions == '':
                            institutions += data["last_known_institution"]["display_name"]
                        else:
                            institutions += ", " + data["last_known_institution"]["display_name"]
                    
            dic_papers_co_authors[author_name_norm]["Last Known Institution"] = institutions
            dic_papers_co_authors[author_name_norm]["Number of works"] = work_count
            dic_papers_co_authors[author_name_norm]["Number of citations"] = cited_by_count

            
        return pd.DataFrame(dic_papers_co_authors, index = [ "Author's name(s)" , "Author's id(s)" ,  "Number of occurence within the 100 most related papers" , "Last Known Institution" , "Number of works" , "Number of citations" ,  "Number of related citations"]).T.style.hide(axis="index")

    else:
        return ("Select another category")


def map_authors(research_key_words , details , size):

    dic_papers , dic_papers_ranked = ranking_own_research(  research_key_words  , details ,  False  )

    
    dic_papers_co_authors = {}
    count = 0
    

    for paper in list(dic_papers_ranked.keys())[:size]:
        
        for k in range(len(dic_papers[paper]["authorships"])):
            
            if dic_papers[paper]["authorships"][k]["institutions"] != [] and "id" in dic_papers[paper]["authorships"][k]["institutions"][0] and dic_papers[paper]["authorships"][k]["institutions"][0]["id"] != None:
                institution_id = dic_papers[paper]["authorships"][k]["institutions"][0]["id"][21:]
                if institution_id in dic_institutions:
                    data = dic_institutions[institution_id]

                    dic_papers_co_authors[count] = {}
                    dic_papers_co_authors[count]["longitude"] = data["longitude"]
                    dic_papers_co_authors[count]["latitude"] = data["latitude"]
                    dic_papers_co_authors[count]["abstract comparison"] = dic_papers_ranked[paper]["abstract comparison"]
                    dic_papers_co_authors[count]["author"] = dic_papers[paper]["authorships"][k]["author"]["display_name"]
                    dic_papers_co_authors[count]["institution"] = dic_papers[paper]["authorships"][k]["institutions"][0]["display_name"]
                    dic_papers_co_authors[count]["date"] = dic_papers[paper]["date"]
                    
                    count += 1


                        
    if dic_papers_co_authors == {}:
        return "No papers"
    
    

    
    map_df = pd.DataFrame(dic_papers_co_authors).T
    map_df["longitude"]=map_df['longitude'].astype(float)
    map_df['latitude']=map_df['latitude'].astype(float)
    map_df = map_df[map_df["latitude"].notnull()]

    return map_df
       



