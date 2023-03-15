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

        if line.split(" 	")[-1] == "Details":
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


#################### Paper Functions #############################

def related_papers(number_technology , list_categories , carbon_related , display  , key_words):
    """Returns a dictionary of data related to the papers the user chooses
    
    This is done through generating URLs to connect with OpenAlex API and parsing through the json file
    
    Parameters
    ----------
    number_technology : int, the index of the technology with respect to the 23 IEA technologies
    list_categories : str, an array of all the technologies related to the 23 IEA technologies
    carbon_related: bool, a setting to select papers related to carbon capture
    display:
    key_words: str, an array of keywords selected based off technology/ user input

    """   
    dic = {}

    max_count = 0
    base_URL_OA = f'https://api.openalex.org/'
    filter_works = f'works?'
    for element in list_categories[number_technology:number_technology+1]:
        

        filter_openalex = f"search=" + key_words


        if carbon_related == True:
            filter_openalex += "&filter=concepts.id:https://openalex.org/C132651083|https://openalex.org/C115343472|https://openalex.org/C530467964&per_page=100&mailto=emma_scharfmann@berkeley.edu"
        
        else:
            filter_openalex += "&per_page=100&mailto=emma_scharfmann@berkeley.edu"
            
            
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

def ranking_papers(number_technology,  dic_details , dic ,  list_categories , display , size ):
    """Returns a dictionary of data related to the papers the user chooses
    
    This is done through generating URLs to connect with OpenAlex API and parsing through the json file
    
    Parameters
    ----------
    number_technology : int, the index of the technology with respect to the 500+ IEA technologies
    dic_details : str, dictionary where key is index of technology with respect to 500+ IEA technolgies and values are the details related to the technologies
    
    dic: bool, a setting to select papers related to carbon capture
    list_categories: str, an array of keywords selected based off technology/ user input
    display: bool, chooses to display information or not
    size: str, an array of keywords selected based off technology/ user input

    """   
    
    dic_scores_papers = {}
    

    if display == True:
        print("Technology " + str(number_technology))
        print("Key words: " , list_categories[number_technology][1])
            
    if number_technology in dic_details:
        reference_text = dic_details[number_technology]
            
        if display== True:
            print("Technology details: " , reference_text)
            print(" ")
        encoded_text = model.encode(reference_text, convert_to_tensor=False).tolist()
        
        
        if len(dic) == 0:
            return "No paper found, select other key words" 
        
        
        for ids in list(dic.keys()):

            dic_scores_papers[ids] = {}
            
            if dic[ids]["title"] != None:
                encoded_title = model.encode(dic[ids]["title"], convert_to_tensor=False).tolist()
                score_title = cosine_similarity2(encoded_title, encoded_text)
            else:
                score_title = None

        

            if dic[ids]["abstract"] != None:
                encoded_abstract = model.encode(dic[ids]["abstract"], convert_to_tensor=False).tolist()
                score_abstract = cosine_similarity2(encoded_abstract, encoded_text)
            else:
                score_abstract = None


            #concepts = ""
            #for elem in dic[ids]["concepts"]:
            #    concepts += elem["display_name"] + " "
            #encoded_concepts = model.encode(concepts, convert_to_tensor=False).tolist()
            #score_concepts = cosine_similarity2(encoded_concepts, encoded_text)

            dic_scores_papers[ids]["title comparision"] = score_title
            dic_scores_papers[ids]["abstract comparision"] = score_abstract
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
            
            

        return dic_scores_papers
        


    else:
        return "No description given"



def get_ranking_related_papers( technologies , number_technology , carbon_related , size , research_words):
    name_file = "iea"
    list_categories = key_words( name_file, False)
    dic_details = details(name_file , False)
    dic_related_papers = related_papers(number_technology , list_categories , carbon_related , False , research_words)
    dic_scores_papers = ranking_papers(number_technology,  dic_details , dic_related_papers ,  list_categories , False , size  )
    
    if dic_scores_papers == {}:
        return "No paper found"
    
    elif type(dic_scores_papers) == str:
        return dic_scores_papers
    
    else:
        return pd.DataFrame(dic_scores_papers).T.sort_values(by="abstract comparision" , ascending = False)[:size]
     

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
            
