"""Fast contract tests for the configurable reference scenario."""
from __future__ import annotations

from pathlib import Path
import sys
import tempfile
import unittest
from copy import deepcopy

import yaml

CODE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE_DIR / "src"))
sys.path.insert(0, str(CODE_DIR / "scenarios"))

from saarathi import demand  # noqa: E402
from saarathi.config import MODAL_SPLIT, N_JUNCTIONS, PCU, SCENARIO  # noqa: E402
from saarathi.scenario import load_scenario  # noqa: E402
from build_corridor import vehicle_types_xml  # noqa: E402


class ScenarioContractTests(unittest.TestCase):
    def test_manifest_drives_junction_count(self):
        self.assertEqual(N_JUNCTIONS, SCENARIO.network["junctions"])
        self.assertEqual(len(SCENARIO.junction_ids), N_JUNCTIONS)

    def test_manifest_supports_a_different_corridor_size(self):
        data = deepcopy(SCENARIO.data)
        data["network"]["junctions"] = 3
        with tempfile.TemporaryDirectory() as temp:
            manifest = Path(temp) / "corridor.yaml"
            manifest.write_text(yaml.safe_dump(data))
            scenario = load_scenario(manifest)
        self.assertEqual(scenario.junction_ids, ["J1", "J2", "J3"])

    def test_modal_split_and_pcu_cover_same_classes(self):
        self.assertAlmostEqual(sum(MODAL_SPLIT.values()), 1.0)
        self.assertEqual(set(MODAL_SPLIT), set(PCU))
        self.assertEqual(set(MODAL_SPLIT), set(SCENARIO.vehicles))

    def test_vehicle_xml_is_manifest_driven(self):
        xml = vehicle_types_xml()
        for vehicle_id in SCENARIO.vehicles:
            self.assertIn(f'id="{vehicle_id}"', xml)

    def test_demand_route_generation_contains_all_active_classes(self):
        with tempfile.TemporaryDirectory() as temp:
            path = demand.generate(hours=(8, 9), seed=7,
                                   out=Path(temp) / "routes.rou.xml")
            xml = path.read_text()
        for vehicle_id, share in MODAL_SPLIT.items():
            if share > 0:
                self.assertIn(f'type="{vehicle_id}"', xml)
        self.assertIn(f'J{N_JUNCTIONS}_E{N_JUNCTIONS + 1}', xml)


if __name__ == "__main__":
    unittest.main()


class OsmScenarioTests(unittest.TestCase):
    """The real-corridor manifest must point at signals that exist in its net."""

    def test_osm_manifest_signals_exist_in_network(self):
        import sumolib
        path = CODE_DIR / "scenarios" / "old_airport_road" / "corridor.yaml"
        scenario = load_scenario(path)
        self.assertTrue(scenario.is_osm)
        self.assertEqual(scenario.profiles, ["literature", "filtering", "lane_disciplined"])
        net = sumolib.net.readNet(str(path.parent / "osm.net.xml"))
        tls = {t.getID() for t in net.getTrafficLights()}
        self.assertLessEqual(set(scenario.junction_ids), tls)

    def test_profile_overrides_apply(self):
        path = CODE_DIR / "scenarios" / "old_airport_road" / "corridor.yaml"
        scenario = load_scenario(path)
        disciplined = scenario.vehicle_types("lane_disciplined")
        self.assertEqual(disciplined["bike"]["lateral_alignment"], "center")
        self.assertEqual(scenario.vehicle_types("literature")["bike"]["lateral_alignment"], "arbitrary")
