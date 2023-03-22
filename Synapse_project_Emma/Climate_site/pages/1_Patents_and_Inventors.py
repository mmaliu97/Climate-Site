import streamlit as st
import pandas as pd
#from python_scripts import functions
from python_scripts import patent_functions
from python_scripts import others

st.set_page_config(page_title="Patents and Inventors", page_icon="📖")

st.markdown("# Patents and Inventors related to IEA technologies")
st.sidebar.header("Patents and Inventors")
st.write(
        """You can find the most related patents and inventors for each climate related IEA technology. Enjoy!"""
    )

header = st.container()
patent_finder = st.container()

with patent_finder:
    

  st.subheader("Select the technology you want to look at")
  dic_technologies, dic_categories, list_categories_tech, list_technologies = patent_functions.finder()
    
  list_technologies = [ ( list_categories_tech[i] , i ) for i in range(len(list_categories_tech))  ] 
  key0 = lambda t: t[0]
    
    
  # Select the category  
  tech_category = st.selectbox('Select a category',list_technologies,format_func = key0)

    
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

    
  # Select type of patent (related to climate or not)
  list_climate = [ ("Any related patents" , False ) , ("Climate related patents" , True)]
  patent_type_bool = st.selectbox('What type of patent do you want?',list_climate,format_func = key0)

  
  #try:

  st.subheader("Look at the related patents and inventors")
    
  if st.button('Get more information about the technology'):
    reference_text, sentences = patent_functions.extract_quantitative_data_technology(
    technologies = technology[0],
    number_technology = technology[1],
  )
    
    st.write(f'<p style="color:Blue"> From IEA Website: <p style="color:Black"> <strong>Technology details:</strong> {reference_text}' , unsafe_allow_html = True)
    st.write(f'<p style="color:Blue"> From IEA Website: <p style="color:Black"> <strong>Deployment target and Announced development target:</strong> {sentences}' , unsafe_allow_html = True)
    st.write(f'<p style="color:Blue"> From IEA Website: <p style="color:Black"> <strong>Announced cost reduction targets:</strong> {sentences}' , unsafe_allow_html = True)

    
  try:
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
  except:
    st.write("No patent found, try with other key words")
        
  try:  
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
        
  except:
    st.write("No inventor found, try with other key words")

        
  try:
      
      if st.button('Get the map of the main inventors patents'):
        patent_rank_df = patent_functions.map_inventors(
        technologies = tech_category[1],
        number_technology = technology[1],
        category = tech_category_keyword,
        carbon_related = patent_type_bool[1])
        st.map(patent_rank_df)
        print(patent_rank_df)
            
  except:
      st.write("No inventor found, try with other key words")
        
        
  

  try:
      patent_id = st.text_input("More data on a patent?", 'Enter a US patent (ex: US-100000)')
      url , title , abstract , date , co_inventors , assignees = patent_functions.extract_quantitative_data_patent(
      patent_id = patent_id)

      st.write(f'<p style="color:Black"> <strong> Patent link:</strong> <a href="url">{url}' , unsafe_allow_html = True)
      st.write(f'<p style="color:Blue"> From PatentsView Website:' , unsafe_allow_html = True)
      st.write(f'<strong> Patent title:</strong> {title}' , unsafe_allow_html = True)
      st.write(f'<strong> Patent abstract:</strong> {abstract}' , unsafe_allow_html = True)
      st.write(f'<strong> Patent date:</strong> {date}' , unsafe_allow_html = True)
      st.write(f'<strong> Patent co-inventors:</strong> {co_inventors}' , unsafe_allow_html = True)
      st.write(f'<strong> Patent assignees:</strong> {assignees}' , unsafe_allow_html = True)
        
  except:
    st.write("Enter a valid patent id")
        
        
        
   ## Get info about technology

  #except NameError:
  #  st.write(f'No patents found')
  # st.write(f'list_categories_tech is {list_categories_tech}')
  # st.write(f'list_technologies is {list_technologies}')
  # st.write(f'dic_categories is {dic_categories}')
