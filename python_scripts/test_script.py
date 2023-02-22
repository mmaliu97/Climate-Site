############## Imports #####################

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

# !python -m spacy download en_core_web_lg
spacy_nlp = spacy.load("en_core_web_lg")

import re

# !pip install sentence_transformers
from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('all-MiniLM-L6-v2'  )

import unicodedata

# !pip install metaphone
from metaphone import doublemetaphone

# !pip install fuzzywuzzy
from fuzzywuzzy import fuzz
from difflib import SequenceMatcher
import re

# !pip install geopandas
import geopandas as gpd
from geopandas import GeoDataFrame



############## General Functions #####################
def URL(base_URL , entity_type , filters):
    """
    Returns URL used in OpenAlex or PatentsView

    Parameters
    ----------
    base_URL : str, API string that starts with either OpenAlex or PatentsView
    entity_type: str, 
    filters: str, selection of fields to query

    Returns
    -------
    url: str, URL to connect to API
    """
    url = base_URL + entity_type + filters
    return url


def get_data(url):
    """Retrieves data from the URL which is in json file format

    Parameters
    ----------
    url : str, entire URL to connect to API
    """
    url = requests.get(url)
    text = url.text
    import json
    data = json.loads(text)
    return data

## encoding the abstract


def reconstruction_abstract(abstract_inverted_index):
    """Returns the abstract if abstract exists in the database, else return None

    Parameters
    ----------
    abstract_inverted_index : str, index of an abstract
    
    """    
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
    return sqrt(sum(x * x for x in vector))    

def cosine_similarity2(vec_a, vec_b):
        norm_a = norm(vec_a)
        norm_b = norm(vec_b)
        dot = sum(a * b for a, b in zip(vec_a, vec_b))
        return dot / (norm_a * norm_b)

############## Extract texts #####################

def print_extracted_text(name_file):
    """Print extracted text from a file

    File texts will be related to IEA technology data

    Parameters
    ----------
    name_file : str, name of the file
    
    """    
    file = open("/content/" + name_file + ".txt", "r")
    lines = file.readlines()
    count = 0
    for index, line in enumerate(lines):
        read_line = line.strip()
        print(read_line)

    file.close()
    
    
    
def details(name_file , display):
    """Print the details of the file

    File texts will be related to IEA technology data

    Parameters
    ----------
    name_file : str, name of the file
    
    """   
    
    file = open("/content/" + name_file + ".txt", "r")
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
    """Print the key iniatives of the file
    
    File texts will be related to IEA technology data

    Parameters
    ----------
    name_file : str, name of the file
    
    """   
    
    file = open("/content/" + name_file + ".txt", "r")
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

    """Print the deployment targets of the file
    
    File texts will be related to IEA technology data

    Parameters
    ----------
    name_file : str, name of the file
    
    """   
    
    file = open("/content/" + name_file + ".txt", "r")
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

    """Print the cost reduction targets of the file
    
    File texts will be related to IEA technology data

    Parameters
    ----------
    name_file : str, name of the file
    
    """   
    
    file = open("/content/" + name_file + ".txt", "r")
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

    """Print the key words of the file
    
    File texts will be related to IEA technology data

    Parameters
    ----------
    name_file : str, name of the file
    
    """   
    
    file = open("/content/" + name_file + ".txt", "r")
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

    """Print the technologies listed in the file
    
    File texts will be related to IEA technology data

    Parameters
    ----------
    name_file : str, name of the file
    
    """   
    ## change this based on your local path
    file = open("D:/UC Berkeley/Climate Site/Climate-Site/python_scripts/" + name_file + ".txt", "r") 
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

############## Function Patents ##################
############## Get Related Patents
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

############################ Extract quantitative data ###################################
   
