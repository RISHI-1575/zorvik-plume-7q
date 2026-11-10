"""Generate routes.rou.xml for a time window of the daily profile.

Flows follow HOURLY_PROFILE (the junction's daily rhythm) and the Bengaluru
modal split. Deterministic given a seed, so experiments are reproducible.
"""
import random
from pathlib import Path

from .config import (SCENARIO_DIR, HOURLY_PROFILE, PEAK_FLOWS, MODAL_SPLIT,
                     N_JUNCTIONS)


def _streams():
    """(name, list-of-edges, peak veh/h) for every origin-destination stream."""
    chain_e = [f'W0_J1'] + [f'J{i}_J{i+1}' for i in range(1, N_JUNCTIONS)] + [f'J{N_JUNCTIONS}_E{N_JUNCTIONS+1}']
    chain_w = [f'E{N_JUNCTIONS+1}_J{N_JUNCTIONS}'] + [f'J{i+1}_J{i}' for i in reversed(range(1, N_JUNCTIONS))] + ['J1_W0']
    yield 'main_we', chain_e, PEAK_FLOWS['main_through']
    yield 'main_ew', chain_w, PEAK_FLOWS['main_through']
    for i in range(1, N_JUNCTIONS + 1):
        yield f'side_ns_{i}', [f'N{i}_J{i}', f'J{i}_S{i}'], PEAK_FLOWS['side_through']
        yield f'side_sn_{i}', [f'S{i}_J{i}', f'J{i}_N{i}'], PEAK_FLOWS['side_through']
    # turning streams: side road -> arterial east, arterial west -> side road
    for i in range(1, N_JUNCTIONS + 1):
        rest_e = chain_e[i:] if i < len(chain_e) else []
        yield f'turn_in_{i}', [f'N{i}_J{i}'] + rest_e, PEAK_FLOWS['turn']
        yield f'turn_out_{i}', chain_e[:i] + [f'J{i}_S{i}'], PEAK_FLOWS['turn']


def generate(hours=(8, 10), seed=0, out: Path | None = None,
             scale: float = 1.0) -> Path:
    """Write flows for sim time 0..(hours span), applying the hourly profile."""
    rng = random.Random(seed)
    out = out or SCENARIO_DIR / 'routes.rou.xml'
    lines = ['<routes>']
    fid = 0
    for h in range(hours[0], hours[1]):
        mult = HOURLY_PROFILE[h % 24] * scale
        begin = (h - hours[0]) * 3600
        end = begin + 3600
        for name, edges, peak in _streams():
            for vtype, share in MODAL_SPLIT.items():
                vph = peak * mult * share
                if vph < 1:
                    continue
                lines.append(
                    f'  <flow id="f{fid}_{name}_{vtype}_h{h}" type="{vtype}" '
                    f'begin="{begin}" end="{end}" vehsPerHour="{vph:.1f}" '
                    f'route="!route" departLane="best" departSpeed="max" '
                    f'departPosLat="random"/>'.replace(
                        'route="!route"',
                        f'route="r{fid}"'))
                lines.insert(1, f'  <route id="r{fid}" edges="{" ".join(edges)}"/>')
                fid += 1
    lines.append('</routes>')
    out.write_text('\n'.join(lines))
    return out


if __name__ == '__main__':
    p = generate()
    print('routes written:', p)
