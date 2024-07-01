import streamlit as st
from utils import execute


# Inject custom CSS
st.markdown(
    """
    <style>
    .reportview-container {
        background: black;
        color: white;
    }
    .sidebar .sidebar-content {
        background: #333;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar inputs
customer = st.sidebar.text_input('Enter your name here:')
quiry = st.sidebar.text_input('Enter your Question here:')
submit_button = st.sidebar.button('Submit')

# Main window heading
st.header('Customer Support Agent for AutoGen')

# When the submit button is pressed
if submit_button:
    with st.spinner('Processing your request...'):
        result = execute(customer=customer, quiry=quiry)
        st.write(result)