import streamlit as st

from rssched.app.utils.io import get_uploaded_data
from rssched.visualization.vehicle_type_gantt import plot_gantt_per_vehicle_type

st.title("Schedule")

request, response, instance_name = get_uploaded_data()

plots = plot_gantt_per_vehicle_type(response, instance_name)

tabs = st.tabs(plots.keys())

for tab, (title, fig) in zip(tabs, plots.items()):
    with tab:
        st.plotly_chart(fig)

"""
from rssched.visualization.vehicle_utilization import plot_vehicle_utilization
from rssched.visualization.fleet_efficiency import plot_fleet_efficiency
from rssched.visualization.active_events import plot_active_events_over_time

tabs = st.tabs(
    [
        "Gantt Chart",
        "Active Events",
        "Vehicle Utilization",
        "Fleet Efficiency",
    ]
)

with tabs[0]:
    st.plotly_chart(plot_gantt_per_vehicle_type(response, instance_name)[0])

with tabs[1]:
    st.plotly_chart(plot_active_events_over_time(response, instance_name))

with tabs[2]:
    st.plotly_chart(plot_vehicle_utilization(response, instance_name))

with tabs[3]:
    st.plotly_chart(plot_fleet_efficiency(response, instance_name))
"""
