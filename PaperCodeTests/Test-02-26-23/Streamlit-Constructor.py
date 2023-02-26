import streamlit as st


header = st.container()
function = st.container()
widget = st.container()

with header:
    st.title("This is the Streamlit Test for the Paper Functions")
    st.text("In this test, we will extract the quantitative data and implement the 'More Data on a Paper' widget")


with function:
    st.header("This is where we will test the function.")

with widget:
    st.header("This is where we will test teh widget.")