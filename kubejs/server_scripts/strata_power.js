// The power grid (docs/design-doc.md, power): Crafts & Additions wires locally, IE LV/MV/HV for long
// distance. Create: New Age's own wiring hangs its wires between Electrical Connectors, so the
// connector recipe goes (its wires stay craftable: copper wire is an ingredient of its copper
// circuit). New Age generators still hand FE over through their carbon brushes, which C&A
// connectors and IE wire connectors accept. The Street Light needs a connector, so it goes too.
// The alternator's lower output is in config/createaddition-common.toml (240 FE at max RPM).
// KubeJS server scripts share one scope: every top-level name here starts with "strataPower".
const strataPowerRemoved = [
  'create_new_age:shaped/electrical_connector',
  'create_new_age:shaped/street_light',
]

ServerEvents.recipes(event => {
  strataPowerRemoved.forEach(id => event.remove({ id: id }))
})
