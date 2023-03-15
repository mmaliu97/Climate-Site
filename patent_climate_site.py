import streamlit as st
import pandas as pd
from python_scripts import functions
from python_scripts import patent_functions
from python_scripts import others


header = st.container()
patent_finder = st.container()

with patent_finder:
  st.header('Which patents are related to the technology?')
  dic_technologies, dic_categories, list_categories_tech, list_technologies = patent_functions.finder()
    
  list_technologies = [ ( list_categories_tech[i] , i ) for i in range(len(list_categories_tech))  ] 

  # Choose the category
    
  key0 = lambda t: t[0]

  tech_category = st.selectbox('Select a category',list_technologies,format_func = key0)
  st.write(f'You chose category {tech_category[1]}')

  # After a selection is made the choices will update
  # Choose the technology and number
  technologies = dic_technologies[tech_category[0]]

  # display only the tech name
  
  technology = st.selectbox('Select a category',technologies,format_func = key0)
  st.write(f'You chose the tech number {technology[1]}')
  
  #st.write(f'You chose the tech number {dic_technologies}')

  # display the categories
  tech_categories = dic_categories[technology[1]]
  tech_category_keyword = st.radio("Select a keyword to search on: ",tech_categories )
  st.write(f'You chose the key workds {tech_category_keyword}')

  # Select type of patent
  list_climate = [ ("Any related patents" , False ) , ("Climate related patents" , True)]
  patent_type_bool = st.selectbox('Select a category',list_climate,format_func = key0)
  st.write(f'You chose {patent_type_bool[1]}')

  
  #try:
  if st.button('Get related patents'):
      patent_rank_df = patent_functions.get_ranking_patents(
      technologies = tech_category[1],
      number_technology = technology[1],
      category = tech_category_keyword,
      carbon_related = patent_type_bool[1],
      size = 10
    )
      st.dataframe(patent_rank_df)
      print(patent_rank_df)
        
        
  if st.button('Get the main inventors patents'):
      patent_rank_df = patent_functions.main_inventors(
      technologies = tech_category[1],
      number_technology = technology[1],
      category = tech_category_keyword,
      carbon_related = patent_type_bool[1],
      size = 10
    )
      st.dataframe(patent_rank_df)
      print(patent_rank_df)
        
        
  if st.button('Get the map of the main inventors patents'):
      patent_rank_df = patent_functions.map_inventors(
      technologies = tech_category[1],
      number_technology = technology[1],
      category = tech_category_keyword,
      carbon_related = patent_type_bool[1],
      
    )
      st.map(patent_rank_df)
      print(patent_rank_df)
  #except NameError:
  #  st.write(f'No patents found')
  # st.write(f'list_categories_tech is {list_categories_tech}')
  # st.write(f'list_technologies is {list_technologies}')
  # st.write(f'dic_categories is {dic_categories}')
