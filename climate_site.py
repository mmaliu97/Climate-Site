"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import pandas as pd
from python_scripts import test_script
from python_scripts import others



header = st.container()
dataset = st.container()
features = st.container()
script_testing = st.container()

modelTraining = st.container()

with header:
  st.title('Climate-Site-napse')
  st.text(others.add(10,22))
  user_input = st.text_input("insert patent id")

  # test with 10167450 
  patent_info, patent_url, patent_assignees, patent_inventors = test_script.extract_quantitative_data_patent(user_input)
  title = patent_info["patent_title"]
  abstract = patent_info["patent_abstract"]
  st.write(f'URL is {patent_url}')
  st.write(f'The title of the patent is {title}')
  st.write(f'The abstract of the patent is {abstract}')

  st.write(f'The patent assignees are {patent_assignees}')
  st.write(f'The patent inventors are {patent_inventors}')


with script_testing:
  st.header('Here I will test scripts')
  number = others.other([10,270])
  st.text(f'Insert description here {number}')