def extract_quantitative_data_patent( patent_id):

    try: 
        url = "https://api.patentsview.org/patents/query?q={%22patent_id%22:%22" + str(patent_id) + "%22}&f=[%22patent_number%22,%22patent_title%22,%22patent_abstract%22,%22patent_date%22,%22inventor_last_name%22,%22inventor_first_name%22,%22assignee_organization%22]"
        data = get_data(url)["patents"][0]
        title = data["patent_title"]
        abstract = data["patent_abstract"]
        print("\033[96mFROM PATENTSVIEW:")
        print("\033[92mPatent link: \x1b[0m"  + url)
        print(" ")
        print("\033[92mTitle: \x1b[0m"  + title)
        print(" ")
        print("\033[92mAbstract: \x1b[0m"  + abstract)
        print(" ")
        print("\033[92mDate: \x1b[0m"  + data["patent_date"])
        print(" ")
        print("\033[92mInventors: \x1b[0m"   ,  ", ".join([ data["inventors"][i]["inventor_first_name"] + " " + data["inventors"][i]["inventor_last_name"] for i in range(len(data["inventors"])) ]) )
        print(" ")
        print("\033[92mAssignee: \x1b[0m" , ", ".join( [ str(data["assignees"][i]["assignee_organization"]) for i in range(len(data["assignees"])) ] ) )

    except:
        print("Enter a valid patent_id from PatentsView")
    


#################################### Rank Patents ########################################
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





def get_ranking_patents(technologies, number_technology ,  carbon_related ,category, size):
    dic_patents = ranking_patents(number_technology , category, carbon_related , False)
    if dic_patents == {}:
        return "No patent found, select other key words"

    elif dic_patents == "Select other key words":
        return dic_patents
    
    else:
        return pd.DataFrame(dic_patents).T.sort_values(by="abstract comparison" , ascending = False)[:size]
    

################################## Main Inventors ########################################
def main_inventors(technologies, number_technology , carbon_related , category , size ):
    
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
            
        
                
                
        return pd.DataFrame(dic_patents_co_inventors , index = ["Inventor's name", "PatentsView inventor's id", "Number of occurence"  , "Number of patents" ,"Number of US patents citations" ,  "Number of related citations"]).T[:size].style.hide_index()


def map_inventors(technologies, number_technology , carbon_related , category):
    
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
    map_df['Longitude']=map_df['Longitude'].astype(float)
    map_df['Latitude']=map_df['Latitude'].astype(float)



    geometry = [Point(xy) for xy in zip(map_df['Longitude'], map_df['Latitude'])]
    gdf = GeoDataFrame(map_df, geometry=geometry)   

    #this is a simple map that goes with geopandas
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    gdf.plot(ax=world.plot( color='white', edgecolor='black' ), marker='o', color='red', markersize=15 , zorder = 1);
    plt.xlim([-180, 180])
    plt.ylim([-90, 90])


    plt.title("Main inventors: geographic location")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.show()

           
################################# Individual Functions #######################################

## Which papers are related to the technology?

#@title Which papers are related to the technology?

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
   

                                       
technologies_widget = widgets.Dropdown(options=list_categories_tech, 
                                            description="Choose the category:" , 
                                            style = {'description_width':'initial' } , 
                                            layout=Layout(width='500px'));

category_widget = widgets.RadioButtons( values = 1,
                                        description='Papers where the abstract contains:' , 
                                        style = {'description_width':'initial' } , 
                                        layout=Layout(width='1000px'));
                                       
number_technology_widget = widgets.Dropdown(options=list_technologies, 
                                            description="Choose the technology:" , 
                                            style = {'description_width':'initial' } , 
                                            layout=Layout(width='500px'));



def update_category(*args):
    category_widget.options = dic_categories[number_technology_widget.value]
    
def update_technology(*args):
    number_technology_widget.options = dic_technologies[technologies_widget.value]
    
                                       
number_technology_widget.observe(update_category)
technologies_widget.observe(update_technology)


print("Which papers are related to the technology?")
interact_manual(get_ranking_related_papers, 
                technologies = technologies_widget,
                number_technology= number_technology_widget ,    
                carbon_related=widgets.Dropdown(options=list_climate, 
                                                description="Select the type of papers:" , 
                                                style = {'description_width':'initial' }   , 
                                                layout=Layout(width='500px')  ) , 
                size = widgets.IntSlider(min=3, 
                                         max=100, 
                                         value=10, 
                                         step=1, 
                                         description="Select the number of papers:" ,  
                                         style = {'description_width':'initial' } , 
                                         layout=Layout(width='500px')),
               research_words = category_widget);
