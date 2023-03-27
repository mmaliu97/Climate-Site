import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="🌎",
)

st.write("# Welcome to the Climate Synapse project! 🌎")

st.sidebar.success("👆 Select a type of document 👆")

st.markdown(
    """
    The Climate Synapse project is a platform which connects investors with early-stage entrepreneurs on climate related projects. 
    The idea is simple though challenging: connecting all these people, so that we can be more efficient in how we bring resources to bear on global warming?
    By creating greater visibility into technological innovation using new tools, we will see who’s doing what in technology areas that are critical to address the climate crisis. 
    We hope to accelerate innovation and integration of new technologies into the economy. 
    We used powerful tools of data analysis and machine learning to interrogate data that’s available, including published scientific research and patent databases.
    
    **👈 Select a type of document from the sidebar** to see some examples
    
    ### Want to learn more about our data?
    - Source of climate related technologies: [IEA website](https://www.iea.org/data-and-statistics/data-tools/etp-clean-energy-technology-guide?selectedTechs=)
    - Database of scientific publications: [OpenAlex](https://docs.streamlit.io)
   -  Database of patents: [PatentsView](https://patentsview.org/)
   

    ### You want to know more about what we are doing? 
    - Send us an email: emma_scharfmann@berkeley.edu
"""
)
