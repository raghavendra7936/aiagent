import os
import json
import streamlit as st
from menu import show_menu

# Load the configuration data
workingdir = os.path.dirname(os.path.abspath(__file__))
configdata = json.load(open(os.path.join(workingdir, 'config.json'), 'r'))

GROQ_API_KEY = configdata['GROQ_API_KEY']
SERPAPI_API_KEY = configdata['SERPAPI_API_KEY']
GROQ_MAX_LIMIT = configdata['GROQ_MAX_LIMIT']
SERPAPI_MAX_LIMIT = configdata['SERPAPI_MAX_LIMIT']

# Set the environment variables
os.environ['GROQ_API_KEY'] = GROQ_API_KEY
os.environ["SERPAPI_API_KEY"] = SERPAPI_API_KEY
os.environ["GROQ_MAX_LIMIT"] = GROQ_MAX_LIMIT
os.environ["SERPAPI_MAX_LIMIT"] = SERPAPI_MAX_LIMIT

# Set the page config and welcome message
st.set_page_config(layout="wide", page_title="AI Assistant Company Search", page_icon=":robot_face:")
st.write("""# Welcome to AI Company Search Assistant :robot_face:
This is a simple Streamlit app that demonstrates how to use LangChain, Groq API and SerpApi to search for company information.

The app is divided into two sections: Load Data and Search. The Load Data section allows you to load data from a CSV file, while the Search section allows you to search for company information using the Groq and the SerpApi.
## How to use this app?
To get started, click on the Load Data link in the sidebar to load data from a CSV file. Once the data is loaded, you can click on the Search link in the sidebar to search for specific information through custom prompts for all the rows of the uploaded CSV.
         
Use the column dropdown to select the column you want to search information about the companies.
You can also click on the Home link in the sidebar to return to this page.
## Useful Prompts
Assuming CompanyName is the column in the csv, here are some useful prompts to get you started:

1. What is the latest quarter revenue of {CompanyName}?
1. Get the latest number of employees of {CompanyName}
1. Find the contact email address or phone number of {CompanyName} investor relations
1. What is the oustanding stock of {CompanyName}?
1. What is the latest stock price of {CompanyName} in Nasdaq?
""")
# Show the side bar menu
show_menu()