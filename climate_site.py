"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import pandas as pd
from python_scripts import functions
from python_scripts import multi_input_functions

header = st.container()
dataset = st.container()
features = st.container()
patent_finder = st.container()

modelTraining = st.container()

# with header:
#   st.title('Climate-Site-napse')
#   user_input = st.text_input("insert patent id")

#   # test with 10167450 
#   patent_info, patent_url, patent_assignees, patent_inventors = functions.extract_quantitative_data_patent(user_input)
#   title = patent_info["patent_title"]
#   abstract = patent_info["patent_abstract"]
#   st.write(f'URL is {patent_url}')
#   st.write(f'The title of the patent is {title}')
  # st.write(f'The abstract of the patent is {abstract}')

  # st.write(f'The patent assignees are {patent_assignees}')
  # st.write(f'The patent inventors are {patent_inventors}')


with patent_finder:
  st.header('Which patents are related to the technology?')
  dic_technologies, dic_categories, list_categories_tech, list_technologies = multi_input_functions.finder()

  # Choose the category
  tech_category = st.selectbox('Select a category',list_categories_tech)
  st.write(f'You chose {tech_category}')

  # After a selection is made the choices will update
  # category_widget = dic_categories[option]
  # st.write(f'That belongs to the category {category_widget}')

  # Choose the technology and number
  technologies = dic_technologies[tech_category]

  # display only the tech name
  key = lambda t: t[0]
  technology = st.selectbox('Select a category',technologies,format_func = key)
  st.write(f'You chose {technology[0]}')
  
  # Select type of patent
  patent_type = st.selectbox('Select a category',['Any related patents', 'Climate related patents'])
  st.write(f'You chose {patent_type}')


  

  if st.button('Get related patents'):
    patent_rank_df = multi_input_functions.get_ranking_patents(
    technologies = technology[0],
    number_technology = technology[1],
    carbon_related = patent_type,
    category = tech_category,
    size = 10
  )
    st.dataframe(patent_rank_df)

  # st.write(f'list_categories_tech is {list_categories_tech}')
  # st.write(f'list_technologies is {list_technologies}')
  # st.write(f'dic_categories is {dic_categories}')

