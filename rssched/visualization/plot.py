from rssched.model.response import Response
from rssched.visualization.active_events import plot_active_events_per_vehicle_type
from rssched.visualization.fleet_efficiency import (
    plot_fleet_efficiency_per_vehicle_type,
)
from rssched.visualization.vehicle_type_gantt import plot_gantt_per_vehicle_type
from rssched.visualization.vehicle_utilization import plot_utilization_per_vehicle_type


def generate_plots(response: Response, instance_name: str):
    figures = list(plot_gantt_per_vehicle_type(response, instance_name).values())
    figures.extend(
        list(plot_active_events_per_vehicle_type(response, instance_name).values())
    )
    figures.extend(
        list(plot_utilization_per_vehicle_type(response, instance_name).values())
    )
    figures.extend(
        list(plot_fleet_efficiency_per_vehicle_type(response, instance_name).values())
    )
    return figures
