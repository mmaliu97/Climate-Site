import streamlit as st

st.set_page_config(page_title="Search papers with your own technology", page_icon="🙋‍♀️")

import pandas as pd
from python_scripts import paper_functions_own_details
from streamlit_folium import folium_static
import folium



header = st.container()

own_paper_finder = st.container()


with own_paper_finder:
    
  
  st.markdown("# Scientific publications and authors related to your technology")
  st.sidebar.header("Scientific publications and authors")
  # st.subheader("Enter keywords related to the technology you are interest in")
  st.subheader("We are searching for the scientific publications which contain (in the title, abstract or text) the key words you can provide below:")
 
  key_words = st.text_input("Keywords", 'Input your text here')
  
  st.subheader("The scientific publications are ranked according to the similary between their abstract and the description you can provide below:")

  details = st.text_input("Details", 'Input your text here')
  
  size = st.slider('How many papers do you want?', 0, 200, 20)


  try:
    if st.button('Get related papers'):
       paper_rank_df = paper_functions_own_details.get_ranking_own_research(research_key_words = key_words,  details = details  , display= False , size=size)
 
       st.dataframe(paper_rank_df)
        #print(paper_rank_df)
  except:
    st.write("No paper found, try with other key words")
        
  #try:  
  if st.button('Get the main authors'):
     authors = paper_functions_own_details.main_authors(research_key_words = key_words,  details = details   , size=size)
     st.dataframe(authors)
  
  #except:
  #  st.write("No author found, try with other key words")
#  
#  #      
  #try:
#    
  if st.button('Get the map of the main authors'):
    map_author = paper_functions_own_details.map_authors(research_key_words = key_words,  details = details   , size=size)
    #st.map(map_author)
#  
    m = folium.Map(zoom_start = 1)
    dic_geo = {}
    for elem in map_author.index:
 
      longitude = map_author["longitude"][elem]
      latitude = map_author["latitude"][elem]
      if str(longitude) + " " + str(latitude) not in dic_geo:
        dic_geo[str(longitude) + " " + str(latitude)] = {}
        dic_geo[str(longitude) + " " + str(latitude)]["authors"] = map_author["author"][elem]
        dic_geo[str(longitude) + " " + str(latitude)]["institutions"] = map_author["institution"][elem]
        dic_geo[str(longitude) + " " + str(latitude)]["dates"] = map_author["date"][elem]
      else:
        dic_geo[str(longitude) + " " + str(latitude)]["authors"] += ", " + map_author["author"][elem]
        dic_geo[str(longitude) + " " + str(latitude)]["institutions"] +=  ", " + map_author["institution"][elem]
        dic_geo[str(longitude) + " " + str(latitude)]["dates"] += ", " + map_author["date"][elem]
        
    for elem in dic_geo:
        folium.Marker([float(elem.split()[1]), float(elem.split()[0])], popup="Author: " + dic_geo[elem]["authors"] + ", Institution: " + dic_geo[elem]["institutions"] + ", Date: " + dic_geo[elem]["dates"], tooltip=dic_geo[elem]["authors"]).add_to(m)
    folium_static(m)
           
  #except:
    #st.write("No author found, try with other key words")
  #      
#  #      
#  #
#  
#  
#  #      
#  #      
#  #      
#  if st.button('Get more information about the related_projects'):
#    try:
#      reference_text,key_initiative,location_entities,papers = paper_functions.related_projects(
#      technologies = technology[0], 
#      number_technology = technology[1], 
#      carbon_related= patent_type_bool[1], 
#      size = 10)
#      
#      st.write(f'<p style="color:Blue"> From IEA Website:' , unsafe_allow_html = True)
#      st.write(f'<strong>Technology details:</strong>  {reference_text}' ,  unsafe_allow_html = True)
#      st.write(f'<strong>Technology key initiative:</strong> {key_initiative}' ,  unsafe_allow_html = True)
#      st.write(f'<strong>Extracted projects and organization name:</strong> {location_entities}' ,  unsafe_allow_html = True)
#      st.write(f'<p style="color:Red"> From OpenAlex Website:' , unsafe_allow_html = True)
#      st.dataframe(papers)
#    except:
#       try:
#          st.write(f'<p style="color:Blue"> From IEA Website:' , unsafe_allow_html = True)
#          st.write(f'<strong>Technology details:</strong>  {reference_text}' , unsafe_allow_html = True)
#          st.write(f'<strong>Technology key initiatives:</strong> {key_initiative}' ,  unsafe_allow_html = True)
#          st.write(f'<strong>Extracted projects and organization name:</strong> {location_entities}' ,  unsafe_allow_html = True)
#          st.write(f'<p style="color:Red"> From OpenAlex Website:' , unsafe_allow_html = True)
#          st.write(f'No related paper found')
#       except:
#          st.write("No key initatives found")
#          
#          
  try:
    paper_id = st.text_input("More data on a paper?", 'Enter an OpenAlex paper id (ex: W100000)')
    url , title , abstract , date , authors , institutions = paper_functions_own_details.extract_quantitative_data_paper(
    work_id = paper_id)
    
    st.write(f'<p style="color:Red"> From OpenAlex Website:' , unsafe_allow_html = True)
    st.write(f'<p style="color:Black"> <strong> Paper link:</strong> <a href="url">{url}' , unsafe_allow_html = True)
    st.write(f'<strong> Paper title:</strong> {title}' , unsafe_allow_html = True)
    st.write(f'<strong> Paper abstract:</strong> {abstract}' , unsafe_allow_html = True)
    st.write(f'<strong> Paper date:</strong> {date}' , unsafe_allow_html = True)
    st.write(f'<strong> Paper co-inventors:</strong> {authors}' , unsafe_allow_html = True)
    st.write(f'<strong> Paper assignees:</strong> {institutions}' , unsafe_allow_html = True)
  #      
  except:
    st.write("Enter a valid work id")
