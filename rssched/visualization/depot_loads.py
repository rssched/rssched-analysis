from datetime import timedelta

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from rssched.model.request import Request
from rssched.model.response import Response


def _flatten_depot_vehicle_loads(response: Response, depot_id: str) -> pd.DataFrame:
    valid_depot_ids = [depot_load.depot for depot_load in response.schedule.depot_loads]
    if depot_id not in valid_depot_ids:
        raise ValueError(
            f"Depot ID '{depot_id}' is not valid. Available depot IDs are: {valid_depot_ids}."
        )

    # Initialize vehicle counts for the specified depot
    counts: dict[str, int] = {}
    for depot_load in response.schedule.depot_loads:
        if depot_load.depot == depot_id:
            for load in depot_load.load:
                counts[load.vehicle_type] = load.spawn_count

    depot_counts = []

    # Process each fleet and its vehicles to track departures and arrivals
    for fleet in response.schedule.fleet:
        for vehicle in fleet.vehicles:
            if vehicle.start_depot == depot_id:
                # Get the earliest departure time from all segments, slots, and trips
                first_departure = min(
                    (
                        segment.departure
                        for segment in vehicle.departure_segments
                        if segment.departure
                    ),
                    default=None,
                )
                first_maintenance_start = min(
                    (slot.start for slot in vehicle.maintenance_slots if slot.start),
                    default=None,
                )
                first_deadhead_departure = min(
                    (
                        trip.departure
                        for trip in vehicle.dead_head_trips
                        if trip.departure
                    ),
                    default=None,
                )

                earliest_time = min(
                    time
                    for time in [
                        first_departure,
                        first_maintenance_start,
                        first_deadhead_departure,
                    ]
                    if time is not None
                )

                depot_counts.append(
                    {
                        "Time": earliest_time,
                        "Vehicle Type": fleet.vehicle_type,
                        "Vehicle": vehicle.id,
                        "Type": "Departure",
                    }
                )

            if vehicle.end_depot == depot_id:
                # Get the latest arrival time from all segments, slots, and trips
                last_departure = max(
                    (
                        segment.departure
                        for segment in vehicle.departure_segments
                        if segment.departure
                    ),
                    default=None,
                )
                last_maintenance_start = max(
                    (slot.start for slot in vehicle.maintenance_slots if slot.start),
                    default=None,
                )
                last_deadhead_departure = max(
                    (
                        trip.departure
                        for trip in vehicle.dead_head_trips
                        if trip.departure
                    ),
                    default=None,
                )

                latest_time = max(
                    time
                    for time in [
                        last_departure,
                        last_maintenance_start,
                        last_deadhead_departure,
                    ]
                    if time is not None
                )

                depot_counts.append(
                    {
                        "Time": latest_time,
                        "Vehicle Type": fleet.vehicle_type,
                        "Vehicle": vehicle.id,
                        "Type": "Arrival",
                    }
                )

    # Convert to DataFrame and sort values
    df = (
        pd.DataFrame(depot_counts)
        .sort_values(by=["Vehicle Type", "Time"])
        .reset_index(drop=True)
    )

    # Find the earliest event time and adjust the initial state
    earliest_event_time = df["Time"].min() - timedelta(hours=1)

    # Add the initial state to the DataFrame for each vehicle type
    for vehicle_type, count in counts.items():
        df = pd.concat(
            [
                pd.DataFrame(
                    [
                        {
                            "Time": earliest_event_time,
                            "Vehicle Type": vehicle_type,
                            "Units": count,
                            "Vehicle": "N/A",
                            "Type": "Initial",
                        }
                    ]
                ),
                df,
            ]
        ).reset_index(drop=True)

    # Fill in the units count based on the type of event
    for vehicle_type in df["Vehicle Type"].unique():
        current_count = df.loc[
            (df["Vehicle Type"] == vehicle_type) & (df["Type"] == "Initial"), "Units"
        ].values[0]
        for i, row in df.iterrows():
            if row["Vehicle Type"] == vehicle_type:
                if row["Type"] == "Departure":
                    current_count -= 1
                elif row["Type"] == "Arrival":
                    current_count += 1
                df.at[i, "Units"] = current_count

    # Find the latest event time for each vehicle type and add the final state
    latest_event_time = df["Time"].max() + timedelta(hours=1)

    for vehicle_type in df["Vehicle Type"].unique():
        final_count = df[df["Vehicle Type"] == vehicle_type]["Units"].iloc[-1]

        df = pd.concat(
            [
                df,
                pd.DataFrame(
                    [
                        {
                            "Time": latest_event_time,
                            "Vehicle Type": vehicle_type,
                            "Units": final_count,
                            "Vehicle": "N/A",
                            "Type": "Final",
                        }
                    ]
                ),
            ]
        ).reset_index(drop=True)

    return df.sort_values(by=["Vehicle Type", "Time"]).reset_index(drop=True)


