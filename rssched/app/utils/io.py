import json
from typing import Tuple

import streamlit as st

from rssched.io.reader import convert_keys_to_snake_case
from rssched.model.request import Request
from rssched.model.response import Info, ObjectiveValue, Response, Schedule


def import_request(file_obj) -> Request:
    data = convert_keys_to_snake_case(json.load(file_obj))
    return Request(**data)


def import_response(file_obj) -> Response:
    data = convert_keys_to_snake_case(json.load(file_obj))

    info = Info(**data["info"])
    objective_value = ObjectiveValue(**data["objective_value"])
    schedule = Schedule(**data["schedule"])

    return Response(info=info, objective_value=objective_value, schedule=schedule)


def get_uploaded_data() -> Tuple[Request, Response, str]:
    if st.session_state.get("request_data") and st.session_state.get("response_data"):
        request_data = st.session_state["request_data"]
        response_data = st.session_state["response_data"]
        return request_data, response_data, st.session_state["rssched_instance_name"]
    else:
        st.warning("Please upload both request and response files on the main page.")
        st.stop()
