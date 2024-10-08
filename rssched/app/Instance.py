from io import BytesIO
from pathlib import Path
from typing import Optional, Tuple

import streamlit as st

from rssched.app.utils.io import get_uploaded_data, import_request, import_response
from rssched.app.utils.transform import get_request_summary, get_response_summary
from rssched.data.access import PkgDataAccess


def toggle_sidebar():
    st.session_state.sidebar_state = (
        "collapsed" if st.session_state.sidebar_state == "expanded" else "expanded"
    )


def set_file_in_session_state(
    request_file_bytes: BytesIO, response_file_bytes: BytesIO
) -> None:
    """Set the uploaded or example files in the session state and process them."""
    request_instance_name = ".".join(request_file_bytes.name.split(".")[:2])
    response_instance_name = ".".join(response_file_bytes.name.split(".")[:2])

    if request_instance_name != response_instance_name:
        st.warning(
            f"Instance of request '{request_instance_name}' and response '{response_instance_name}' not the same."
        )

    st.session_state.rssched_instance_name = request_instance_name
    st.session_state.request_file = request_file_bytes
    st.session_state.response_file = response_file_bytes
    st.session_state.request_data = import_request(request_file_bytes)
    st.session_state.response_data = import_response(response_file_bytes)

    st.success("Files uploaded and processed successfully!")


def load_example_files() -> Tuple[BytesIO, BytesIO]:
    """Load example request and response files from the package."""
    request_file_path: Path = PkgDataAccess.locate_request()
    response_file_path: Path = PkgDataAccess.locate_response()

    # Read files and convert to BytesIO
    with request_file_path.open("rb") as f:
        request_bytes = BytesIO(f.read())
        request_bytes.name = request_file_path.name  # Set the name attribute

    with response_file_path.open("rb") as f:
        response_bytes = BytesIO(f.read())
        response_bytes.name = response_file_path.name  # Set the name attribute

    return request_bytes, response_bytes


def handle_file_upload() -> Optional[Tuple[BytesIO, BytesIO]]:
    """Handle the user file uploads for request and response files."""
    request_file_upload = st.file_uploader(
        "Set request file (JSON)", type=["json"], key="request_uploader"
    )
    response_file_upload = st.file_uploader(
        "Set response file (JSON)", type=["json"], key="response_uploader"
    )

    if request_file_upload is not None and response_file_upload is not None:
        return request_file_upload, response_file_upload
    return None


# Initialize session state to store file uploads
if "request_file" not in st.session_state:
    st.session_state.request_file = None
if "response_file" not in st.session_state:
    st.session_state.response_file = None
if "sidebar_state" not in st.session_state:
    st.session_state.sidebar_state = "collapsed"

st.set_page_config(initial_sidebar_state=st.session_state.sidebar_state)
st.title("RSSched Analyzer")
st.markdown(
    """
### About
This page provides an aggregated summary of the request data uploaded by the user. 
You can see important statistics such as the number of locations, vehicle types, depots, 
routes, and other relevant metrics. Additionally, an objective value from the response is also displayed below.
"""
)

# Check if files have been uploaded
files_uploaded = (
    st.session_state.request_file is not None
    and st.session_state.response_file is not None
)

# Display file uploaders and "Load Example" button only if no files have been uploaded
if not files_uploaded:
    st.subheader("Upload Data")
    uploaded_files = handle_file_upload()
    if uploaded_files:
        request_file, response_file = uploaded_files
        set_file_in_session_state(request_file, response_file)
        toggle_sidebar()
        st.rerun()

    if st.button("Load Example"):
        example_request_file, example_response_file = load_example_files()
        set_file_in_session_state(example_request_file, example_response_file)
        toggle_sidebar()
        st.rerun()


# Show the reset button only if files have been uploaded
if files_uploaded:
    request, response, instance_name = get_uploaded_data()

    st.subheader("Uploaded Data")
    st.write(f"**Request File:** {st.session_state.request_file.name}")
    st.dataframe(get_request_summary(request), hide_index=True)
    st.write(f"**Response File:** {st.session_state.response_file.name}")
    st.dataframe(get_response_summary(response), hide_index=True)

    if st.button("Reset"):
        st.session_state.request_file = None
        st.session_state.response_file = None
        st.session_state.request_data = None
        st.session_state.response_data = None
        toggle_sidebar()
        st.rerun()
