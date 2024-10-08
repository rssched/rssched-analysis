import pandas as pd
import plotly.graph_objects as go

from rssched.model.response import Response
from rssched.visualization.colors import EVENT_TYPES


def summarize_vehicle_activities(response):
    activities = []

    for fleet in response.schedule.fleet:
        vehicle_type = fleet.vehicle_type

        for vehicle in fleet.vehicles:
            vehicle_id = vehicle.id
            times = []

            for segment in vehicle.departure_segments:
                times.append(("ServiceTrip", segment.departure, segment.arrival))
            for slot in vehicle.maintenance_slots:
                times.append(("MaintenanceSlot", slot.start, slot.end))
            for trip in vehicle.dead_head_trips:
                times.append(("DeadHeadTrip", trip.departure, trip.arrival))

            times.sort(key=lambda x: x[1])

            last_end_time = None

            for activity_type, start, end in times:
                duration = (end - start).total_seconds() / 3600
                activities.append(
                    {
                        "vehicle_id": vehicle_id,
                        "vehicle_type": vehicle_type,
                        "activity_type": activity_type,
                        "duration": duration,
                        "start_time": start,
                        "end_time": end,
                    }
                )

                if last_end_time is not None and start > last_end_time:
                    idle_duration = (start - last_end_time).total_seconds() / 3600
                    activities.append(
                        {
                            "vehicle_id": vehicle_id,
                            "vehicle_type": vehicle_type,
                            "activity_type": "Idle",
                            "duration": idle_duration,
                            "start_time": last_end_time,
                            "end_time": start,
                        }
                    )

                last_end_time = end

    df_activities = pd.DataFrame(activities)
    return df_activities


def plot_fleet_efficiency_per_vehicle_type(
    response: Response, instance_name: str
) -> dict[str, go.Figure]:
    df = summarize_vehicle_activities(response)

    vehicle_types = df["vehicle_type"].unique()

    figs = {}

    for v_type in vehicle_types:
        filtered_df = df[df["vehicle_type"] == v_type]
        grouped = filtered_df.groupby("activity_type")["duration"].sum().reset_index()
        fig = go.Figure(
            data=[
                go.Pie(
                    labels=grouped["activity_type"],
                    values=grouped["duration"],
                    textinfo="label+percent",
                    insidetextorientation="radial",
                    marker_colors=[
                        EVENT_TYPES[atype] for atype in grouped["activity_type"]
                    ],
                )
            ]
        )
        fig.update_layout(
            title=f"Activity Distribution '{v_type}' (instance: {instance_name})"
        )
        figs[v_type] = fig

    return figs
