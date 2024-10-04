import streamlit as st

from rssched.app.utils.io import get_uploaded_data

st.title("Depots")

request, response, instance_name = get_uploaded_data()
