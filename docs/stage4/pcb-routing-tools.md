# Native PCB routing and export tools

The board package uses KiCad 10.0.6 native PCB objects and its actual Specctra
DSN/SES import/export. The saved-file KiCad MCP bridge supplies independent
metadata and electrical/design checks; a saved result is not unsaved GUI state.

Routing uses the free [Freerouting 2.5.0 release](https://github.com/freerouting/freerouting/releases/tag/v2.5.0)
with a portable [Eclipse Temurin Java 25 runtime](https://adoptium.net/temurin/releases?version=25).
The local Java version is 25.0.4.1+1. These tools were added under the authorized
assets directory without changing system PATH or redistributing their binaries
in the project. Official release digests were checked before execution.

| Local asset | SHA-256 |
|---|---|
| `freerouting-2.5.0.jar` | `f6f51bb02245e8e717f9359bd260cc9c5c0b1bc0acc8b7cb2cd5b8ffeb5de3c7` |
| `temurin25-jre.zip` | `4c95451cea98556def2c54f7782933f52a26d4a36bd85e1d59f0364464828b07` |

The local installations are in `E:\project workspace assests\tool readiness\pcb-routing`
and `E:\project workspace assests\tool readiness\java25`. Exact DSN inputs and
SES results accompany each board. Analytics are explicitly disabled. Routing
passes are bounded; unresolved nets receive a concrete fanout, placement or
supply-distribution correction followed by native checks. Autorouter completion
is not accepted as evidence in place of KiCad connectivity and DRC.

Actual populated exports use KiCad CLI. Eight missing package patterns were
built as native FreeCAD 1.1.4 solids and STEP, reimported and checked for valid
topology. They are nominal visual/mechanical representations with actual pad
datums; package tolerances and physical execution are unmeasured.

Native DRC also checks schematic parity. The portable `run_native_drc.py`
creates a temporary empty global library table while retaining every board's
actual local footprint library table. This avoids scanning hundreds of unrelated
installed global libraries. It does not suppress a test or change the user's
global configuration. Each final report must contain zero ignored checks as
well as zero violations, unconnected items and parity findings.
