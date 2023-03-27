##packages code
from shapely.geometry import Point
import pandas as pd
from tqdm import tqdm

import numpy as np
import json, requests 
import pandas as pd
from pandas.io.json import json_normalize

import matplotlib.pyplot as plt
import seaborn as sns
from math import radians, cos, sin, asin, sqrt

import spacy
#!python -m spacy download en_core_web_lg
spacy_nlp = spacy.load("en_core_web_lg")

from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('all-MiniLM-L6-v2')
import unicodedata

from metaphone import doublemetaphone
from fuzzywuzzy import fuzz
from difflib import SequenceMatcher
import re

import geopandas as gpd
from geopandas import GeoDataFrame
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

## Extracted texts

def print_extracted_text(name_file):

    file = open('D:/UC Berkeley/Climate Site/Climate-Site/python_scripts/iea.txt', "r", encoding='utf8')
    lines = file.readlines()
    count = 0
    for index, line in enumerate(lines):
        read_line = line.strip()
        print(read_line)

    file.close()
    
    
    iea.txt


def details(name_file , display):
    
    file = open('D:/UC Berkeley/Climate Site/Climate-Site/python_scripts/iea.txt', "r", encoding='utf8')
    lines = file.readlines()

    mark = 0 
    dic_details = {}
    count = -1
    for index, line in enumerate(lines):

        line = line.strip()
        if line == "Close explanation":
            break

        if line != "" and  (line[0].isnumeric() and ">" in line and " 	" in line) :
            count += 1


        if mark == 1 and line != "" and line[0] == "*":
            
            if display == True:
                print(count)
                print(text)
                print(" ")
            dic_details[count] = text
            mark = 0


        if mark == 1:
            text = text + line + " "

        if line.split(" 	")[-1] == "Details" or line.split(" 	")[-1] == "Hide":
            mark = 1
            text = ""
            
    return dic_details





def key_initiatives(name_file , display ):
    
    file = open('D:/UC Berkeley/Climate Site/Climate-Site/python_scripts/iea.txt', "r", encoding='utf8')
    lines = file.readlines()

      
    mark = 0 
    dic_key_initiatives = {}
    count = -1
    for index, line in enumerate(lines):

        line = line.strip()
        if line == "Close explanation":
            break

        if line != "" and  (line[0].isnumeric() and ">" in line and " 	" in line) :

            count += 1



        if mark == 1 and line != "" and ( (line[0].isnumeric() and  ">" in line and " 	" in line) or line == "*Deployment targets:*" or line == "*Announced development targets:*"):
            if display == True: 
                print(count)
                print(text)
                print(" ")
            
            dic_key_initiatives[count] = text
            mark = 0


        if mark == 1:
            text = text + line + " "

        if line == "*Key initiatives:*":


            mark = 1
            text = ""
            
    return dic_key_initiatives




def deployment_target(name_file , display):
    
    file = open('D:/UC Berkeley/Climate Site/Climate-Site/python_scripts/iea.txt', "r", encoding='utf8')
    lines = file.readlines()


    mark = 0 
    dic_target = {}
    count = -1
    for index, line in enumerate(lines):

        line = line.strip()
        if line == "Close explanation":
            break

        if line != "" and  (line[0].isnumeric() and ">" in line and " 	" in line) :
            count += 1



        if mark == 1 and line != "" and  ((line[0].isnumeric() and ">" in line and " 	" in line)  or line == "*Announced cost reduction targets:*" or line == "*Announced development targets:*"):
            
            if display == True:
                print(count)
                print(text)
                print(" ")
                
            dic_target[count] = text
            mark = 0


        if mark == 1:
            text = text + line + " "

        if line == "*Deployment targets:*" or line == "*Announced development targets:*":

            mark = 1
            text = ""
            
    return dic_target


 
    
