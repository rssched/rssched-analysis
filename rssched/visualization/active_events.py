import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from rssched.model.response import Response
from rssched.visualization.colors import EVENT_TYPES


def plot_active_events_per_vehicle_type(
    response: Response, instance_name: str
) -> dict[str, go.Figure]:
    events = []
    for fleet in response.schedule.fleet:
        for vehicle in fleet.vehicles:
            for segment in vehicle.departure_segments:
                events.append(
                    {
                        "Start": segment.departure,
                        "End": segment.arrival,
                        "Type": "ServiceTrip",
                        "Vehicle Type": fleet.vehicle_type,
                    }
                )
            for slot in vehicle.maintenance_slots:
                events.append(
                    {
                        "Start": slot.start,
                        "End": slot.end,
                        "Type": "MaintenanceSlot",
                        "Vehicle Type": fleet.vehicle_type,
                    }
                )
            for trip in vehicle.dead_head_trips:
                events.append(
                    {
                        "Start": trip.departure,
                        "End": trip.arrival,
                        "Type": "DeadHeadTrip",
                        "Vehicle Type": fleet.vehicle_type,
                    }
                )

    df = pd.DataFrame(events)
    figures = {}

    for vehicle_type, group in df.groupby("Vehicle Type"):
        min_time = group["Start"].min().floor("15min")
        max_time = group["End"].max().ceil("15min")
        time_range = pd.date_range(min_time, max_time, freq="15min")
        df_count = pd.DataFrame(
            0,
            index=time_range,
            columns=["ServiceTrip", "MaintenanceSlot", "DeadHeadTrip"],
        )

        for interval in time_range:
            for _, event in group.iterrows():
                if event["Start"] <= interval < event["End"]:
                    df_count.at[interval, event["Type"]] += 1

        df_count.reset_index(inplace=True)
        df_count.rename(columns={"index": "Time"}, inplace=True)
        df_melted = df_count.melt(
            id_vars=["Time"], var_name="Event Type", value_name="Active Count"
        )

        fig = px.line(
            df_melted,
            x="Time",
            y="Active Count",
            color="Event Type",
            title=f"Active Events '{vehicle_type}' (instance: {instance_name})",
            color_discrete_map=EVENT_TYPES,
        )
        fig.update_layout(hovermode="x", hoverdistance=50)
        fig.update_xaxes(title_text="Time", tickformat="%Y-%m-%d %H:%M")
        fig.update_yaxes(title_text="Number of Active Events")

        figures[vehicle_type] = fig

    return figures
