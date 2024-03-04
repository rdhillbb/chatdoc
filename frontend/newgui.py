from dotenv import load_dotenv
from pathlib import Path
import streamlit as st
from send_post_request import send_post_request  # Import the modified function
from setchatdoc import setchatDoc
import json
import time
from listfilesfunc import listdocs
dotenv_path = Path('.')
load_dotenv(dotenv_path=dotenv_path)
# Initialize loading condition
dirload = False

# Example JSON structure for documents
# Load and process document data
if not dirload:
    #print(listdocs())
    docs = listdocs()
    data = json.loads(docs)
    #print("_------------")
    #print(json.loads(docs))
    dirload = True
#docselect = ""
# Main function to run the Streamlit app
def main():
    st.title("Chat with Doc")
    if 'docselect' not in st.session_state:
        st.session_state['docselect'] = ""
    # Initialize session state for selections if not already set
    if 'previous_selections' not in st.session_state:
        st.session_state['previous_selections'] = {label: None for label in data.keys()}
    
    # Display dropdowns for document selection
    items = list(data.items())
    for i in range(0, len(items), 4):
        row_items = items[i:i+4]
        cols = st.columns(len(row_items))
        
        for col, item in zip(cols, row_items):
            label, options = item
            with col:
                selected_option = st.selectbox(label, ["Select an option..."] + options, key=label)
                
                # Check for new selections and update accordingly
                if selected_option != "Select an option..." and selected_option != st.session_state['previous_selections'].get(label):
                    #time.sleep(3)
                    #rsp = setchatDoc(f"/{label}/{selected_option}")
                    docselect = f"/{label}/{selected_option}"
                    st.session_state['docselect'] = f"/{label}/{selected_option}"
                    print(st.session_state['docselect'])
                    print(docselect)
                    print(f"{label}: {selected_option}--? /{label}/{selected_option}")
                    st.session_state['previous_selections'][label] = selected_option
    
    # User input and send button
    user_input = st.text_input("Type your message here:", "")
    send_button = st.button("Send")
    
    # Process and display response to user input
    if send_button and user_input:
        print(st.session_state['docselect'])
        response = send_post_request("message", user_input,st.session_state.get('docselect', ''))
        if response['requestType'] == "Error":
            st.write("Response:", response['error'])
        elif "content" in response:
            st.write("Response:", response["content"])
            print("--->Response",response["content"])
        else:
            st.write("Received an unexpected response:", response)

# Execute the main function
if __name__ == "__main__":
    main()

