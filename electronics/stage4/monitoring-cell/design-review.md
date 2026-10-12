# Monitoring-cell package review

12 October 2026 · revision 0.2 · digital native schematic review only.

The initial slice used OPA391DBVR. Texas Instruments marks the DBV package as
preview information, not production data. The same Rev E datasheet identifies
OPA391DCKR as an Active, Production orderable part. All five amplifier instances
now use that DCK part. This corrects a package-selection issue without changing
the intended circuit functions or claiming an analog performance improvement.
[TI OPAx391 Rev E datasheet, first page, Table 4-1 and ordering table](https://www.ti.com/lit/ds/symlink/opa391.pdf),
[TI OPA391DCKR product page](https://www.ti.com/product/OPA391/part-details/OPA391DCKR).

| Function | DCK pad | Midpoint U2 | Integrator U101/U201 | Buffer U102/U202 |
|---|---|---|---|---|
| IN+ |1| MID_DIV | V_MID | CHx_Q_INT |
| V− |2| GND | GND | GND |
| IN− |3| V_MID | CHx_SUM | CHx_ADC_BUF |
| OUT |4| V_MID | CHx_Q_INT | CHx_ADC_BUF |
| V+ |5| +5VA | +5VA | +5VA |

The original symbol functions, functional nets and layout positions are
preserved. The explicit pin numbers, MPNs and footprints change together in the
generator, manifest, custom symbols, native sheets, BOM and KiCad exports.
The independent verifier checks all 25 amplifier pin assignments and the selected
MPN/footprint, in addition to every manifest/export pin assignment. The circuit
still contains 70 components and 245 pins; ERC alone cannot validate manufacturer
pinout or component availability.

The local footprint is KiCad 10's
`Package_TO_SOT_SMD:SOT-353_SC-70-5`. Its pins 1/2/3 are on one side at 0.65 mm
pitch, with 4/5 opposite, consistent with DCK numbering. Its pads are 1.025×0.35 mm
at x=±0.8375 mm. This generic library land pattern differs from the TI DCK0005A
recommended layout example in the datasheet. Matching package family/pitch does
not qualify a PCB land pattern. Package lead tolerances, solder-joint goals,
copper/mask/stencil and assembly process must be reviewed before PCB creation;
a TI-specific local land pattern may be preferable at that stage. No PCB exists
in this slice and no manufacturing qualification is implied.

Production part status does not establish stability, settling, endpoint charge
accuracy or suitability for implantation. The 5 V supply, 2.048 V midpoint and
continuous integrator topology remain proposed. The separate monitoring study
must bind the revised native artifacts; it must not present traces bound to the
previous DBV manifest as if generated against this revision. Existing dose,
tail, bias, protection, independent supervision and physical evidence limits
remain unchanged.
