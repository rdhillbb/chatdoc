import streamlit as st
from listfilesfunc  import listdocs
from send_post_request import send_post_request  # Import the modified function

st.title("Chat with Doc")

# List of strings for button labels
#button_labels = ["Button 1", "Button 2", "Button 3"]  # Example button labels
button_labels = listdocs()
print(button_labels)
# Create a session state to hold the last pressed button if it doesn't already exist
if 'last_pressed' not in st.session_state:
    st.session_state['last_pressed'] = ""

# Function to set the last pressed button in session state
def set_last_pressed(label):
    st.session_state['last_pressed'] = label

# Generate buttons and their messages side by side
for label in button_labels:
    col1, col2 = st.columns([1, 3])  # Adjust the ratio as needed
    with col1:
        if st.button(label):
            set_last_pressed(label)
    with col2:
        if st.session_state['last_pressed'] == label:
            st.write(f"You pressed: {label}")

# Display the chat input and send button
user_input = st.text_input("Type your message here:", "")
send_button = st.button("Send", key="send")

# When the send button is clicked, process the user input
if send_button and user_input:
    response = send_post_request("message", user_input)
    if response['requestType'] == "Error":
        st.write("Response:", response['error'])
    elif "content" in response:
        st.write("Response:", response["content"])
    else:
        st.write("Received an unexpected response:", response)

