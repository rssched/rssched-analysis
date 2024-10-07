from typing import List

import pandas as pd
import streamlit as st

from rssched.app.utils.io import get_uploaded_data
from rssched.app.utils.transform import flatten_depots
from rssched.visualization.depot_loads import plot_depot_vehicle_loads

st.title("Depots")

request, response, instance_name = get_uploaded_data()

tabs = st.tabs(["Overview", "Details"])

df_depots = flatten_depots(request, response)


with tabs[0]:
    show_aggregated = st.checkbox("Aggregate", value=True)

    if show_aggregated:
        df_grouped = df_depots.groupby("depot_id", as_index=False).agg(
            {"vehicles": "sum", "capacity": "mean"}
        )
        st.dataframe(df_grouped, hide_index=True)
    else:
        st.dataframe(df_depots, hide_index=True)


with tabs[1]:
    selected_depot: str = st.selectbox(
        "Choose depot to see detailed statistics",
        df_depots[df_depots["vehicles"] > 0]["depot_id"].unique(),
    )
    st.plotly_chart(plot_depot_vehicle_loads(response, instance_name, selected_depot))
    st.dataframe(df_depots[df_depots["depot_id"] == selected_depot], hide_index=True)
