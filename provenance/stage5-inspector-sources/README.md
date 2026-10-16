# Actual independent inspector revisions

The `09027f...` SHA256-named source is the exact LF-normalized independent
inspector that successfully produced the future and harness native receipts.
Those receipts remain bound to their actual executed code and unchanged geometry.

The current inspector corrects the reference enclosure's overall envelope to
include its four feet (panels occupy Z=8..240 mm; the assembled envelope includes
feet down to Z=0 mm). It also writes local, machine-generated successful phase
checkpoints for interruption recovery. The reference audit is rerun with this
corrected source. No CAD geometry or acceptance clearance is changed, and no
pass is reconstructed from an incomplete execution log.

The `2bf920...` source is the actual corrected inspector that completed the four
reference source/native/export phases preserved byte-for-byte in
`../stage5-reference-phases/`. Its later whole-compound distance operation did
not finish and produced no complete pass receipt. The final reference receipt
identifies `scripts/inspect_stage5_reference.py`, which explicitly binds those
completed phases and the separately completed exact solid-pair distance run,
then performs fresh saved-native validity, topology, nearest-pair witness and
material-interference checks. Each receipt retains its actual executed source.
