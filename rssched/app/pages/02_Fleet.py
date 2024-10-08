from typing import Any

import streamlit as st

from rssched.app.utils.io import get_uploaded_data
from rssched.visualization.active_events import plot_active_events_over_time
from rssched.visualization.fleet_efficiency import plot_fleet_efficiency
from rssched.visualization.vehicle_type_gantt import plot_gantt_per_vehicle_type
from rssched.visualization.vehicle_utilization import plot_vehicle_utilization

st.title("Fleet")

request, response, instance_name = get_uploaded_data()


tabs = st.tabs(
    ["Vehicle Circuits", "Active Events", "Vehicle Utilization", "Efficiency"]
)

with tabs[0]:
    plots = plot_gantt_per_vehicle_type(response, instance_name)
    selected_vehicle_type: str = st.selectbox("Choose vehicle type", plots.keys())
    st.plotly_chart(plots[selected_vehicle_type])

with tabs[1]:
    st.plotly_chart(plot_active_events_over_time(response, instance_name))

with tabs[2]:
    st.plotly_chart(plot_vehicle_utilization(response, instance_name))

with tabs[3]:
    for fig in plot_fleet_efficiency(response, instance_name):
        st.plotly_chart(fig)
