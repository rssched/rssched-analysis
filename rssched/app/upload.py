import streamlit as st

from rssched.app.utils.io import import_request, import_response

st.title("RSSched Analyzer")
st.markdown(
    """
### About
This page provides an aggregated summary of the request data uploaded by the user. 
You can see important statistics such as the number of locations, vehicle types, depots, 
routes, and other relevant metrics. Additionally, an objective value from the response is also displayed below.
"""
)

st.subheader("Upload Data")

# Session state to store file uploads
if "request_file" not in st.session_state:
    st.session_state.request_file = None
if "response_file" not in st.session_state:
    st.session_state.response_file = None

# Upload Request and Response Files
request_file = st.file_uploader(
    "Set request file (JSON)", type=["json"], key="request_uploader"
)
response_file = st.file_uploader(
    "Set response file (JSON)", type=["json"], key="response_uploader"
)

# If both files are uploaded, process them
if request_file is not None and response_file is not None:
    request_instance_name = ".".join(request_file.name.split(".")[:2])
    response_instance_name = ".".join(response_file.name.split(".")[:2])

    if request_instance_name != response_instance_name:
        st.warning(
            f"Instance of request '{request_instance_name}' and response '{response_instance_name}' not the same."
        )

    st.session_state.rssched_instance_name = request_instance_name
    st.session_state.request_file = request_file
    st.session_state.response_file = response_file
    st.session_state.instance_name = response_file
    st.session_state.request_data = import_request(st.session_state.request_file)
    st.session_state.response_data = import_response(st.session_state.response_file)

    st.success("Files uploaded and processed successfully!")


# Reset button to clear the uploaded files and session state
if st.button("Reset"):
    st.session_state.request_file = None
    st.session_state.response_file = None
    st.session_state.request_data = None
    st.session_state.response_data = None
    st.rerun()
