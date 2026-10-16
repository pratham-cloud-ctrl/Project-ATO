# Stage 5 reference mechanical design

The reference assembly packages all eight frozen Stage 4 populated circuit boards at their original scale. It is a 600×310×240mm service chassis, not an implant enclosure. The independent future implant allocation is a separate concept; none of these boards is scaled down to fit it.

## Layout and service method

Two unequal bays carry four removable horizontal trays each. The left bay, bottom to top, contains supervision, power, current driver and contact router. The right contains recording front end, monitoring cell, monitoring transport and controller carrier. The 50 mm tier pitch leaves at least24 mm between the tallest current fitted source package and the next tray. The highest board has additional space under the lid. Each tray is 2 mm nominal insulating sheet with a 6 mm rear stop, a finger grip and dedicated angle rails. Each board sits on four 10 mm nominal insulating M3 standoffs. All 32 mount axes come directly from the frozen KiCad mounting footprints; they are 4 mm from board edges. There are 64 board mounting screws, eight flush lid screws and four flush front cover screws.

The actual populated STEP compounds are retained, including the original detailed fitted packages, underside leads and board holes. The `SourceSTEP`, checksum and rigid translation properties on each native PCB object make its source traceable. Native boxes, cylinders and boolean cuts retain editable dimensions for trays, mounting bores, rails, panels and cover holes. Imported source boards remain frozen geometry.

Disconnect external power before opening. Remove the lid and front cover, label and disconnect a tray's harness plugs, then withdraw it toward negativeY. Reserve 310 mm of clear space in front. No energized hot-swapping or blind-mate insertion is proposed. The enclosure is referenced to X=left-to-right, Y=front-to-rear and Z=bottom-to-top. The source KiCad STEP Y coordinate is negative, so board placement uses(X,30+boardDepth,28+50tier) without scaling or rotation.

## Interfaces and space

The central cable spine is X336..374, Y20..290, Z18..230 mm. The rear corridor begins behind the rear frame posts at Y296 and ends at the rear wall's inner face Y307. An additional 26 mm right corridor lies at X571..597. The rear panel has a 90 × 28 mm artificial-load opening and a 100 × 28 mm companion/power/debug opening. Their lower edge is Z194; their upper edge is Z222. These are mechanical pass-through allocations, not certified panel connector interfaces. The harness models supply mating geometry, routing plans and bend reservations.

The rear panel contains twelve 4 × 17 mm ventilation slots. Their inclusion does not establish airflow, cooling or ingress performance. The power and recording grounds remain defined by the electronics; this model adds no claimed protective-earth or conductive shield bond. Insulating board support is a design allocation rather than an insulation certification.

## Nominal hardware and materials

Base, front, rear and side panels are 3 mm nominal aluminium. The lid is 3 mm clear polycarbonate. The rail and 6 mm square frame posts are nominal aluminium. Trays and standoffs are nominal insulating polymer, and four 10 mm-radius adhesive elastomer feet provide the 8 mm base offset. No alloy temper, polymer grade, flame rating or machining process has been qualified. The lower screw heads lie under each tray and above the rail-free mounting zone. Threads are omitted; nominal 2.9 mm shafts have radial clearance inside 3 mm modeled standoff bores. This avoids treating a simplified solid interference as thread qualification. Flush cover screws sit in stepped counterbores; final production countersink or counterbore hardware must be selected and dimensioned to a manufacturer part.

## Verification boundary

The producer checks native shape validity, dependency features, source hashes, component count and all source solids. A separate independent checker compares each transformed PCB compound with its original STEP and tests mounting geometry, intended contacts, part clearances and interference. Its result is authoritative for the bounded digital geometry release. Reopening a model, passing shape validity or obtaining a zero-interference report is not physical qualification. Structural loads, tray sag, fastener torque/pullout, creep, shock, vibration, cable fatigue, grounding, EMI, thermal performance, ingress, electrical safety and implant suitability remain untested.

The mechanical STEP and per-part STL files are inspectable fabrication references. They are not manufacturing approval. The full assembly and exploded STEP contain the real populated boards; the mechanical-only STEP permits enclosure inspection without those electronics.
