# Nominal package models for populated board inspection

Eight missing package patterns are supplied as native FreeCAD solids and STEP.
`verification.json` lists exact filenames, physical pad counts, source footprint
hashes, valid reimported solids and dimensions. All 192 physical contact datums
come from the saved actual land patterns. These are editable reference models;
they are not manufacturer tolerance models.

Small IC body heights are declared visualization allocations. Contacts use
land datums with simplified nominal metal geometry. TRACO's body envelope uses
its package description. BT40F uses the asymmetric 15/14 mm manufacturer Fab
outline and original footprint origin; its shield is a nominal envelope. The
local axes are X=footprint X, Y=negative footprint Y, Z=above board.

Regenerate with KiCad's Python for `extract_packages.py`, then FreeCAD's Python
for `build_packages.py`. Reimport/topology checks run during generation. Model
names contain decimal points, so filenames append the extension to the entire
package name. The installed standard KiCad models accompany the board set with
their upstream notices. No model establishes an interference tolerance,
hermetic enclosure, implantation suitability or manufacturing qualification.
