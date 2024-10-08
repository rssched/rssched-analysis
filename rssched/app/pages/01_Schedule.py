import streamlit as st

from rssched.app.utils.io import get_uploaded_data
from rssched.visualization.vehicle_type_gantt import plot_gantt_per_vehicle_type

st.title("Schedule")

request, response, instance_name = get_uploaded_data()

plots: dict[str, any] = plot_gantt_per_vehicle_type(response, instance_name)

tabs = st.tabs(plots.keys())

for tab, (title, fig) in zip(tabs, plots.items()):
    with tab:
        st.plotly_chart(fig)
