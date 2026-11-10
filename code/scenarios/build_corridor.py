"""Build the corridor4 scenario: a 4-junction EW arterial with NS side roads.

Writes plain-XML node/edge files, runs netconvert to produce corridor.net.xml,
then writes Indian vehicle types (PCU-based, sublane-enabled) and the sumocfg.

Usage:  python scenarios/build_corridor.py
"""
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from saarathi.config import SCENARIO_DIR, LATERAL_RESOLUTION, STEP_LENGTH_S, SCENARIO

NETWORK = SCENARIO.network
SPACING = float(NETWORK["spacing_m"])
SIDE_LEN = float(NETWORK["side_road_length_m"])
N_JUNCTIONS = int(NETWORK["junctions"])
MAIN_LANES = int(NETWORK["main_lanes"])
SIDE_LANES = int(NETWORK["side_lanes"])
SPEED_MAIN = float(NETWORK["main_speed_mps"])
SPEED_SIDE = float(NETWORK["side_speed_mps"])


def build_network(out: Path) -> None:
    nodes, edges = [], []
    xs = [(i + 1) * SPACING for i in range(N_JUNCTIONS)]

    # boundary nodes of the arterial
    nodes.append(('W0', 0, 0, 'priority'))
    nodes.append((f'E{N_JUNCTIONS + 1}', xs[-1] + SPACING, 0, 'priority'))
    for i, x in enumerate(xs, start=1):
        nodes.append((f'J{i}', x, 0, 'traffic_light'))     # signalized junction
        nodes.append((f'N{i}', x, SIDE_LEN, 'priority'))   # side-road ends
        nodes.append((f'S{i}', x, -SIDE_LEN, 'priority'))

    def edge(frm, to, lanes, speed):
        edges.append((f'{frm}_{to}', frm, to, lanes, speed))

    # arterial west->east and east->west
    chain = ['W0'] + [f'J{i}' for i in range(1, N_JUNCTIONS + 1)] + [f'E{N_JUNCTIONS + 1}']
    for a, b in zip(chain, chain[1:]):
        edge(a, b, MAIN_LANES, SPEED_MAIN)
        edge(b, a, MAIN_LANES, SPEED_MAIN)
    # side roads
    for i in range(1, N_JUNCTIONS + 1):
        for end in (f'N{i}', f'S{i}'):
            edge(end, f'J{i}', SIDE_LANES, SPEED_SIDE)
            edge(f'J{i}', end, SIDE_LANES, SPEED_SIDE)

    nod = ['<nodes>']
    nod += [f'  <node id="{n}" x="{x}" y="{y}" type="{t}"/>' for n, x, y, t in nodes]
    nod.append('</nodes>')
    (out / 'corridor.nod.xml').write_text('\n'.join(nod))

    edg = ['<edges>']
    edg += [f'  <edge id="{e}" from="{f}" to="{t}" numLanes="{l}" speed="{s}"/>'
            for e, f, t, l, s in edges]
    edg.append('</edges>')
    (out / 'corridor.edg.xml').write_text('\n'.join(edg))

    subprocess.run(
        ['netconvert',
         '--node-files', str(out / 'corridor.nod.xml'),
         '--edge-files', str(out / 'corridor.edg.xml'),
         '--output-file', str(out / 'corridor.net.xml'),
         '--tls.guess-signals', 'false',
         '--tls.default-type', 'static',
         '--no-turnarounds',            # keep phase structure simple
         ],
        check=True)
    print('net written:', out / 'corridor.net.xml')


VTYPES = """<additional>
  <!-- Indian mixed traffic. PCU/behaviour assumptions: docs/assumptions.md -->
  <vType id="bike"  vClass="motorcycle" length="2.0" width="0.75" minGap="0.8"
         accel="3.0" decel="4.5" maxSpeed="16.7" speedFactor="norm(1.0,0.15)"
         latAlignment="arbitrary" minGapLat="0.25" lcSublane="1.0" lcPushy="0.7"/>
  <vType id="auto"  vClass="passenger"  length="3.0" width="1.4"  minGap="1.0"
         accel="1.8" decel="4.0" maxSpeed="13.9" speedFactor="norm(0.9,0.1)"
         latAlignment="arbitrary" minGapLat="0.35" lcSublane="0.8" lcPushy="0.5"/>
  <vType id="car"   vClass="passenger"  length="4.4" width="1.8"  minGap="1.5"
         accel="2.4" decel="4.5" maxSpeed="19.4" speedFactor="norm(1.0,0.1)"
         latAlignment="center" minGapLat="0.5"/>
  <vType id="bus"   vClass="bus"        length="12.0" width="2.5" minGap="2.0"
         accel="1.1" decel="3.5" maxSpeed="13.9"
         latAlignment="center" minGapLat="0.6"/>
  <vType id="truck" vClass="truck"      length="9.5" width="2.4"  minGap="2.0"
         accel="1.0" decel="3.5" maxSpeed="13.9"
         latAlignment="center" minGapLat="0.6"/>
</additional>
"""

SUMOCFG = f"""<configuration>
  <input>
    <net-file value="corridor.net.xml"/>
    <route-files value="routes.rou.xml"/>
    <additional-files value="vtypes.add.xml"/>
  </input>
  <processing>
    <step-length value="{STEP_LENGTH_S}"/>
    <lateral-resolution value="{LATERAL_RESOLUTION}"/>
    <collision.action value="warn"/>
    <time-to-teleport value="600"/>
  </processing>
  <report>
    <no-step-log value="true"/>
    <duration-log.statistics value="true"/>
  </report>
</configuration>
"""


def vehicle_types_xml() -> str:
    """Render vehicle types from the active manifest.

    ``VTYPES`` is retained above solely as the historic reference. The actual
    generated file follows the manifest, so adding a vehicle class does not
    require a second code change here.
    """
    lines = [
        '<additional>',
        '  <!-- Provisional behaviour; see docs/assumptions.md. -->',
    ]
    attributes = {
        'vclass': 'vClass', 'length_m': 'length', 'width_m': 'width',
        'min_gap_m': 'minGap', 'accel_mps2': 'accel', 'decel_mps2': 'decel',
        'max_speed_mps': 'maxSpeed', 'speed_factor': 'speedFactor',
        'lateral_alignment': 'latAlignment', 'min_lateral_gap_m': 'minGapLat',
        'lc_sublane': 'lcSublane', 'lc_pushy': 'lcPushy',
    }
    for vehicle_id, values in SCENARIO.vehicles.items():
        rendered = ' '.join(
            f'{attributes[key]}="{value}"' for key, value in values.items()
            if key in attributes
        )
        lines.append(f'  <vType id="{vehicle_id}" {rendered}/>')
    return '\n'.join(lines + ['</additional>', ''])


def main() -> None:
    SCENARIO_DIR.mkdir(parents=True, exist_ok=True)
    build_network(SCENARIO_DIR)
    (SCENARIO_DIR / 'vtypes.add.xml').write_text(vehicle_types_xml())
    (SCENARIO_DIR / 'corridor.sumocfg').write_text(SUMOCFG)
    print('scenario ready:', SCENARIO_DIR)


if __name__ == '__main__':
    main()