def cost_reduction_target(name_file , display):
    
    file = open('D:/UC Berkeley/Climate Site/Climate-Site/python_scripts/iea.txt', "r", encoding='utf8')
    lines = file.readlines()
    
    mark = 0 
    dic_cost = {}
    count = -1
    for index, line in enumerate(lines):

        line = line.strip()
        
        if line == "Close explanation":
            break

        if line != "" and  (line[0].isnumeric() and ">" in line and " 	" in line) :


            count += 1



        if mark == 1 and line != ""  and (line[0].isnumeric() and ">" in line and " 	" in line) :
            
            if display == True: 
                print(count)
                print(text)
                print(" ")
                
            dic_cost[count] = text
            mark = 0


        if mark == 1:
            text = text + line + " "

        if line == "*Announced cost reduction targets:*":

            mark = 1
            text = ""
            
    return dic_cost



def key_words(name_file, display ):
    
    file = open('D:/UC Berkeley/Climate Site/Climate-Site/python_scripts/iea.txt', "r", encoding='utf8')
    
    lines = file.readlines()
    
    list_categories = []
    count = -1
    for index, line in enumerate(lines):

        line = line.strip()
        
        if line == "Close explanation":
            break

        if line != "" and  (line[0].isnumeric() and ">" in line and " 	" in line) :
            count += 1
            
            if display == True:
                print("Technologies"  , count+1 , ":")

        if line != "":

            if line[0].isnumeric() and ">" in line and " 	" in line:
                i = 0
                try:
                    line = line.split(" 	")[2]
                except:
                    print(line)
                    break
                
                if "Details" not in lines[index] and "Moderate" not in lines[index]:
                
                    while "	" not in line:
                        i += 1
                        if "Details"==lines[index + i][:7] or "End-use"==lines[index + i][:7]:
                            break
                        else:
                            line = line + "  " +  lines[index + i]

                #if " Production" in line:
                    #line = line.replace(" Production" , "")

                line = line.replace("\n" , " ")
                line = line.replace("/" , " ")
                line = line.replace("-" , " ")
                line = line.split(" 	")[0]

                if "  " in line:
                    line = line.replace("  ", " ")
                line = line.split(">")


                if "(" in line[-1]:
                    line[-1] = line[-1].split("(")[0] 


                for i in range(len(line)):

                    # remove multiple spaces
                    line[i] = re.sub(' +', ' ', line[i])
                    # remove trailing spaces
                    line[i] = line[i].strip()

    

                if display == True:
                    print(line)
                    print(" ")
                    
                if '' in line:
                    line.remove('')

                list_categories.append([count , line])
                
    return list_categories



def technology(name_file, display ):
    # Filepath too specific, need to change to relative path
    file = open('D:/UC Berkeley/Climate Site/Climate-Site/python_scripts/iea.txt', "r", encoding='utf8')
    lines = file.readlines()
    
    list_categories = []
    count = -1
    for index, line in enumerate(lines):

        line = line.strip()
        
        if line == "Close explanation":
            break

        if line != "" and  (line[0].isnumeric() and ">" in line and " 	" in line) :
            count += 1
            
            if display == True:
                print("Technologies"  , count+1 , ":")

        if line != "":

            if line[0].isnumeric() and ">" in line and " 	" in line:
                i = 0
                try:
                    line = line.split(" 	")[1]
                except:
                    print(line)
                    break
                

                line = line.replace("\n" , " ")
                line = line.replace("/" , " ")
                line = line.replace("-" , " ")
                line = line.strip()
                line = re.sub(' +', ' ', line)
                line = line.split(" 	")[0]
                line = line.split(">")


                if "(" in line[-1]:
                    line[-1] = line[-1].split("(")[0] 


                for i in range(len(line)):

                    # remove multiple spaces
                    line[i] = re.sub(' +', ' ', line[i])
                    # remove trailing spaces
                    line[i] = line[i].strip()

    

                if display == True:
                    print(line)
                    print(" ")
                

                list_categories.append([count , line])
                
    return list_categories


#################### Patent Functions #############################

