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
  user_input = st.text_input("insert paper id")

  url, date, title, abstract, concepts, authors, institutions = functions.extract_quantitative_data_paper(user_input)
  
  st.write(f'Paper URL: {url}')
  st.write(f'Paper date: {date}')
  st.write(f'Paper title: {title}')
  st.write(f'Paper abstract: {abstract}')
  st.write(f'Paper concepts: {concepts}')
  st.write(f'Paper authors: {authors}')
  st.write(f'Paper institutions: {institutions}')
  



with script_testing:
  st.header('Here I will test scripts')
  number = others.other([10,270])
  st.text(f'Insert description here {number}')

