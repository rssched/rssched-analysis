import pandas as pd
import streamlit as st

from rssched.app.utils.io import get_uploaded_data

st.title(f"Run Info")

# Retrieve uploaded request and response data
request, response, instance_name = get_uploaded_data()


request_summary_df = pd.DataFrame(
    {
        "Locations": [len(request.vehicle_types)],
        "Vehicle types": [len(request.vehicle_types)],
        "Depots": [len(request.depots)],
        "Depot capacity": [sum(depot.capacity for depot in request.depots)],
        "Routes": [len(request.routes)],
        "Departures": [len(request.departures)],
        "Maintenance tracks": [
            sum(slot.track_count for slot in request.maintenance_slots)
        ],
    }
)

response_summary_df = pd.DataFrame(
    {
        "Unserved passengers": [response.objective_value.unserved_passengers],
        "Maintenance violoation": [response.objective_value.maintenance_violation],
        "Vehicle count": [response.objective_value.vehicle_count],
        "Costs": [response.objective_value.costs],
    }
)

st.write(f"**Instance:** {instance_name}")

st.subheader("Request Summary")
st.write(f"**File:** {st.session_state.request_file.name}")
st.dataframe(request_summary_df, hide_index=True)

st.subheader("Response Summary")
st.write(f"**File:** {st.session_state.response_file.name}")
st.dataframe(response_summary_df, hide_index=True)