def related_patents(number_technology , research_words, carbon_related , display):
    
    name_file = "iea"
    list_categories = key_words( name_file, False)

    dic_patents = {}

    max_count = 0
    base_URL_PV = "https://api.patentsview.org/"
    filter_works = "patents/query?"
    filter_PV = "q={%22_and%22:[{%22_text_all%22:{%22patent_abstract%22:%22" 
    filter_PV += research_words
    
    if carbon_related == True:
        filter_PV += "%22}},{%22_eq%22:{%22cpc_group_id%22:%22Y02E%22}}]}&f=[%22patent_number%22,%22patent_title%22,%22assignee_country%22,%22patent_date%22,%22inventor_id%22,%22assignee_organization%22,%22inventor_longitude%22,%22inventor_latitude%22,%22inventor_last_name%22,%22inventor_first_name%22,%22cpc_subsection_title%22,%22assignee_city%22,%22patent_abstract%22,%22patent_kind%22,%22cpc_group_id%22,%22assignee_organization%22,%22citedby_patent_number%22]"
    
    else:
        filter_PV += "%22}}]}&f=[%22patent_number%22,%22patent_title%22,%22assignee_country%22,%22patent_date%22,%22assignee_organization%22,%22inventor_longitude%22,%22inventor_latitude%22,%22inventor_last_name%22,%22inventor_id%22,%22inventor_first_name%22,%22cpc_subsection_title%22,%22assignee_city%22,%22patent_abstract%22,%22patent_kind%22,%22cpc_group_id%22,%22assignee_organization%22,%22citedby_patent_number%22]"

        
    filter_PV = filter_PV.replace(" " , "%20")

        

    url = URL(base_URL_PV , filter_works, filter_PV) 
    data = get_data(url)


    if display == True:
        print(  data["total_patent_count"] , elem[-1] )
        print(url)



    
    for i in range(data["count"]):
        dic_patents[ "US-" + data["patents"][i]["patent_number"]] = {}
        dic_patents[ "US-" + data["patents"][i]["patent_number"]]["title"] = data["patents"][i]["patent_title"]
        dic_patents["US-" + data["patents"][i]["patent_number"]]["abstract"] = data["patents"][i]["patent_abstract"]

        dic_patents[ "US-" + data["patents"][i]["patent_number"]]["assignee"] = str(data["patents"][i]["assignees"][0]["assignee_organization"])
        dic_patents["US-" + data["patents"][i]["patent_number"]]["assignee_city"] = str(data["patents"][i]["assignees"][0]["assignee_city"])
        dic_patents["US-" + data["patents"][i]["patent_number"]]["assignee_country"] = str(data["patents"][i]["assignees"][0]["assignee_country"])
        for j in range(1, len(data["patents"][i]["assignees"])):
            dic_patents[ "US-" + data["patents"][i]["patent_number"]]["assignee"] +=  ", " + str(data["patents"][i]["assignees"][j]["assignee_organization"])
            dic_patents[ "US-" + data["patents"][i]["patent_number"]]["assignee_city"] +=  ", " + str(data["patents"][i]["assignees"][j]["assignee_city"])
            dic_patents["US-" + data["patents"][i]["patent_number"]]["assignee_country"] +=  ", " + str(data["patents"][i]["assignees"][j]["assignee_country"])

        dic_patents[ "US-" + data["patents"][i]["patent_number"]]["list_inventors"] = data["patents"][i]["inventors"]

        dic_patents[ "US-" + data["patents"][i]["patent_number"]]["inventors"] = str(data["patents"][i]["inventors"][0]["inventor_first_name"]) + " " + str(data["patents"][i]["inventors"][0]["inventor_last_name"])
        for j in range(1, len(data["patents"][i]["inventors"])):
            dic_patents[ "US-" + data["patents"][i]["patent_number"]]["inventors"] +=  ", " + str(data["patents"][i]["inventors"][j]["inventor_first_name"]) + " " + str(data["patents"][i]["inventors"][j]["inventor_last_name"])


        dic_patents["US-" + data["patents"][i]["patent_number"]]["date"] = data["patents"][i]["patent_date"]
        dic_patents["US-" + data["patents"][i]["patent_number"]]["number_citations"] = len(data["patents"][i]["citedby_patents"])


    if display == True:
        print(" ")
            
            
    return dic_patents