def extract_quantitative_data_paper( work_id):
    

    try:
        url = "https://api.openalex.org/works/" + str(work_id)
        data = get_data(url)
        date = data["publication_date"]
        title = data["title"]
        abstract = reconstruction_abstract(data["abstract_inverted_index"])
        concepts = ", ".join( [elem["display_name"] for elem in data["concepts"]] )
        authors = ", ".join( [elem["author"]["display_name"] for elem in data["authorships"]] )
        institutions = ", ".join( set([elem["institutions"][0]["display_name"] for elem in data["authorships"] if len(elem["institutions"]) > 0]) )
        print("\033[96mFROM OpenAlex: ")
        print("\033[92mPaper link: "  + url)
        print(" ")
        print("\033[92mTitle: \x1b[0m"  + title)
        print(" ")
        print("\033[92mConcepts: \x1b[0m"  + concepts)
        print(" ")
        print("\033[92mDate: \x1b[0m"  + date)
        print(" ")
        print("\033[92mAuthors: \x1b[0m"  + authors)
        print(" ")
        print("\033[92mInstitutions: \x1b[0m"  + institutions)
        print(" ")
        sentences = extract_sentences_with_numbers(abstract , "\033[92mAbstract\x1b[0m")
    except:
        print("Enter a valid work id from OpenAlex")
    

## Get papers related to cited projects

def related_projects(technologies, number_technology , carbon_related , size):

    name_file = "iea"
    dic_details = details(name_file , False)
    dic_key_initiatives = key_initiatives(name_file , False )
    
    
    dic2 = {}

    reference_text = dic_details[number_technology]
    print("\033[92mTechnology details: \x1b[0m" , reference_text)
    print(" ")
    encoded_text = model.encode(reference_text, convert_to_tensor=False).tolist()
     # reference_text key_initiative location_entities
    if number_technology in dic_key_initiatives:
        key_initiative = dic_key_initiatives[number_technology]
        print("\033[92mTechnology key initiatives: \x1b[0m" ,  key_initiative)

        location_entities = set()
        doc = spacy_nlp(key_initiative.strip())
        for j in doc.ents:
            entry = str(j.lemma_).lower()
            key_initiative = key_initiative.replace(str(j).lower(), "")
            if j.label_ in ["ORG"]:
                location_entities.add(j)
        print(" ")
        print("\033[92mExtracted projects and organizations names: \x1b[0m", location_entities)


        base_URL_OA = f'https://api.openalex.org/'
        filter_works = f'works?'
        for element in location_entities:

            filter_openalex = f"search=" 
            filter_openalex += str(element) 
            if carbon_related == True:
                filter_openalex += "&filter=concepts.id:https://openalex.org/C2780021121&per_page=200&mailto=emma_scharfmann@berkeley.edu"
            else:
                filter_openalex += "&per_page=200&mailto=emma_scharfmann@berkeley.edu"

            filter_openalex = filter_openalex.replace(" " , "%20")

            url = URL(base_URL_OA , filter_works, filter_openalex) 

            data = get_data(url)
            count = len(data)
            if count < 50:

                for k in range(count):
                    
                    if data["results"][k]["abstract_inverted_index"] != None:
                        encoded_abstract = model.encode(reconstruction_abstract(data["results"][k]["abstract_inverted_index"]) ,  convert_to_tensor=False).tolist()
                        abstract_similarity = cosine_similarity2(encoded_abstract, encoded_text)
                    else:
                        abstract_similarity = None
                        
                    if data["results"][k]["title"] != None:
                        encoded_title = model.encode(data["results"][k]["title"] ,  convert_to_tensor=False).tolist()
                        title_similarity = cosine_similarity2(encoded_title, encoded_text)
                    else:
                        title_similarity = None
                        
                    work_id = data["results"][k]["id"]
                    dic2[work_id] = {}
                    dic2[work_id]["project/institution name"] = str(element)
                    dic2[work_id]["title comparision"] = title_similarity
                    dic2[work_id]["abstract comparision"] = abstract_similarity

            else:

                key_word = list_categories[7]
                elem = key_word[1]

                string = ""
                for j in range(1,len(elem)):
                    if elem[j] == "CCUS":
                        elem[j] = "Carbon capture and storage"
                    string += elem[j]  + " " 


                string += str(element)
                filter_openalex = f"search="  + string 

                if carbon_related == True:
                    filter_openalex += "&filter=concepts.id:https://openalex.org/C2780021121&per_page=200&mailto=emma_scharfmann@berkeley.edu"
                else:
                    filter_openalex += "&per_page=200&mailto=emma_scharfmann@berkeley.edu"
                filter_openalex = filter_openalex.replace(" " , "%20")
                url = URL(base_URL_OA , filter_works, filter_openalex) 
                data = get_data(url)
                count = data["meta"]["count"]
                for k in range(count):
                    
                    if data["results"][k]["abstract_inverted_index"] != None:
                        encoded_abstract = model.encode(reconstruction_abstract(data["results"][k]["abstract_inverted_index"]) ,  convert_to_tensor=False).tolist()
                        abstract_similarity = cosine_similarity2(encoded_abstract, encoded_text)
                    else:
                        abstract_similarity = None
                        
                    if data["results"][k]["title"] != None:
                        encoded_title = model.encode(data["results"][k]["title"] ,  convert_to_tensor=False).tolist()
                        title_similarity = cosine_similarity2(encoded_title, encoded_text)
                    else:
                        title_similarity = None
                        
                    work_id = data["results"][k]["id"]
                    dic2[work_id] = {}
                    dic2[work_id]["project/institution name"] = str(element)
                    dic2[work_id]["title comparision"] = title_similarity
                    dic2[work_id]["abstract comparision"] = abstract_similarity
                    


        if dic2 != {}:
            return pd.DataFrame(dic2).T.sort_values(by="abstract comparision" , ascending = False)[:size]
        else:
            return "No paper found"

    else:
        return "No key initiatives given"

    return reference_text,key_initiative,location_entities

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


