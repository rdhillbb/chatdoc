import streamlit as st
from listfilesfunc import listdocs
from send_post_request import send_post_request  # Import the modified function

st.title("Chat with Doc")

# Retrieve button labels from the listdocs function
button_labels = listdocs()  # Assuming this function returns a list of strings

# Define the layout for the buttons
max_buttons_per_row = 5
num_rows = -(-len(button_labels) // max_buttons_per_row)  # Ceiling division to get number of rows needed

# Create session state for last pressed button if it doesn't exist
if 'last_pressed' not in st.session_state:
    st.session_state['last_pressed'] = ""

# Function to update the last pressed button in session state
def set_last_pressed(label):
    st.session_state['last_pressed'] = label

# Dynamically generate buttons in rows
for row in range(num_rows):
    start_idx = row * max_buttons_per_row
    end_idx = start_idx + max_buttons_per_row
    row_labels = button_labels[start_idx:end_idx]
    
    cols = st.columns(len(row_labels))  # Create columns for the current row
    
    for idx, label in enumerate(row_labels):
        with cols[idx]:
            if st.button(label, key=f"btn_{row}_{idx}"):
                set_last_pressed(label)
                st.write(f"You pressed: {label}")

# Display the chat input and send button
user_input = st.text_input("Type your message here:", "")
send_button = st.button("Send", key="send_main")

# Process user input on button click
if send_button and user_input:
    response = send_post_request("message", user_input)
    if response['requestType'] == "Error":
        st.write("Response:", response['error'])
    elif "content" in response:
        st.write("Response:", response["content"])
    else:
        st.write("Received an unexpected response:", response)

