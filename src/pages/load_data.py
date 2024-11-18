import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from io import StringIO
from menu import show_menu

st.set_page_config(layout="wide", page_title="AI Assistant Company Search", page_icon=":robot_face:")

def show_preview():   
    if "uploaded_data" in st.session_state:
        upload_data_df = st.session_state.uploaded_data
        # Show CSV preview and column options
        st.write("To clear this previously uploaded data, upload a new CSV")
        st.write("Preview of the CSV (first 5 rows):")
        st.write(upload_data_df.head(5))

        # # Show the column names in a dropdown
        column_name = st.selectbox("Choose a column", upload_data_df.columns, key="columns")
        st.session_state.selected_column = column_name
        # Display the selected column name
        st.write(f"You selected the column: {column_name}")
        st.write("Here is the data in the selected column:")
        st.write(upload_data_df[column_name].head(5))

def upload_csv():
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    # Check if the file is uploaded
    if uploaded_file is not None:
        st.session_state.data_loaded = True # used to enable the search menu
        upload_data_df = pd.read_csv(uploaded_file)
        st.session_state.uploaded_data = upload_data_df
        uploaded_file = None

def get_data_gsheet(url):
    # Placeholder function to get data from Google Sheets
    # Create a connection object.
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read()
    st.session_state.data_loaded = True # used to enable the search menu
    st.session_state.uploaded_data = df
    show_preview()

# Main app interface
def main():
    # choose between CSV upload or Google Sheets
    st.write("# Load Data :cd:")
    option = st.radio("Choose a Data Source", ["Upload CSV", "Use Google Sheets"])

    if option == "Upload CSV":
        upload_csv()
        show_preview()
    elif option == "Use Google Sheets":
        with st.form(key='my_form'):
            # Text input for Google Sheets URL
            google_sheet_url = st.text_input("Enter Google Sheets URL")
            submit_button = st.form_submit_button(label='Go')
        # If the user enters a URL, we could (hypothetically) process it here
        if submit_button:
            get_data_gsheet(google_sheet_url)

    show_menu()

if __name__ == "__main__":
    main()
