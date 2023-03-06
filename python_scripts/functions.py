##packages code
import pandas as pd
import numpy as np
import json, requests 
import pandas as pd
from pandas.io.json import json_normalize

import spacy
#!python -m spacy download en_core_web_lg
spacy_nlp = spacy.load("en_core_web_lg")

#################### Test Scripts #############################

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

################################### Extracted texts ###############################################################

def extract_quantitative_data_paper( work_id):
    

    try:
        url = "https://api.openalex.org/works/" + str(work_id)
        data = get_data(url)
        date = data["publication_date"]
        title = data["title"]
        abstract = reconstruction_abstract(data["abstract_inverted_index"])
        concepts = ", ".join( [elem["display_name"] for elem in data["concepts"]] )
        authors = ", ".join( [elem["author"]["display_name"] for elem in data["authorships"]] )
        institutions = ", ".join( set([elem["institutions"][0]["display_name"] for elem in data["authorships"]]) )
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
        # sentences = extract_sentences_with_numbers(abstract , "\033[92mAbstract\x1b[0m")
        return [url, date, title, abstract, concepts, authors, institutions]
    except:
        print("Enter a valid work id from OpenAlex")
        
   
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
        assignees = ', '.join( [ str(data["assignees"][i]["assignee_organization"]) for i in range(len(data["assignees"])) ] )
        inventors = ", ".join([ data["inventors"][i]["inventor_first_name"] + " " + data["inventors"][i]["inventor_last_name"] for i in range(len(data["inventors"])) ])
    except:
        print("Enter a valid patent_id from PatentsView")

    return data, url, assignees, inventors
    

#print("Do you want the quantitative information corresponding to a paper?")