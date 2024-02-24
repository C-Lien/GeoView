# GeoView v0.0.3
Simple 3D visualisation of downhole geological data.

This software was designed to facilitate simplistic plotting and triangulations
of known downhole data. This process currently only supports delauney triangulation
of known WSECT (layers) to provide quick reference to current lithology state.

This is not intended as a professional geological software package and will not
attempt to replicate any of the more advanced features present in dedicate services.

Currently supports:
- Import collar data CSV - See example documents for required headers.

- Import lithology data CSV - See example documents for required headers.

- Import downhole survey data CSV - See example documents for required headers.

- View identified working sections (WSECT), label and draw delauney triangulations.
    - Downhole data will exclude holes where WSECT does not exist at matching
      depth to surrounding holes. Exclusion occurs where not exist but TD is
      probable for inclusion. Shallow holes are excluded from exclusion and
      triangulation will ignore these coordinates.

- Minimum Curvature Desurvey - Drill String and Lithology desurvey mapping.

Planned tasks:
- Basemap imagery support.

- Cross-section draw.

- Synthetic hole import/export.

- LIDAR dot-imagery import support.

- SHP import support.

- Predictive lithology where downhole survey does not extend to lithology TD.

- Expediate text drawing. Currently text values are plotted as one object per
  instance. This results in significant slowdown at larger text volumes.

- Downhole plotting currently 'magic number' two meters when not desurvey.
  This will be moved to a user accessible value/assess viability of string type
  plotting over point plotting to create a single downhole visual entity.

- Highlighting of statistically significant angle variance of WSECT between holes
  to assist in fault delineation or regions of interest.

Known issues:
- External hole to selected radius will occasionally plot downhole string in
  addition to selected radius. Does not impact triangulations nor visual obs
  of target region. While odd, this does not impact use.

- No handling of downhole survey data where downhole survey starts at a depth
  greater than 0 meters. As a result, current desurvey assumes correct recording
  of orientation from surface. As such, desurvey starting at >0 meters will be
  'shifted' to starting at 0 meters.

- Lithology logged below desurvey TD will not plot due to uncertainty.