## Ranking Patents

def ranking_patents(number_technology , research_words, carbon_related , display):
    
    name_file = "iea"
    list_categories = key_words( name_file, False)
    dic_details = details(name_file , False)
    dic_patents = related_patents(number_technology , research_words, carbon_related , display)
    

    dic_scores = {}

    if display == True:
        print("Key words: " , list_categories[number_technology][1])
        
    if number_technology in dic_details:
        reference_text = dic_details[number_technology]
        if display == True:
            print("Technology details: " , reference_text)
            print(" ")
        encoded_text = model.encode(reference_text, convert_to_tensor=False).tolist()
        
        
        if len(dic_patents ) == 0:
            return "Select other key words"
        
        
        else:
            for ids in list(dic_patents.keys()):

                dic_scores[ids] = {}

                encoded_title = model.encode(dic_patents[ids]["title"], convert_to_tensor=False).tolist()
                score_title = cosine_similarity2(encoded_title, encoded_text)


                if dic_patents[ids]["abstract"] != None:
                    encoded_abstract = model.encode(dic_patents[ids]["abstract"], convert_to_tensor=False).tolist()
                    score_abstract = cosine_similarity2(encoded_abstract, encoded_text)
                else:
                    score_abstract = None

                dic_scores[ids]["title comparision"] = score_title
                dic_scores[ids]["abstract comparison"] = score_abstract
                dic_scores[ids]["title"] = dic_patents[ids]["title"]
                dic_scores[ids]["citations"] = dic_patents[ids]["number_citations"]
                dic_scores[ids]["date"] = dic_patents[ids]["date"][:4]
                dic_scores[ids]["assignee"] = dic_patents[ids]["assignee"]
                #dic_scores[ids]["assignee_city"] = dic_patents[ids]["assignee_city"]
                #dic_scores[ids]["assignee_country"] = dic_patents[ids]["assignee_country"]
                dic_scores[ids]["inventors"] = dic_patents[ids]["inventors"]
                dic_scores[ids]["number of co-inventors"] = len(dic_patents[ids]["inventors"].split(","))
    return dic_scores


def get_ranking_patents(technologies, number_technology ,category ,  carbon_related , size):
    dic_patents = ranking_patents(number_technology , category, carbon_related , False)
    if dic_patents == {}:
        return "No patent found, select other key words"

    elif dic_patents == "Select other key words":
        return dic_patents
    
    else:
        return pd.DataFrame(dic_patents).T.sort_values(by="abstract comparison" , ascending = False)[:size]
    
    
#merge the nobiliary particles with the last name
#ln_suff file can be modified if more or less nobiliary particles want to be suppressed

# with open("/home/emma_scharfmann/LeeFleming/MattMarx_Ryan_dataset/Patent_paper_pairs/ln_suff.json","r", encoding="utf-8") as f:
#     ln_suff = json.load(f)
    
def ln_suff_merge(string):
    for suff in ln_suff:
        if f" {suff} " in string or string.startswith(f"{suff} "):
            return string.replace(f"{suff} ",suff.replace(" ",""))
    return string



#suppress all the unwanted suffixes from a string. 
#name_del file can be modified if more or less suffixes want to be suppressed 

# with open("/home/emma_scharfmann/LeeFleming/MattMarx_Ryan_dataset/Patent_paper_pairs/name_del-2.json","r", encoding="utf-8") as f:
#     name_del = json.load(f)

def name_delete(string):
    for elmt in name_del:
        if f" {elmt}" in string:
            return string.replace(f" {elmt}","")
    return string



#normalize a string dat that represents often a name. 

def normalize(data):
    normal = unicodedata.normalize('NFKD', data).encode('ASCII', 'ignore')
    val = normal.decode("utf-8")
    # delete unwanted elmt
   # val = name_delete(val)
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
    #val = ln_suff_merge(val)

    return val


