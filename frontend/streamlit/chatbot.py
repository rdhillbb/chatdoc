import streamlit as st
from send_post_request import send_post_request  # Import the modified function

st.title("Chat with Doc")

# Create a text input box and a send button
user_input = st.text_input("Type your message here:", "")
send_button = st.button("Send")

# When the button is clicked, send the input to the backend and display the response
if send_button and user_input:  # Check if there is input and the button is pressed
    response = send_post_request(
        "message", user_input
    )  # Call the function with the user's message
    if response['requestType']=="Error":    
       st.write("Response:",response['error'])
    elif "content" in response:
        st.write("Response:", response["content"])  # Display the response content
    else:
        st.write("Received an unexpected response:", response)
