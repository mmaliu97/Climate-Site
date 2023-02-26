import streamlit as st
from python_scripts import test_script
from python_scripts import others


header = st.container()
function = st.container()
widget = st.container()

with header:
    st.title("This is the Streamlit Test for the Paper Functions")
    st.text("In this test, we will extract the quantitative data and implement the 'More Data on a Paper' widget")


with function:
    st.header("This is where we will test the function.")
    #input = st.text_input("Do you want the quantitative information corresponding to a paper?")
    st.write(test_script.interact_manual(test_script.extract_quantitative_data_paper  ,
                                         work_id= test_script.widgets.Text(value='W00000000' , description="Enter a work id from OpenAlex" ,
                                                                           style = {'description_width':'initial' }   ,
                                                                           layout=test_script.Layout(width='500px'))))

with widget:
    st.header("This is where we will test the widget.")