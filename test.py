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
  st.text('Insert description here')

with script_testing:
  st.header('Here I will test scripts')
  number = others.other([10,270])
  st.text(f'Insert description here {number}')