def main_authors(technologies,number_technology , carbon_related , size , research_words):
    
    name_file = "iea"
    list_categories = key_words( name_file, False)
    dic_details = details(name_file , False)
    dic_papers = related_papers(number_technology , list_categories , carbon_related , False , research_words)
    
    dic_papers_co_authors = {}
        


    for paper in dic_papers:

        for k in range(len(dic_papers[paper]["authorships"])):
            coauthor_id = dic_papers[paper]["authorships"][k]["author"]["id"]
            
            
            author_name = dic_papers[paper]["authorships"][k]["author"]["display_name"]
            author_name_norm = normalize(dic_papers[paper]["authorships"][k]["author"]["display_name"]).split()

            if len(author_name_norm ) > 0:
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
                        dic_papers_co_authors[author_name_norm]["Author's name(s)"] += ", " + author_name[0]
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
                    url = 'https://api.openalex.org/authors?filter=openalex_id:' + elem + "&page=1&per_page=200&mailto=emma_scharfmann@berkeley.edu"
                    data = get_data(url)["results"][0]
      
                    work_count += data["works_count"]
                    cited_by_count += data["cited_by_count"]
                    if data["last_known_institution"] != None and len(data["last_known_institution"]) > 0 and data["last_known_institution"]["display_name"] != None:
                        institutions += data["last_known_institution"]["display_name"]
                    
            dic_papers_co_authors[author_name_norm]["Last Known Institution"] = institutions
            dic_papers_co_authors[author_name_norm]["Number of works"] = work_count
            dic_papers_co_authors[author_name_norm]["Number of citations"] = cited_by_count

            
        return pd.DataFrame(dic_papers_co_authors, index = [ "Author's name(s)" , "Author's id(s)" ,  "Number of occurence within the 100 most related papers" , "Last Known Institution" , "Number of works" , "Number of citations" ,  "Number of related citations"]).T[:size].style.hide_index()

    else:
        return ("Select another category")


