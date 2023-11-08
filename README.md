# GeoView
Simple 3D visualisation of downhole geological data. Currently a WIP.

Currently supports:
- Import collar data CSV
  Headings: [HOLE] [EASTING] [NORTHING] [RL]
- Import lithology data CSV
  Headings: [HOLE] [DEPTH_FROM] [DEPTH_TO] [ROCK] [WSECT]
- View identified working sections (WSECT), label and draw delauney triangulations

Planned tasks:
- Desurvey support
- Basemap imagery support
- Cross-section draw
- Synthetic hole import/ export
- LIDAR dot-imagery import support
- SHP import support
