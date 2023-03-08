"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import pandas as pd
from python_scripts import functions
from python_scripts import others



header = st.container()
dataset = st.container()
features = st.container()
script_testing = st.container()

modelTraining = st.container()

with header:
  st.title('Climate-Site-napse')
  st.text(others.add(10,22))
  # test with W2169337437
  user_input = st.text_input("insert paper id")

  url, date, title, abstract, concepts, authors, institutions = functions.extract_quantitative_data_paper(user_input)
  
  st.write(f'Paper URL: {url}')
  st.write(f'Paper date: {date}')
  st.write(f'Paper title: {title}')
  st.write(f'Paper abstract: {abstract}')
  st.write(f'Paper concepts: {concepts}')
  st.write(f'Paper authors: {authors}')
  st.write(f'Paper institutions: {institutions}')
  

# with header:
#   st.title('Climate-Site-napse')
#   user_input = st.text_input("insert patent id")

  # test with 10167450 
  # patent_info, patent_url, patent_assignees, patent_inventors = test_script.extract_quantitative_data_patent(user_input)
  # title = patent_info["patent_title"]
  # abstract = patent_info["patent_abstract"]
  # st.write(f'URL is {patent_url}')
  # st.write(f'The title of the patent is {title}')
  # st.write(f'The abstract of the patent is {abstract}')

  # st.write(f'The patent assignees are {patent_assignees}')
  # st.write(f'The patent inventors are {patent_inventors}')

with script_testing:
  st.header('Here I will test scripts')
  number = others.other([10,270])
  st.text(f'Insert description here {number}')

  """
# My first app
Here's our first attempt at using data to create a table:
"""

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

  # Choose the category
  tech_category = st.selectbox('Select a category',list_categories_tech)
  st.write(f'You chose {tech_category}')

  # After a selection is made the choices will update
  # Choose the technology and number
  technologies = dic_technologies[tech_category]

  # display only the tech name
  key0 = lambda t: t[0]
  technology = st.selectbox('Select a category',technologies,format_func = key0)
  # st.write(f'You chose {technology[0]}')
  # st.write(f'You chose the tech number {technology[1]}')

  # display the categories
  tech_categories = dic_categories[technology[1]]
  tech_category_keyword = st.radio(
    "Select a keyword to search on: ",
    tech_categories)

  # Select type of patent
  list_climate = [ ("Any related patents" , False ) , ("Climate related patents" , True)]
  patent_type_bool = st.selectbox('Select a category',list_climate,format_func = key0)
  st.write(f'You chose {patent_type_bool[1]}')

  
  try:
    if st.button('Get related patents'):
      patent_rank_df = multi_input_functions.get_ranking_patents(
      technologies = technology[0],
      number_technology = technology[1],
      carbon_related = patent_type_bool[1],
      category = tech_category_keyword,
      size = 10
    )
      st.dataframe(patent_rank_df)
      print(patent_rank_df)
  except NameError:
    st.write(f'No patents found')
  # st.write(f'list_categories_tech is {list_categories_tech}')
  # st.write(f'list_technologies is {list_technologies}')
  # st.write(f'dic_categories is {dic_categories}')



