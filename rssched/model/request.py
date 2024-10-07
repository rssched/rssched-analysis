from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class VehicleType(BaseModel):
    id: str
    capacity: int
    seats: int
    maximal_formation_count: Optional[int] = None


class Location(BaseModel):
    id: str
    day_limit: Optional[int] = None


class AllowedType(BaseModel):
    vehicle_type: str
    capacity: Optional[int] = None


class Depot(BaseModel):
    id: str
    location: str
    capacity: int
    allowed_types: List[AllowedType]


class RouteSegment(BaseModel):
    id: str
    order: int
    origin: str
    destination: str
    distance: int
    duration: int
    maximal_formation_count: Optional[int] = None


class Route(BaseModel):
    id: str
    vehicle_type: str
    segments: List[RouteSegment]


class DepartureSegment(BaseModel):
    id: str
    route_segment: str
    departure: datetime
    passengers: int
    seated: int


class Departure(BaseModel):
    id: str
    route: str
    segments: List[DepartureSegment]


class MaintenanceSlot(BaseModel):
    id: str
    location: str
    start: datetime
    end: datetime
    track_count: int


class DeadHeadTrips(BaseModel):
    indices: List[str]
    durations: List[List[int]]
    distances: List[List[int]]


class Shunting(BaseModel):
    minimal_duration: int
    dead_head_trip_duration: int


class MaintenanceParameters(BaseModel):
    maximal_distance: int


class Costs(BaseModel):
    staff: int
    service_trip: int
    maintenance: int
    dead_head_trip: int
    idle: int


class Parameters(BaseModel):
    forbid_dead_head_trips: bool
    day_limit_threshold: int
    shunting: Shunting
    maintenance: MaintenanceParameters
    costs: Costs


class Request(BaseModel):
    vehicle_types: List[VehicleType]
    locations: List[Location]
    depots: List[Depot]
    routes: List[Route]
    departures: List[Departure]
    maintenance_slots: List[MaintenanceSlot]
    dead_head_trips: DeadHeadTrips
    parameters: Parameters
