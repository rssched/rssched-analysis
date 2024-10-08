from typing import Any

import streamlit as st

from rssched.app.utils.io import get_uploaded_data
from rssched.app.utils.transform import get_vehicle_types
from rssched.visualization.active_events import plot_active_events_per_vehicle_type
from rssched.visualization.fleet_efficiency import (
    plot_fleet_efficiency_per_vehicle_type,
)
from rssched.visualization.vehicle_type_gantt import plot_gantt_per_vehicle_type
from rssched.visualization.vehicle_utilization import plot_utilization_per_vehicle_type

st.title("Fleet")

request, response, instance_name = get_uploaded_data()

selected_vehicle_type: str = st.selectbox(
    "Choose vehicle type", get_vehicle_types(response)
)

tabs = st.tabs(
    ["Vehicle Circuits", "Active Events", "Vehicle Utilization", "Efficiency"]
)

with tabs[0]:
    plots = plot_gantt_per_vehicle_type(response, instance_name)
    st.plotly_chart(plots[selected_vehicle_type])

with tabs[1]:
    plots = plot_active_events_per_vehicle_type(response, instance_name)
    st.plotly_chart(plots[selected_vehicle_type])

with tabs[2]:
    plots = plot_utilization_per_vehicle_type(response, instance_name)
    st.plotly_chart(plots[selected_vehicle_type])

with tabs[3]:
    plots = plot_fleet_efficiency_per_vehicle_type(response, instance_name)
    st.plotly_chart(plots[selected_vehicle_type])
