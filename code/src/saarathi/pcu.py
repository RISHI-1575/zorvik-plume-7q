"""PCU-weighted traffic sensing helpers (shared by all controllers + RL env)."""
import traci

from .config import PCU, HALT_SPEED

_type_cache: dict[str, float] = {}


def vehicle_pcu(veh_id: str) -> float:
    t = traci.vehicle.getTypeID(veh_id).split('@')[0]
    if t not in _type_cache:
        _type_cache[t] = PCU.get(t, 1.0)
    return _type_cache[t]


def lane_queue_pcu(lane_id: str) -> float:
    """PCU total of halted vehicles on a lane (what a camera-count gives us)."""
    total = 0.0
    for v in traci.lane.getLastStepVehicleIDs(lane_id):
        if traci.vehicle.getSpeed(v) < HALT_SPEED:
            total += vehicle_pcu(v)
    return total


def lane_occupancy_pcu(lane_id: str) -> float:
    """PCU total of ALL vehicles on a lane (moving + halted)."""
    return sum(vehicle_pcu(v) for v in traci.lane.getLastStepVehicleIDs(lane_id))
