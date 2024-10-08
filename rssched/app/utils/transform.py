from typing import List

import pandas as pd
from requests import Response

from rssched.model.request import Depot, Request
from rssched.model.response import DepotLoad


def get_request_summary(request: Request) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "locations": [len(request.vehicle_types)],
            "vehicle_types": [len(request.vehicle_types)],
            "depots": [len(request.depots)],
            "depot_capacity": [sum(depot.capacity for depot in request.depots)],
            "routes": [len(request.routes)],
            "departures": [len(request.departures)],
            "maintenance_tracks": [
                sum(slot.track_count for slot in request.maintenance_slots)
            ],
        }
    )


def get_response_summary(response: Response) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "unserved_passengers": [response.objective_value.unserved_passengers],
            "maintenance_violoation": [response.objective_value.maintenance_violation],
            "vehicle_count": [response.objective_value.vehicle_count],
            "costs": [response.objective_value.costs],
        }
    )


def get_vehicle_types(response: Response) -> list[str]:
    return [fleet.vehicle_type for fleet in response.schedule.fleet]


def get_vehicle_summary(response: Response):
    data = []

    for depot_load in response.schedule.depot_loads:
        depot = depot_load.depot
        for load in depot_load.load:
            vehicle_type = load.vehicle_type
            spawn_count = load.spawn_count
            data.append(
                {"location": depot, "vehicle_type": vehicle_type, "count": spawn_count}
            )

    return (
        pd.DataFrame(data)
        .groupby("vehicle_type")["count"]
        .sum()
        .sort_values()
        .reset_index()
    )


def flatten_depots(request: Request, response: Response) -> pd.DataFrame:
    df_request = _flatten_request_depots(request.depots)
    df_response = _flatten_response_depot_loads(response.schedule.depot_loads)
    df_combined = pd.merge(
        df_request, df_response, on=["depot_id", "vehicle_type"], how="outer"
    )
    df_combined["vehicles"] = df_combined["vehicles"].fillna(0).astype(int)
    return df_combined.sort_values(by="vehicles", ascending=False).reset_index(
        drop=True
    )


def _flatten_response_depot_loads(
    response_depot_loads: List[DepotLoad],
) -> pd.DataFrame:
    response_data = []
    for depot_load in response_depot_loads:
        for load in depot_load.load:
            response_data.append(
                {
                    "depot_id": depot_load.depot,
                    "vehicle_type": load.vehicle_type,
                    "vehicles": load.spawn_count,
                }
            )
    return pd.DataFrame(response_data)


def _flatten_request_depots(request_depots: List[Depot]) -> pd.DataFrame:
    request_data = []
    for depot in request_depots:
        for allowed_type in depot.allowed_types:
            request_data.append(
                {
                    "depot_id": depot.id,
                    "vehicle_type": allowed_type.vehicle_type,
                    "vehicle_type_capacity": (
                        allowed_type.capacity
                        if allowed_type.capacity is not None
                        else depot.capacity
                    ),
                    "capacity": depot.capacity,
                }
            )
    return pd.DataFrame(request_data)