def main_inventors(technologies, number_technology , carbon_related , category , size ):
    display = False
    dic_patents = related_patents(number_technology , category, carbon_related , display)
    dic_patents_co_inventors = {}
    

    for patent in dic_patents:
        for k in range(len(dic_patents[patent]["list_inventors"])):
            
            inventor_id = dic_patents[patent]["list_inventors"][k]["inventor_id"]
            inventor_name = dic_patents[patent]["list_inventors"][k]["inventor_first_name"] + " " + dic_patents[patent]["list_inventors"][k]["inventor_last_name"]
            inventor_name_norm = normalize(inventor_name).split()
            inventor_name_norm = inventor_name_norm[0] + " " + inventor_name_norm[-1]

            if inventor_name_norm not in dic_patents_co_inventors:
                dic_patents_co_inventors[inventor_name_norm] = {}
                dic_patents_co_inventors[inventor_name_norm]["Inventor's name"] = inventor_name 
                dic_patents_co_inventors[inventor_name_norm]["PatentsView inventor's id"] =  inventor_id 
                dic_patents_co_inventors[inventor_name_norm]["Number of occurence"] = 1
                dic_patents_co_inventors[inventor_name_norm]["Number of related citations"] = dic_patents[patent]["number_citations"]

            else:
                if inventor_id not in dic_patents_co_inventors[inventor_name_norm]["PatentsView inventor's id"] :
                    dic_patents_co_inventors[inventor_name_norm]["PatentsView inventor's id"] += ", " + inventor_id
                if inventor_name not in dic_patents_co_inventors[inventor_name_norm]["Inventor's name"] :
                    dic_patents_co_inventors[inventor_name_norm]["Inventor's name"] += ", " + inventor_name
                dic_patents_co_inventors[inventor_name_norm]["Number of occurence"] += 1
                dic_patents_co_inventors[inventor_name_norm]["Number of related citations"] += dic_patents[patent]["number_citations"]


        dic_patents_co_inventors = {k: v for k, v in sorted(dic_patents_co_inventors.items(), key=lambda item: item[1]["Number of occurence"] , reverse = True)}
    
    if dic_patents_co_inventors == {}:
    
        
        return "No patent, select other key words"
    else:
        
        for inventor_name_norm in list(dic_patents_co_inventors.keys())[:size]:
            list_inventors = dic_patents_co_inventors[inventor_name_norm]["PatentsView inventor's id"].split(", ")
            work_count = 0
            cited_by_count = 0
            
            for elem in list_inventors:
                url = "https://api.patentsview.org/inventors/query?q={%22inventor_id%22:[%22" + elem + "%22]}&f=[%22inventor_total_num_patents%22,%22patent_num_cited_by_us_patents%22]"
                data = get_data(url)["inventors"][0]
                work_count += int(data["inventor_total_num_patents"])
                for k in range(len(data["patents"])):
                    cited_by_count += int(data["patents"][k]["patent_num_cited_by_us_patents"])
                
            dic_patents_co_inventors[inventor_name_norm]["Number of patents"] = work_count
            dic_patents_co_inventors[inventor_name_norm]["Number of US patents citations"] = cited_by_count
            
        
                
                
        return pd.DataFrame(dic_patents_co_inventors , index = ["Inventor's name", "PatentsView inventor's id", "Number of occurence"  , "Number of patents" ,"Number of US patents citations" ,  "Number of related citations"]).T[:size].style.hide(axis="index")


    
    
