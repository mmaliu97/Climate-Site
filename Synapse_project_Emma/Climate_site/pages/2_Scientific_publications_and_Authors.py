
import streamlit as st

st.set_page_config(page_title="Scientific publications and authors", page_icon="📖")


from streamlit_folium import folium_static
import folium
import pandas as pd
#from python_scripts import functions
from python_scripts import paper_functions
from python_scripts import others



header = st.container()

paper_finder = st.container()


with paper_finder:
    
  
  st.markdown("# Scientific publications and authors related to IEA technologies")
  st.sidebar.header("Scientific publications and authors")
  st.write(
        """You can find the most related scientific publications and authors for each climate related IEA technology. Enjoy!"""
    )

  st.header('Which papers are related to the technology?')


  st.subheader("Select the technology you want to look at")
  dic_technologies, dic_categories, list_categories_tech, list_technologies = paper_functions.finder()

  list_technologies = [ ( list_categories_tech[i] , i ) for i in range(len(list_categories_tech))  ] 
  key0 = lambda t: t[0]
    
    
   # Choose the category
  tech_category = st.selectbox('Select a category',list_technologies, format_func = key0)

    
  # After a selection is made the choices will update
  # Choose the technology and number
  technologies = dic_technologies[tech_category[0]]

  technology = st.selectbox('Select a technology',technologies,format_func = key0)
  

  # Select whether or not to use keywords
  list_keyword_option = [ ("No pre-select them for me" , False) , ("Yes" , True )]
  list_keyword_bool = st.selectbox('Would you like to enter your own keywords?',list_keyword_option,format_func = key0)

  if list_keyword_bool[1] == True:
    tech_category_keyword = st.text_input("Keywords", 'Input your text here')
  else:
    tech_categories = dic_categories[technology[1]]
    tech_category_keyword = st.radio(
      "Select a keyword to search on: ",
      tech_categories)

    
  # Select type of papers (related to climate or not)
  list_climate = [ ("Any related papers" , False ) , ("Climate related papers" , True)]
  patent_type_bool = st.selectbox('What type of papers do you want?',list_climate,format_func = key0)

  st.subheader("Look at the related scientific publications and authors")
  #try:
  #if st.button('Get more information about the technology'):
  reference_text, sentences = paper_functions.extract_quantitative_data_technology(
  technologies = technology[0],
  number_technology = technology[1],
  )
  
  st.write(f'<p style="color:Blue"> From IEA Website: <p style="color:Black"> <strong>Technology details:</strong> {reference_text}' , unsafe_allow_html = True)
  st.write(f'<p style="color:Blue"> From IEA Website: <p style="color:Black"> <strong>Deployment target and Announced development target:</strong> {sentences}' , unsafe_allow_html = True)
  st.write(f'<p style="color:Blue"> From IEA Website: <p style="color:Black"> <strong>Announced cost reduction targets:</strong> {sentences}' , unsafe_allow_html = True)

  #except:
  #  st.write("No information about the technology")
    


  #try:
  if st.button('Get related papers'):
     paper_rank_df = paper_functions.get_ranking_related_papers(
     technologies = tech_category[1],
     number_technology = technology[1],
     research_words = tech_category_keyword,
     carbon_related = patent_type_bool[1],
     size = 10
     )
     st.dataframe(paper_rank_df)
        #print(paper_rank_df)
  #except:
  #  st.write("No paper found, try with other key words")
        
  #try:  
  if st.button('Get the main authors'):
     authors = paper_functions.main_authors(
     technologies = tech_category[1],
     number_technology = technology[1],
     research_words = tech_category_keyword,
     carbon_related = patent_type_bool[1],
     size = 10
     )
     st.dataframe(authors)
     #print(patent_rank_df)
#      
 # except:
 #   st.write("No author found, try with other key words")
  
  #      
  #try:
    
  if st.button('Get the map of the main authors'):
    map_author = paper_functions.map_authors(
    technologies = tech_category[1],
    number_technology = technology[1],
    research_words = tech_category_keyword,
    carbon_related = patent_type_bool[1],
    size = 20)
    #st.map(map_author)
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
  #  st.write("No author found, try with other key words")
  #      
  #      
  #
  
  
  #      
  #      
  #      
  if st.button('Get more information about the related_projects'):
    try:
      reference_text,key_initiative,location_entities,papers = paper_functions.related_projects(
      technologies = technology[0], 
      number_technology = technology[1], 
      carbon_related= patent_type_bool[1], 
      size = 10)
      
      st.write(f'<p style="color:Blue"> From IEA Website:' , unsafe_allow_html = True)
      st.write(f'<strong>Technology details:</strong>  {reference_text}' ,  unsafe_allow_html = True)
      st.write(f'<strong>Technology key initiative:</strong> {key_initiative}' ,  unsafe_allow_html = True)
      st.write(f'<strong>Extracted projects and organization name:</strong> {location_entities}' ,  unsafe_allow_html = True)
      st.write(f'<p style="color:Red"> From OpenAlex Website:' , unsafe_allow_html = True)
      st.dataframe(papers)
    except:
       try:
          st.write(f'<p style="color:Blue"> From IEA Website:' , unsafe_allow_html = True)
          st.write(f'<strong>Technology details:</strong>  {reference_text}' , unsafe_allow_html = True)
          st.write(f'<strong>Technology key initiatives:</strong> {key_initiative}' ,  unsafe_allow_html = True)
          st.write(f'<strong>Extracted projects and organization name:</strong> {location_entities}' ,  unsafe_allow_html = True)
          st.write(f'<p style="color:Red"> From OpenAlex Website:' , unsafe_allow_html = True)
          st.write(f'No related paper found')
       except:
          st.write("No key initatives found")
          
          
  try:
    paper_id = st.text_input("More data on a paper?", 'Enter an OpenAlex paper id (ex: W100000)')
    url , title , abstract , date , authors , institutions = paper_functions.extract_quantitative_data_paper(
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
  
