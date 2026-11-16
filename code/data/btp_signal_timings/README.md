# BTP signal timings (HAL Old Airport Road corridor)

- Source: https://data.opencity.in/dataset/bengaluru-city-traffic-signal-data (Bengaluru City Traffic Police signal timings, published via OpenCity)
- Dataset created 2022-04-11, last updated 2025-11-27 (CKAN metadata_created / metadata_modified)
- Licence: not stated (CKAN API returns license_title/license_id = None)
- Downloaded: 2026-11-10

## Files
- raw/ : 6 source PDFs (1 page each, text-extractable via pdftotext -layout)
  - cbroad_domlur.pdf (CB Road Airport + Domlur Water Tank), marathalli_yamlur.pdf, isro_kadubeesanahalli.pdf, kudulu_madiwala.pdf, hoodi_esi.pdf (Hoodi + RM Nagar), hosmat_kensington.pdf
  - No Doddanekundi PDF matched in the dataset.
- timings.csv : one row per junction x time band (12 junctions)

## PDF columns
Each table: time band (HH:MM-HH:MM; Sunday row separately), then per-phase durations in seconds for phases 1..N, then CYCLE (s). Phase durations are not split into green/amber/all-red in the PDFs, so `green_s` holds the printed per-phase durations and `amber_s`/`all_red_s` are blank. The last short phase is an exclusive pedestrian phase where the PDF says so (CB Road junction); otherwise unlabelled.
Phase-to-approach mapping is drawn in the PDF's junction diagram, not in text; `phase_order` uses approach names only where the table lists them in phase order (CB Road junction), else P1..Pn. Table-to-junction assignment relies on the title text position in each PDF; verify against the PDF.
Notes: Kudulu Gate has parenthesised alternate values (kept in notes). ISRO rows: phase sum is 3 s less than the printed cycle (noted). Yamlur has BLINKING MODE bands (no timings). Control type (FIXED/VAC) and BWSSB WORK label are in the junction name.
