import streamlit as st
from send_post_request import send_post_request  # Import the modified function
from setchatdoc import setchatDoc
import json
import time
from listfilesfunc import listdocs

# Initialize loading condition
dirload = False

# Example JSON structure for documents
json_data = """
{
    "SKELETONOFTHOURHT": ["2307.15337"],
    "USAIDPOLICY": ["PA00K7SH"],
    "FIFDOCUMENT": ["FSD_BackOffice_LouiseV2-06012022", "User Manual Guide Produktif v.1.0", "FD Microfinance App_v1.2", "chroma_db"],
    "CHAINOFTHOUGHT": ["2201.11903"],
    "GARLIC": ["Garlic_ Proven health benefits and uses"],
    "OFTHOUGHTSK": ["2307.15337"]
}
"""

# Load and process document data
if not dirload:
    print(listdocs())
    docs = listdocs()
    data = json.loads(docs)
    print("_------------")
    print(json.loads(docs))
    dirload = True

# Main function to run the Streamlit app
def main():
    st.title("Chat with Doc")
    
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
                    rsp = setchatDoc(f"/{label}/{selected_option}")
                    print(f"{label}: {selected_option}")
                    st.session_state['previous_selections'][label] = selected_option
    
    # User input and send button
    user_input = st.text_input("Type your message here:", "")
    send_button = st.button("Send")
    
    # Process and display response to user input
    if send_button and user_input:
        response = send_post_request("message", user_input)
        if response['requestType'] == "Error":
            st.write("Response:", response['error'])
        elif "content" in response:
            st.write("Response:", response["content"])
        else:
            st.write("Received an unexpected response:", response)

# Execute the main function
if __name__ == "__main__":
    main()