def map_inventors(technologies, number_technology , carbon_related , category):
    display = False
    dic_patents = related_patents(number_technology , category, carbon_related , display)
    dic_patents_co_inventors = {}
    count = 0
    
    for patent in dic_patents:
        for k in range(len(dic_patents[patent]["list_inventors"])):
            
            dic_patents_co_inventors[count] = {}
            
            dic_patents_co_inventors[count]["Latitude"] = dic_patents[patent]["list_inventors"][k]["inventor_latitude"]
            dic_patents_co_inventors[count]["Longitude"] = dic_patents[patent]["list_inventors"][k]["inventor_longitude"]

            count += 1
                
    if dic_patents_co_inventors == {}:
        return "No patent, select other key words"
    
    
    map_df = pd.DataFrame(dic_patents_co_inventors).T
    map_df["longitude"]=map_df['Longitude'].astype(float)
    map_df['latitude']=map_df['Latitude'].astype(float)
    map_df = map_df[map_df["latitude"].notnull()]

    return map_df

    #geometry = [Point(xy) for xy in zip(map_df['Longitude'], map_df['Latitude'])]
    #gdf = GeoDataFrame(map_df, geometry=geometry)   

    #this is a simple map that goes with geopandas
    #world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    #gdf.plot(ax=world.plot( color='white', edgecolor='black' ), marker='o', color='red', markersize=15 , zorder = 1);
    #plt.xlim([-180, 180])
    #plt.ylim([-90, 90])


    #plt.title("Main inventors: geographic location")
    #plt.xlabel("Longitude")
    #plt.ylabel("Latitude")
    #plt.show()

    
## Extract quantitative data

def extract_sentences_with_numbers(text , text_name):
    if text != None:
        text = text.replace("CO 2" , "CO2")
        text = text.replace("CO 3" , "CO3")
        text = text.replace("CO(2)" , "CO2")
        text = text.replace("CO(3)" , "CO3")
        
        print(text_name + ": " , text)
        print(" ")



        list_text = list(text)
        for i in range(1,len(list_text)-1):
            if list_text[i] == " " and list_text[i-1] == "." and list_text[i+1].isupper():
                list_text[i] = "~"

        text = "".join(list_text)
        text = text.split("~")
        for sentence in text:                

            if any(char.isdigit() for char in sentence):
                
                
                
                if "CO2" in sentence:
                    print("\x1b[31mCARBON RELATED:\x1b[0m", sentence)
                    print(" ")


                    
                if "GJ" in sentence or "MJ" in sentence:
                    print("\x1b[31mENERGY:\x1b[0m" , sentence)
                    print(" ")


                    
                ##price
                if "€"  in sentence or "$" in sentence or "EUR" in sentence or "dollars" in sentence.lower():
                    print("\x1b[31mPRICE:\x1b[0m" , sentence)
                    print(" ")


                    
                ##dates
                digits = []
                for word in sentence.replace("," , "").replace("%" , "").replace("." , " ").split():
                    if word.isdigit() and 1850 < int(word) < 2200 :
                        digits.append(word)
                if digits != []:
                    print("\x1b[31mDATE:\x1b[0m" , sentence)
                    print(" ")


                    
                ##CO quantity
                if "Mt" in sentence or "tC" in sentence or "t-C" in sentence:
                    print("\x1b[31mCARBON QUANTITY:\x1b[0m" , sentence)
                    print(" ")
 
    print(" ")
          
    
def extract_quantitative_data_technology(technologies, number_technology):
    count = 0
      
    name_file = "iea"
    dic_target = deployment_target(name_file , False)
    dic_cost = cost_reduction_target(name_file , False)
    dic_details = details(name_file , False)
    sentences = 'No information'
    
    if number_technology in dic_details:
        reference_text = dic_details[number_technology]
            
        print("\033[96mFROM IEA website: ")
        print("\033[92mTechnology details: \x1b[0m" , reference_text)
        print(" ")
        encoded_text = model.encode(reference_text, convert_to_tensor=False).tolist()

    if number_technology in dic_target:
        cost_target_text = dic_target[number_technology]
        print("\033[96mFROM IEA website: ")
        sentences = extract_sentences_with_numbers(cost_target_text , "\033[92mDeployment target and Announced development target\x1b[0m")

    if number_technology in dic_cost:
        cost_text = dic_cost[number_technology]
        print("\033[96mFROM IEA website: ")
        sentences = extract_sentences_with_numbers(cost_text , "\033[92mAnnounced cost reduction targets\x1b[0m")
    
    return reference_text, sentences


        
