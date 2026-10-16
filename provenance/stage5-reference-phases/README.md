# Completed independent reference phases

These four JSON files are byte-for-byte copies of successful, machine-written
independent FreeCAD inspection checkpoints. Each operation completed before its
file was written. They are not reconstructed from console logs or CAD producer
assertions. Their bindings identify the exact executed inspector source,
FreeCAD version, reference contract, saved native assembly, neutral exports and
all eight original populated board and native PCB sources.

The executed inspector is preserved under its SHA256 name in
`../stage5-inspector-sources/`. The complete original run did not finish its
whole-compound distance operations. It produced no final pass receipt.

`scripts/inspect_stage5_reference.py` explicitly reuses these completed phases,
verifies every current input binding, reopens the saved native assembly for
fresh validity, inventory, solid coverage and material-interference checks, and
binds the separately completed exact constituent-solid clearance inspection.
Its final receipt identifies this driver and every reused evidence file. No
checkpoint key or executed-source hash is migrated to another implementation.

The portable verifier checks these source and evidence bindings again. This is
nominal digital geometry evidence; it supplies no physical qualification.