def map_authors(technologies, number_technology , carbon_related , size , category):

    name_file = "iea"
    list_categories = key_words( name_file, False)
    dic_details = details(name_file , False)
    dic_papers = related_papers(number_technology , list_categories , carbon_related , False , category)

    reference_text = dic_details[number_technology]
    
    encoded_text = model.encode(reference_text, convert_to_tensor=False).tolist()
    
    dic_papers_co_authors = {}
    count = 0
    

    for paper in list(dic_papers.keys())[:30]:
        
        if dic_papers[paper]["abstract"] != None:
            encoded_abstract = model.encode(dic_papers[paper]["abstract"], convert_to_tensor=False).tolist()
            score_abstract = cosine_similarity2(encoded_abstract, encoded_text)
        else:
            score_abstract = None

        for k in range(len(dic_papers[paper]["authorships"])):
            
            if dic_papers[paper]["authorships"][k]["institutions"] != [] and "id" in dic_papers[paper]["authorships"][k]["institutions"][0] and dic_papers[paper]["authorships"][k]["institutions"][0]["id"] != None:
                institution_id = dic_papers[paper]["authorships"][k]["institutions"][0]["id"]
                url = 'https://api.openalex.org/institutions?filter=openalex_id:' + institution_id + "&page=1&per_page=200&mailto=emma_scharfmann@berkeley.edu"
                try:
                  data = get_data(url)["results"][0]

                  dic_papers_co_authors[count] = {}
                  dic_papers_co_authors[count]["Longitude"] = data["geo"]["longitude"]
                  dic_papers_co_authors[count]["Latitude"] = data["geo"]["latitude"]
                  dic_papers_co_authors[count]["abstract comparision"] = score_abstract
                  count += 1
                except:
                  continue

                
                        
    if dic_papers_co_authors == {}:
        return "No papers"
    

    
    map_df = pd.DataFrame(dic_papers_co_authors,).T.sort_values(by="abstract comparision" , ascending = False)[:size]
    map_df['Longitude']=map_df['Longitude'].astype(float)
    map_df['Latitude']=map_df['Latitude'].astype(float)
    

    geometry = [Point(xy) for xy in zip(map_df['Longitude'], map_df['Latitude'])]
    gdf = GeoDataFrame(map_df, geometry=geometry)   

    #this is a simple map that goes with geopandas
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    gdf.plot(ax=world.plot( color='white', edgecolor='black' ), marker='o', color='red', markersize=15 , zorder = 1);
    
    plt.xlim([-180, 180])
    plt.ylim([-90, 90])


    plt.title("Main authors: geographic location" )
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.show()
       

################################### Extracted texts ###############################################################

#@title Which patents are related to the technology?
def finder():
    name_file = 'iea'
    res = technology("iea", False )
    list_categories_tech = []
    list_categories = key_words("iea" , False)
    list_technologies = [ ( ", ".join(list_categories[i][1]) , i ) for i in range(len(list_categories))  ] 
    dic_technologies = {}
    for i in range(len(res)):
        names = res[i][1]
        if ", ".join(names) not in list_categories_tech:
            list_categories_tech.append(", ".join(names))
            dic_technologies[", ".join(names)] = []
        dic_technologies[", ".join(names)].append( (", ".join(list_categories[i][1]) , i ))
        

    list_climate = [ ("Any related papers" , False ) , ("Climate related papers" , True)]

    dic_categories = {}
    for elem in list_technologies:
        list_words = elem[0].split(",")[-3:]
        for i in range(len(list_words)):
            if "CCUS" in list_words[i]:
                list_words[i] = list_words[i].replace("CCUS" , "carbon capture storage")
        dic_categories[elem[1]]  = [  ", ".join([ " ".join(words.split()[:3]) for words in list_words ] )  ,  ", ".join([ " ".join(words.split()[:3]) for words in list_words[:-1] ]) , ", ".join([ " ".join(words.split()[:3]) for words in list_words[1:] ] ) ]  
    
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
