import os
import json
import streamlit as st
import time
from menu import show_menu
from langchain.agents import load_tools, initialize_agent, AgentType
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq.chat_models import ChatGroq

# set the page title
st.set_page_config(layout="wide", page_title="AI Assistant Company Search", page_icon=":robot_face:")

# Function to search for the query
def search(query):
    prompt = ChatPromptTemplate.from_messages(
        [
            ("assistant", "You are a helpful assistant."), ("human", query), 
        ]
    ) 
    response = None
    try:
        response = agent.invoke(prompt.messages)
    except Exception as e:
        print(f"An error occurred during search: {e}")
    if response is None:
        assistant_response = "I'm sorry, I couldn't find any information on that. Try with different prompt."
    else:
        assistant_response = response['output']
    return assistant_response

# LLM configuration
llm = ChatGroq(
    api_key = os.environ['GROQ_API_KEY'],
    model_name = "mixtral-8x7b-32768",
    temperature=0
)
# Add the tools
tool_names =['serpapi']
tools = load_tools(tool_names, os.environ["SERPAPI_API_KEY"])
agent=initialize_agent(tools,llm, agent="zero-shot-react-description", verbose=True)


# Rate limit configuration and avoid throttling calculation
groq_rate_limit = int(os.environ['GROQ_MAX_LIMIT'])  # Requests per minute
serpapi_rate_limit = int(os.environ['SERPAPI_MAX_LIMIT'])  # Requests per hour
time_between_requests_groq = 60 / groq_rate_limit  # Time to wait between requests
time_between_requests_serpapi = 3600 / serpapi_rate_limit  # Time to wait between requests
time_between_requests = time_between_requests_groq if time_between_requests_groq > time_between_requests_serpapi else time_between_requests_serpapi

show_menu()
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.write("# Company Search :office:")
if "selected_column" not in st.session_state:
    with st.expander("You have not loaded the data yet. Please load the data and select the column."):
        st.write("Click the Confirm button to load the data.")

    # Button to simulate confirming and redirecting
        if st.button("Confirm"):
            time.sleep(1)
            st.switch_page("pages/load_data.py")
else:
    st.write("Enter your query to search more on the uploaded company database for all records using the selected column. For ex: What is the revenue of {CompanyName} for the quarter ending Sep 2024?")
    st.write("You have currently selected the column '{0}'. This column value will be substituted in your prompt for the corresponding entities as listed in the uploaded database".format(st.session_state.selected_column))
    for role, message in st.session_state.chat_history:
        with st.chat_message(role):
            st.markdown(message)

    user_prompt = st.chat_input("Enter your query here.")
    if user_prompt:
        # need to add a loop for the companies in the uploaded_data
        df = st.session_state.uploaded_data
        # Show a spinner with a running message
        with st.spinner("Processing your request..."):
            # iterate through the values of the df for the selected column
            # check if user_prompt contains the selected_column in the format {selected_column}
            
            if "{{{0}}}".format(st.session_state.selected_column) in user_prompt:
                # custom search; replace the selected column with column values
                entityCount = df[st.session_state.selected_column].count()
                counter = 0
                for companyName in df[st.session_state.selected_column].values:
                    counter += 1
                    params = {st.session_state.selected_column: companyName}
                    user_query = user_prompt.format(**params)
                    st.chat_message("user").markdown(user_query)
                    st.session_state.chat_history.append(('human', user_query))       
                    assistant_response = search(user_query)
                    st.session_state.chat_history.append(("assistant", assistant_response))
                    with st.chat_message("assistant"):
                        st.markdown(assistant_response) # assistant_response
                    if counter < entityCount:
                        time.sleep(time_between_requests)
            else:
                # normal search
                st.chat_message("user").markdown(user_prompt)
                st.session_state.chat_history.append(('human', user_prompt))       
                assistant_response = search(user_prompt)
                st.session_state.chat_history.append(("assistant", assistant_response))
                with st.chat_message("assistant"):
                    st.markdown(assistant_response) # assistant_response
