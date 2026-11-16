"""Saarathi global configuration derived from the active scenario manifest."""
from pathlib import Path

from .scenario import load_scenario

CODE_DIR = Path(__file__).resolve().parents[2]
SCENARIO = load_scenario()
SCENARIO_DIR = SCENARIO.path.parent
RESULTS_DIR = CODE_DIR / "experiments" / "results"
if SCENARIO_DIR.name != "corridor4":      # keep the reference results untouched
    RESULTS_DIR = RESULTS_DIR / SCENARIO_DIR.name

# PCU is scenario-owned. The supplied factors are a sourced baseline, not an
# assertion that PCU is constant in every Indian traffic condition.
PCU = SCENARIO.pcu["factor_sets"][SCENARIO.pcu["active"]]["factors"]
MODAL_SPLIT = SCENARIO.traffic["modal_split"]

# Safety shell
MIN_GREEN_S = SCENARIO.data["safety"]["min_green_s"]
MAX_GREEN_S = SCENARIO.data["safety"]["max_green_s"]
YELLOW_S = SCENARIO.data["safety"]["yellow_s"]
ALL_RED_S = SCENARIO.data["safety"]["all_red_s"]
DECISION_INTERVAL_S = SCENARIO.data["safety"]["decision_interval_s"]

# Simulation
STEP_LENGTH_S = SCENARIO.data["simulation"]["step_length_s"]
LATERAL_RESOLUTION = SCENARIO.data["simulation"]["lateral_resolution_m"]
HALT_SPEED = SCENARIO.data["simulation"]["halt_speed_mps"]

HOURLY_PROFILE = SCENARIO.traffic["hourly_profile"]
PEAK_FLOWS = SCENARIO.traffic.get("peak_flows_veh_per_hour", {})
N_JUNCTIONS = len(SCENARIO.junction_ids)
