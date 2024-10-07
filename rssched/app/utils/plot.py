import pandas as pd
import plotly.graph_objects as go
from plotly.graph_objs import Figure


def plot_depots_bar_chart(df_depots: pd.DataFrame) -> Figure:
    # Group by depot_id to calculate the total capacity and sort by the number of vehicles
    df_depots_grouped = (
        df_depots[df_depots["vehicles"] > 0]
        .groupby("depot_id", as_index=False)
        .agg({"vehicles": "sum", "capacity": "max"})
        .sort_values(by="vehicles", ascending=False)
    )

    # Create a bar chart
    fig = go.Figure()

    # Add bar for the number of vehicles
    fig.add_trace(
        go.Bar(
            x=df_depots_grouped["depot_id"],
            y=df_depots_grouped["vehicles"],
            name="Vehicles",
            marker_color="blue",  # Color for vehicles bar
        )
    )

    # Add bar for the depot capacity
    fig.add_trace(
        go.Bar(
            x=df_depots_grouped["depot_id"],
            y=df_depots_grouped["capacity"],
            name="Capacity",
            marker_color="gray",  # Color for capacity bar
        )
    )

    # Update layout of the bar chart
    fig.update_layout(
        barmode="group",  # Bars grouped side by side
        title="Depot Vehicles and Capacity",
        xaxis_title="Depot ID",
        # yaxis_title="Count",
        legend_title="Legend",
    )

    # Return the figure object
    return fig
