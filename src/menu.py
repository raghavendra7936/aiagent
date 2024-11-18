import streamlit as st

def show_menu():
    # Sidebar navigation: Links
    # Check if data is loaded
    if "data_loaded" not in st.session_state:
        # Show initial menu with Load Data only
        st.sidebar.page_link("main.py", label="Home")
        st.sidebar.page_link("pages/load_data.py", label="Load Data")
    else:
        # Show full menu with Load Data and Search options
        st.sidebar.page_link("main.py", label="Home")
        st.sidebar.page_link("pages/load_data.py", label="Load Data")
        st.sidebar.page_link("pages/search.py", label="Search")