def _extract_cummulative_vehicle_loads(df_depot_counts):
    # Initialize cumulative load with the sum of initial vehicle units
    initial_total_load = df_depot_counts[df_depot_counts["Type"] == "Initial"][
        "Units"
    ].sum()
    cumulative_count = initial_total_load

    # Create a new DataFrame to store the cumulative load over time
    cumulative_load_data = []

    # Loop over the sorted DataFrame to calculate the cumulative load
    for _, row in (
        df_depot_counts.sort_values(by=["Time"]).reset_index(drop=True).iterrows()
    ):
        if row["Type"] == "Departure":
            cumulative_count -= 1
        elif row["Type"] == "Arrival":
            cumulative_count += 1

        # Store the cumulative load at each event time
        cumulative_load_data.append(
            {"Time": row["Time"], "Cumulative Units": cumulative_count}
        )

    # Convert to DataFrame
    df_total_cumulative_load = pd.DataFrame(cumulative_load_data)

    return df_total_cumulative_load


def plot_depot_vehicle_loads(
    request: Request, response: Response, instance_name: str, depot_id: str
):
    df_depot_counts = _flatten_depot_vehicle_loads(response, depot_id)
    df_total_cumulative_load = _extract_cummulative_vehicle_loads(df_depot_counts)

    # Find the depot's maximum capacity from the request data
    depot_capacity = next(
        (depot.capacity for depot in request.depots if depot.id == depot_id),
        None,
    )

    # Create a subplot with shared x-axis to display both graphs
    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.1,
    )

    # Add step plot for each vehicle type in the first graph
    vehicle_types = df_depot_counts["Vehicle Type"].unique()

    for vehicle_type in vehicle_types:
        vehicle_data = df_depot_counts[df_depot_counts["Vehicle Type"] == vehicle_type]
        fig.add_trace(
            go.Scatter(
                x=vehicle_data["Time"],
                y=vehicle_data["Units"],
                mode="lines",
                line_shape="hv",  # Step chart
                name=f"{vehicle_type}",
            ),
            row=1,
            col=1,
        )

    # Add cumulative load plot in the second graph with gray color
    fig.add_trace(
        go.Scatter(
            x=df_total_cumulative_load["Time"],
            y=df_total_cumulative_load["Cumulative Units"],
            mode="lines",
            line_shape="hv",
            name="Cumulative Load",
            fill="tozeroy",  # Filling the area under the curve
            line=dict(color="gray"),  # Set cumulative load color to gray
        ),
        row=2,
        col=1,
    )

    # Add a horizontal dashed line for the depot capacity on the second subplot
    if depot_capacity:
        fig.add_shape(
            type="line",
            x0=df_total_cumulative_load["Time"].min(),
            y0=depot_capacity,
            x1=df_total_cumulative_load["Time"].max(),
            y1=depot_capacity,
            line=dict(
                color="red", width=2, dash="dash"
            ),  # Red dashed line for capacity
            xref="x2",  # Refers to the x-axis of the second subplot
            yref="y2",  # Refers to the y-axis of the second subplot
        )
        fig.add_annotation(
            x=df_total_cumulative_load["Time"].max(),
            y=depot_capacity,
            text=f"Capacity: {depot_capacity}",
            showarrow=False,
            yshift=10,
            font=dict(color="red"),
            xref="x2",  # Refers to the x-axis of the second subplot
            yref="y2",  # Refers to the y-axis of the second subplot
        )

    # Update layout to always show the legend and improve visualization
    fig.update_layout(
        xaxis_title="",
        yaxis_title="Units at Depot",
        legend_title="Vehicle Types",
        hovermode="x unified",
        showlegend=True,
        title=f"Depot '{depot_id}': Vehicle Loads (Instance: {instance_name})",
    )

    return fig