def extract_quantitative_data_patent(patent_id):
    

    patent_id = patent_id[3:]
        
    url = "https://api.patentsview.org/patents/query?q={%22patent_id%22:%22" + str(patent_id) + "%22}&f=[%22patent_number%22,%22patent_title%22,%22patent_abstract%22,%22patent_date%22,%22inventor_last_name%22,%22inventor_first_name%22,%22assignee_organization%22]"
    url_google = "https://patents.google.com/patent/US" + str(patent_id)
    
    data = get_data(url)["patents"][0]
    title = data["patent_title"]
    abstract = data["patent_abstract"]
    co_inventors = ", ".join([ data["inventors"][i]["inventor_first_name"] + " " + data["inventors"][i]["inventor_last_name"] for i in range(len(data["inventors"])) ]) 
    assignees =  ", ".join([ str(data["assignees"][i]["assignee_organization"]) for i in range(len(data["assignees"])) ] )

    return url_google , title , abstract , data["patent_date"] , co_inventors , assignees





    
        
    

################################### Extracted texts ###############################################################

#@title Which patents are related to the technology?
def finder():
    name_file = 'iea'

    res = technology("iea", False )
    list_categories_tech = []
    list_categories = key_words(name_file , False)
    list_technologies = [ ( ", ".join(list_categories[i][1]) , i ) for i in range(len(list_categories))  ] 

    dic_technologies = {}
    for i in range(len(res)):
        names = res[i][1]
        if ", ".join(names) not in list_categories_tech:
            list_categories_tech.append(", ".join(names))
            dic_technologies[", ".join(names)] = []
        dic_technologies[", ".join(names)].append( (", ".join(list_categories[i][1]) , i ))
        

    list_climate = [ ("Any related patents" , False ) , ("Climate related patents" , True)]

    dic_categories = {}
    for elem in list_technologies:
        list_words = elem[0].split(",")[-3:]

        dic_categories[elem[1]]  = [  " ".join(list_words[-1].split()[:3]) ,  " ".join(list_words[-2].split()[:3]) if len(list_words) > 1 else "" ,  " ".join(list_words[-3].split()[:3]) if len(list_words) > 2 else ""  ]  
    
    return dic_technologies, dic_categories, list_categories_tech, list_technologies
                                       
# technologies_widget = widgets.Dropdown(options=list_categories_tech, 
#                                             description="Choose the category:" , 
#                                             style = {'description_width':'initial' } , 
#                                             layout=Layout(width='500px'));

# category_widget = widgets.RadioButtons( values = 1,
#                                         description='Patents where the abstract contains:' , 
#                                         style = {'description_width':'initial' } , 
#                                         layout=Layout(width='1000px'));
                                       
# number_technology_widget = widgets.Dropdown(options=list_technologies, 
#                                             description="Choose the technology:" , 
#                                             style = {'description_width':'initial' } , 
#                                             layout=Layout(width='500px'));

# def update_category(*args):
#     category_widget.options = dic_categories[number_technology_widget.value]
    
# def update_technology(*args):
#     number_technology_widget.options = dic_technologies[technologies_widget.value]
    
                                       
# number_technology_widget.observe(update_category)
# technologies_widget.observe(update_technology)

# print("Which patents are related to the technology?")
# interact_manual(get_ranking_patents, 
#                 technologies=technologies_widget,
#                 number_technology= number_technology_widget ,    
#                 carbon_related=widgets.Dropdown(options=list_climate, 
#                                                 description="Select the type of patents:" , 
#                                                 style = {'description_width':'initial' }   , 
#                                                 layout=Layout(width='500px')  ) , 
#                 size = widgets.IntSlider(min=3, 
#                                          max=100, 
#                                          value=10, 
#                                          step=1, 
#                                          description="Select the number of patents:" ,  
#                                          style = {'description_width':'initial' } , 
#                                          layout=Layout(width='500px')),
#                category = category_widget);
