"""Scenario manifest loader.

All scenario-specific values live in ``scenarios/<name>/corridor.yaml``.
Keeping this data outside Python makes the simulator configurable without
duplicating junction counts, vehicle mixes, or PCU factors across modules.
"""
from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class Scenario:
    path: Path
    data: dict[str, Any]

    @property
    def name(self) -> str:
        return str(self.data["name"])

    @property
    def network(self) -> dict[str, Any]:
        return self.data["network"]

    @property
    def traffic(self) -> dict[str, Any]:
        return self.data["traffic"]

    @property
    def vehicles(self) -> dict[str, dict[str, Any]]:
        return self.data["vehicles"]

    @property
    def pcu(self) -> dict[str, Any]:
        return self.data["pcu"]

    @property
    def junction_ids(self) -> list[str]:
        return [f"J{i}" for i in range(1, int(self.network["junctions"]) + 1)]


def _default_path() -> Path:
    code_dir = Path(__file__).resolve().parents[2]
    configured = os.environ.get("SAARATHI_SCENARIO")
    if configured:
        return Path(configured).expanduser().resolve()
    return code_dir / "scenarios" / "corridor4" / "corridor.yaml"


def load_scenario(path: str | Path | None = None) -> Scenario:
    manifest = Path(path).resolve() if path else _default_path()
    if not manifest.exists():
        raise FileNotFoundError(f"Scenario manifest not found: {manifest}")
    with manifest.open(encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    _validate(data, manifest)
    return Scenario(path=manifest, data=data)


def _validate(data: Any, path: Path) -> None:
    if not isinstance(data, dict):
        raise ValueError(f"{path}: manifest must be a mapping")
    required = {"schema_version", "name", "network", "traffic", "vehicles", "pcu"}
    missing = required - set(data)
    if missing:
        raise ValueError(f"{path}: missing keys: {', '.join(sorted(missing))}")

    network = data["network"]
    junctions = int(network.get("junctions", 0))
    if not 1 <= junctions <= 20:
        raise ValueError(f"{path}: network.junctions must be between 1 and 20")
    for key in ("spacing_m", "side_road_length_m", "main_lanes", "side_lanes"):
        if float(network.get(key, 0)) <= 0:
            raise ValueError(f"{path}: network.{key} must be positive")

    vehicles = data["vehicles"]
    if "car" not in vehicles:
        raise ValueError(f"{path}: vehicles must include the car reference class")
    shares = data["traffic"].get("modal_split", {})
    if set(shares) != set(vehicles):
        raise ValueError(f"{path}: modal_split classes must match vehicle classes")
    if abs(sum(float(v) for v in shares.values()) - 1.0) > 1e-6:
        raise ValueError(f"{path}: modal_split must sum to 1.0")

    factors = data["pcu"].get("factor_sets", {})
    active = data["pcu"].get("active")
    if active not in factors:
        raise ValueError(f"{path}: pcu.active must name an available factor set")
    for name, factor_set in factors.items():
        if set(factor_set["factors"]) != set(vehicles):
            raise ValueError(f"{path}: PCU set {name!r} must cover all vehicle classes")

