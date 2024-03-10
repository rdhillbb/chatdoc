import sys
import streamlit as st
import json
sys.path.append("../")
from fileops.webfildload import upload_fileadmin ,is_valid_download_url
from fileops.uploadfldr import serverupload
from listfilesfunc import listdocs
# Initialize loading condition
dirload = False

# Example JSON structure for documents
# Load and process document data
# Assuming the JSON data is stored in a variable named `data_json`
def is_empty_or_spaces(s):
     return not s or not s.strip()
data_json = {
    'Accounting': ['c209d3be-4fc4-48c0-b553-974766f538a2', 'KVP Individual Return Engagement Letter'],
    'SKELETONOFTHOURHT': ['2307.15337'],
    'your_filecabinet_name': ['file', 'KVP Individual Return Engagement Letter'],
    'USAIDPOLICY': ['PA00K7SH'],
    # Add the rest of your JSON data here...
}
try:
    docs = listdocs()
    data_json = data = json.loads(docs)
    # Convert JSON keys to a list for the dropdown menu
    drawer_names = list(data_json.keys())

    # Streamlit interface
    st.title("File Upload Interface")

    # Dropdown menu for file drawer selection
    selected_drawer = st.selectbox("File Drawer Selection", drawer_names)

    # Text field for file drawer - updated by dropdown selection or user input
    file_drawer = st.text_input("File Drawer", value=selected_drawer)

    # Text field for file name
    file_name = st.text_input("File")

    # Send button
    if is_empty_or_spaces(file_drawer):
       st.write("Error: File Drawer Required")
    elif st.button("Send"):
        # On button click, print the selected file drawer and file name
       st.write(f"File Drawer: {file_drawer}")
       st.write(f"File: {file_name}")
       if is_valid_download_url(file_name):
          msg = upload_fileadmin(file_drawer, file_name)
          st.write(f"Result: {msg}")
       else:
          msg =  serverupload(file_drawer, file_name)
          st.write(f"Result: {msg}")
except Exception as e:
        st.write(f'<p style="color: blue;">Error: {str(e)}</p>', unsafe_allow_html=True)
        st.write('<p style="color: green;">Please check the backend server.</p>', unsafe_allow_html=True)
