# Target firmware tools

12 October 2026. **Compiler installation checked; complete SDK installation and
application-core example build are still in progress.** This is a tool-readiness
record. The full ATO processor backend remains unimplemented.

The Stage 2 processor witness is nRF5340. Its native firmware work needs a
supported Arm compiler, Nordic/Zephyr headers, build tools and a linked target
image. The existing portable C tests execute on the host and do not provide
those results.

## Selection and observed installation

The official stable release selected is
[nRF Connect SDK v3.4.1](https://github.com/nrfconnect/sdk-nrf/releases/tag/v3.4.1).
Nordic's SDK manager reports its matching toolchain bundle as `4f5b6ad6dd`.
The supported [SDK-manager installer](https://docs.nordicsemi.com/r/bundle/nrfutil/page/nrfutil-sdk-manager/guides/sdk_manager_installing.html/basic-usage)
installs both SDK and toolchain. This project needs no paid IDE or physical
development board to cross-compile its digital artifacts.

Observed checks:

- Official nRF Util executable: **8.2.1**; Windows Authenticode signature valid,
  signer **Nordic Semiconductor**.
- Download SHA256: `22cb1bd03fc29016670c1fc8408a78bd213286ecc1156c70712485d77b097c75`.
- Installed SDK-manager command: **1.16.1**.
- Matching toolchain installed; its compiler responds as
  **arm-zephyr-eabi-gcc 14.3.0 (Zephyr SDK 1.0.1)**.
- The SDK source bundle is still downloading. No complete example-build result
  or ATO target firmware result is claimed at this checkpoint.

Tools physically reside in
`E:\project workspace assests\Firmware\Nordic`. Nordic/Zephyr
[application paths cannot contain spaces](https://nrfconnectdocs.nordicsemi.com/ncs/latest/nrf/app_dev/create_application.html),
so two local junctions provide short build paths:

| Alias | Physical destination |
|---|---|
| `E:\ATO-Tools` | `E:\project workspace assests\Firmware\Nordic` |
| `E:\ATO` | `E:\Project ATO` |

The project and asset folders remain authoritative. The aliases reuse those
directories; they are not duplicate checkouts. Installer command data and logs
use the process-local `NRFUTIL_HOME=E:\ATO-Tools\nrfutil-home` setting. No global
PATH change or physical-device operation is needed for this workflow.

The active installation command is:

```powershell
$env:NRFUTIL_HOME='E:\ATO-Tools\nrfutil-home'
& E:\ATO-Tools\nrfutil.exe sdk-manager install v3.4.1 --install-dir E:\ATO-Tools\ncs
```

## Next verification

After the installer completes, run the
[example cross-compilation check](../../scripts/check_nordic_toolchain.py):

```powershell
.\.venv\Scripts\python.exe scripts\check_nordic_toolchain.py
```

It builds the **unmodified SDK hello_world** example for
`nrf5340dk/nrf5340/cpuapp` in an ignored project build directory. It records tool
versions, source/ELF identities and section sizes only after successful linking.
Its build log stays under `tmp/nordic-toolchain-check`. The command performs no
flashing or physical execution.

That result will establish the installation's basic build path. It will not
close ATO firmware integration, application/network memory budgets, ADC/DMA/bus
arbitration, timer/DPPI timing, delivered-charge observation or fault shutdown.
Those require the actual ATO backend and their own verification artifacts.
