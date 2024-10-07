from typing import List

import pandas as pd
from requests import Response

from rssched.model.request import Depot, Request
from rssched.model.response import DepotLoad


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
