"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import pandas as pd
from python_scripts import functions
from python_scripts import paper_functions
from python_scripts import others


header = st.container()

paper_finder = st.container()


with paper_finder:
  st.header('Which papers are related to the technology?')
  dic_technologies, dic_categories, list_categories_tech, list_technologies = paper_functions.finder()

  # Choose the category
  tech_category = st.selectbox('Select a category',list_categories_tech)
  st.write(f'You chose {tech_category}')

  # After a selection is made the choices will update
  # Choose the technology and number
  technologies = dic_technologies[tech_category]

  # display only the tech name
  key0 = lambda t: t[0]
  technology = st.selectbox('Select a category',technologies,format_func = key0)
  st.write(f'You chose {technology[0]}')
  st.write(f'The number is {technology[1]}')
  # st.write(f'You chose the tech number {dic_categories}')
  # st.write(f'You chose the tech number {dic_technologies}')

  # Select type of patent
  list_climate = [ ("Any related papers" , False ) , ("Climate related papers" , True)]
  patent_type_bool = st.selectbox('Select a category',list_climate,format_func = key0)
  st.write(f'You chose {patent_type_bool[1]}')

  # Select whether or not to use keywords
  list_keyword_option = [ ("Yes" , True ) , ("No pre-select them for me" , False)]
  list_keyword_bool = st.selectbox('Would you like to enter your own keywords?',list_keyword_option,format_func = key0)

  if list_keyword_bool[1] == True:
    tech_category_keyword = st.text_input("Keywords", 'Input your text here')
  else:
    tech_categories = dic_categories[technology[1]]
    tech_category_keyword = st.radio(
      "Select a keyword to search on: ",
      tech_categories)
  
  ## Get matches
  try:
    if st.button('Get related papers'):
      paper_rank_df = paper_functions.get_ranking_related_papers(
      technologies = technology[0],
      number_technology = technology[1],
      carbon_related = patent_type_bool[1],
      research_words = tech_category_keyword,
      size = 10
    )
      st.dataframe(paper_rank_df)
  except NameError:
    st.write(f'No patents found')


  ## Get info about technology
  if st.button('Get more information about the technology'):
    reference_text, sentences = paper_functions.extract_quantitative_data_technology(
    technologies = technology[0],
    number_technology = technology[1],
  )
    st.write(f'From IEA Website, Technology details:  {reference_text}')
    st.write(f'From IEA Website, Deployment target and Announced development target {sentences}')
    st.write(f'From IEA Website, Announced cost reduction targets {sentences}')


  # ## Get more information about paper
  # st.write('Get more user input')
  #  # test with W2169337437
  # user_input = st.text_input("insert paper id",'W2169337437')
  # url, date, title, abstract, concepts, authors, institutions = paper_functions.extract_quantitative_data_paper(user_input)
  
  # st.write(f'Paper URL: {url}')
  # st.write(f'Paper date: {date}')
  # st.write(f'Paper title: {title}')
  # st.write(f'Paper abstract: {abstract}')
  # st.write(f'Paper concepts: {concepts}')
  # st.write(f'Paper authors: {authors}')
  # st.write(f'Paper institutions: {institutions}')


  ## Get related_projects
  if st.button('Get more information about the related_projects'):
    reference_text,key_initiative,location_entities = paper_functions.related_projects(
    technologies = technology[0], 
    number_technology = technology[1], 
    carbon_related= patent_type_bool[1], 
    size = 10)

    st.write(f'Technology details:  {reference_text}')
    st.write(f'Technology key initiatives {key_initiative}')
    st.write(f'Extracted projects and organization name {location_entities}')

  

  

