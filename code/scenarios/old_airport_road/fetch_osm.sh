#!/usr/bin/env bash
# Rebuild osm.net.xml (+ buildings.poly.xml for rendering) from OpenStreetMap.
# Map data (c) OpenStreetMap contributors, ODbL. Run from anywhere; needs sumo on PATH.
set -euo pipefail
cd "$(dirname "$0")"
i=0
for lo in 77.636 77.6533 77.6705 77.6878; do   # 4 tiles: OSM API caps 50k nodes/request
  i=$((i+1)); hi=$(python3 -c "print(round($lo+0.0173,4))")
  [ -s tile$i.osm ] || curl -sf -A "sumo-osm-fetch/1.0" -o tile$i.osm \
    "https://api.openstreetmap.org/api/0.6/map?bbox=$lo,12.951,$hi,12.964"
done
T=tile1.osm,tile2.osm,tile3.osm,tile4.osm
netconvert --osm-files $T -o osm.net.xml --lefthand true \
  --keep-edges.by-type highway.trunk,highway.trunk_link,highway.primary,highway.primary_link,highway.secondary,highway.secondary_link,highway.tertiary,highway.tertiary_link \
  --remove-edges.by-vclass pedestrian,rail,tram --keep-edges.components 1 \
  --geometry.remove --ramps.guess --roundabouts.guess --junctions.join \
  --tls.guess-signals --tls.discard-simple --tls.join --tls.default-type static \
  --no-turnarounds --output.street-names --osm.sidewalks false --edges.join \
  --ignore-errors.edge-type --no-warnings
# OSM lacks signal tags at Domlur (Inner Ring Rd) and Suranjandas Rd (ISRO); BTP signals them.
netconvert -s osm.net.xml --tls.set 13392231547,cluster_4703745979_6884057005 \
  --tls.default-type static -o osm.net.xml --no-warnings
TYP="$(python3 -c 'import sumo,os;print(os.path.join(os.path.dirname(sumo.__file__),"data","typemap","osmPolyconvert.typ.xml"))')"
polyconvert --osm-files $T --net-file osm.net.xml --type-file "$TYP" -o buildings.poly.xml --ignore-errors --no-warnings
echo "ok: osm.net.xml buildings.poly.xml"
