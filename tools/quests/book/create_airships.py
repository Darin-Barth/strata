from dsl import *

C = chapter("create_airships", "Create: Airships", group="tech", icon="aeronautics:propeller_bearing",
            subtitle="Build it, glue it, fly it")
q = C.quest

q("intro", "Build. Fly. Explore.", deps="welcome/path_tech", icon="aeronautics:propeller_bearing",
  size=1.5, shape="gear", desc="""
    This is what Strata is named for. With &eCreate Aeronautics&r you build a ship out of
    normal blocks, any shape you like, and it becomes a real physics object: it floats,
    tilts, falls and flies. &eAviator's Goggles&r show thrust, lift and airflow.

    Every airship needs three things:
    &b1. Lift&r: a balloon full of hot air or steam (or Levitite later).
    &b2. Thrust&r: propellers or thrusters, spun or fueled from on board.
    &b3. Control&r: a steering wheel, levers or a cockpit.

    Start tiny. A raft with a balloon and one propeller is a perfect first ship.""",
  rewards=[give("create:andesite_alloy", 16), give("minecraft:white_wool", 32)])

# --- your first ship ------------------------------------------------------------------------
q("assemble", "Physics Assembler", deps="intro", icon="simulated:physics_assembler",
  tasks=[item("simulated:physics_assembler"), item("create:super_glue")], desc="""
    Build your ship, put a &ePhysics Assembler&r on it, and select the ship with
    &eSuper Glue&r (or &eHoney Glue&r): drag a box around it. Then hold right-click on
    the assembler and pull its lever.

    Your build is now a &eSimulated Contraption&r. Walk on it, open chests on it, use
    machines on it. Any Physics Assembler turns it back into blocks.

    Ponder the assembler with &eW&r first!""",
  rewards=[give("minecraft:slime_ball", 8), give("create:andesite_casing", 4)], tier=2)

q("envelope", "Balloon Fabric", deps="assemble", icon="aeronautics:white_envelope",
  tasks=item("aeronautics:white_envelope", 32), desc="""
    &eHot Air Envelope&r blocks are balloon walls (wool and sticks). Build a closed,
    airtight bag with them: hot air fills it from the top down.

    A bigger balloon gives more lift. Blocks inside the balloon take up space and
    reduce lift. Right-click with dye to paint it.""",
  rewards=[give("minecraft:white_wool", 32), give("minecraft:stick", 32)])

q("burner", "Hot Air Burner", deps="envelope", icon="aeronautics:adjustable_burner",
  tasks=item("aeronautics:adjustable_burner"), size=1.5, shape="hexagon", desc="""
    Put a &eHot Air Burner&r under the balloon's opening and give it a &eredstone&r
    signal: it fills the balloon above with hot air and your ship rises.

    A stronger signal means more hot air. Set the maximum on its panel.
    Ships settle where lift and weight balance, so &ea lever and a redstone dial are your
    altitude control&r. Several burners can share one balloon.""",
  rewards=[give("minecraft:redstone", 16), give("minecraft:lever", 4)], tier=3)

q("propellers", "Propellers", deps="burner", icon="aeronautics:andesite_propeller",
  tasks=item("aeronautics:andesite_propeller", 2), desc="""
    Floating is nice; going somewhere is better. An &eAndesite Propeller&r (or Wooden
    Propeller) pushes air when its shaft spins. Reverse the spin (or wrench it) to
    reverse the thrust.

    Propellers need &erotation on board&r: see the Portable Engine quest.""",
  rewards=[give("create:shaft", 16), give("create:cogwheel", 4)])

q("engine", "Portable Engine", deps="assemble", icon="simulated:white_portable_engine",
  tasks=item("simulated:white_portable_engine"), desc="""
    Water wheels don't fly. The &ePortable Engine&r burns fuel to make rotation right on
    your ship, in either direction. Funnels or chutes can feed it fuel.

    A &eBlaze Cake&r superheats it for extra power. Bring spare fuel on long trips!""",
  rewards=[give("minecraft:coal", 32), give("minecraft:charcoal", 16)], tier=2)

q("prop_bearing", "Big Propellers", deps=["propellers", "engine"],
  icon="aeronautics:propeller_bearing", tasks=item("aeronautics:propeller_bearing"), desc="""
    A &ePropeller Bearing&r spins whatever you build on its front as a propeller.
    Any shape counts as long as it has at least two sail-like blocks; more sails means
    more thrust. Big props on big ships!

    Air gets thinner the higher you go, so propellers push less at high altitude.""",
  rewards=[give("create:white_sail", 8)], tier=2)

q("steering", "Steering Wheel", deps="prop_bearing", icon="simulated:steering_wheel",
  tasks=[item("simulated:steering_wheel"), item("simulated:throttle_lever")], desc="""
    Hold right-click on a &eSteering Wheel&r and move the mouse to turn it; it gives a
    precise rotation to whatever it's connected to (like a bearing that swings a rudder
    or tilts a propeller). Sneak to snap to 45°.

    A &eThrottle Lever&r is a smooth redstone dial: drag it to set 0 to 15. Perfect for
    a burner or a thruster.""",
  rewards=[give("create:brass_ingot", 4)], tier=2)

q("altitude", "How High?", deps="burner", icon="simulated:altitude_sensor",
  tasks=item("simulated:altitude_sensor"), desc="""
    Air pressure drops as you climb, so lift and thrust get weaker the higher you go.
    That gives every ship a natural ceiling.

    The &eAltitude Sensor&r reads the air pressure as a redstone signal. Wire it to your
    burner to hold a steady height on autopilot. A &eNavigation Table&r with a compass
    or map points its redstone toward a destination, so a ship can steer itself.""",
  rewards=[give("minecraft:comparator", 2), give("minecraft:repeater", 4)])

q("helicopter", "Helicopters", deps="prop_bearing", icon="aeronautics:gyroscopic_propeller_bearing",
  tasks=item("aeronautics:gyroscopic_propeller_bearing"), desc="""
    A normal propeller pointing up makes a wobbly helicopter. The &eGyroscopic Propeller
    Bearing&r tries to keep its propeller upright, so your chopper stays level.

    It needs a &eGyroscopic Mechanism&r, made by sequenced assembly like a precision
    mechanism. A redstone signal resets its tilt.""",
  rewards=[give("create:precision_mechanism")], tier=3)

q("steam_vent", "Steam Balloons", deps=["burner", "welcome/nether"], icon="aeronautics:steam_vent",
  tasks=item("aeronautics:steam_vent"), desc="""
    The &eSteam Vent&r fills a balloon with &esteam&r from a boiler on your ship. Like a
    steam engine, it needs heat (Blaze Burners), water and enough boiler size.

    Bigger ships, bigger boilers. Redstone controls it like a hot air burner.""",
  rewards=[give("create:fluid_tank", 4)], tier=3)

# --- controls -------------------------------------------------------------------------------
q("cockpit", "Build a Cockpit", deps="steering", icon="aeroworks:control_stand",
  tasks=[item("aeroworks:control_stand"), item("aeroworks:lever_module")], desc="""
    &eCreate: Aeroworks&r adds proper flight controls. Put &eControl Modules&r (levers,
    throttles, joysticks, yokes, pedals, buttons) into the sockets of a &eControl Stand&r
    or &eControl Desk&r.

    Sneak-right-click to bind each control to keys and Redstone Link frequencies.
    Right-click with an empty hand to take control; press &eEsc&r to let go.
    Consoles that touch become one deck. &eMechanical Servos&r turn rudders to an exact
    angle, and a &eGyroscope&r helps keep the ship level.""",
  rewards=[give("create:redstone_link", 4)], tier=3)

q("wires", "Drive-By-Wire", deps="cockpit", icon="drivebywire:wire",
  tasks=[item("drivebywire:wire"), item("drivebywire:controller_hub")], desc="""
    Running redstone across a big ship is messy. &eDrive-By-Wire&r &eCables&r connect a
    redstone source to any block on the same assembled ship directly.

    Bind a controller to a &eLinked Controller Hub&r and run the whole network from the
    controller. A &eBackup Block&r saves your wiring when you turn the ship into a
    schematic. Got a game pad? The &eTweaked Linked Controller&r maps its sticks and
    triggers to Redstone Link frequencies.""",
  rewards=[give("minecraft:redstone", 16)], tier=2)

q("controller", "Contraption Controller", deps="cockpit",
  icon="createthrusters:analogue_contraption_controller",
  tasks=item("createthrusters:analogue_contraption_controller"), desc="""
    &eAeronautics: Gadgets & Gizmos&r adds the &eSable Contraption Controller&r: map flight
    controls to keys, redstone, wireless frequencies or blocks on your ship, all in one
    place.

    The same mod adds &eSmart Glasses&r (live force readouts), &eShip Couplers&r for
    towing, and &eNavigation Tables&r that steer toward a map target.""",
  rewards=[give("create:electron_tube", 4)], tier=3)

# --- thrusters and wings --------------------------------------------------------------------
q("gg_thruster", "Thrusters", deps="prop_bearing", icon="createthrusters:thruster",
  tasks=item("createthrusters:thruster"), desc="""
    No propeller needed: a Gadgets & Gizmos &eThruster&r burns fuel (solid or liquid) and
    pushes your ship away from its nozzle. Redstone sets the throttle: 0 off, 15 full.

    Mount it on a &eServo Bearing&r to swing the thrust around. &eRCS Thrusters&r have four
    small nozzles for fine steering and run on rotation instead of fuel.""",
  rewards=[give("minecraft:coal_block", 4)], tier=3)

q("propulsion", "Propulsion Thrusters", deps="prop_bearing", icon="createpropulsion:thruster",
  tasks=[item("createpropulsion:thruster"), item("createpropulsion:turpentine_bucket")], desc="""
    &eCreate Propulsion&r thrusters burn &eTurpentine&r: crush spruce logs for
    &ePine Resin&r, then mix it with water in a basin.

    Pipe turpentine into a Propulsion &eThruster&r and give it redstone: directional
    thrust. Eight thrusters in a 2x2x2 cube (or 27 in a 3x3x3) merge into one big engine
    fed from the back.

    Later: the &eIon Thruster&r runs on FE, &eVector Thrusters&r tilt their own nozzle,
    and light &eWings&r make fast ships fly more like planes.""",
  rewards=[give("create:fluid_pipe", 16), give("minecraft:spruce_log", 32)], tier=3)

# --- utility --------------------------------------------------------------------------------
q("ropes", "Ropes and Winches", deps="assemble", icon="simulated:rope_winch",
  tasks=[item("simulated:rope_winch"), item("simulated:rope_coupling", 2)], desc="""
    Tie two contraptions (or a contraption and the ground) together: right-click a
    &eRope Winch&r and a connector with a &eRope Coupling&r. Spin the winch to reel the
    rope in and out.

    Lower cargo from a hovering ship, or tow a barge! Right-click a rope while holding a
    wrench to slide down it.""",
  rewards=[give("minecraft:string", 16)], tier=2)

q("wheels", "Land Vehicles", deps="assemble", icon="offroad:tire",
  tasks=[item("offroad:wheel_mount", 4), item("offroad:tire", 4)], desc="""
    Not everything has to fly. &eOffroad&r (part of Aeronautics) adds &eWheel Mounts&r
    and tires. Spin the mounts and build a car, a truck or a rover.

    The &eBorehead Bearing&r with &eRock Cutting Wheels&r turns a vehicle into a tunnel
    borer.""",
  rewards=[give("create:shaft", 8), give("create:cogwheel", 8)], tier=2)

q("levitite", "Levitite", deps=["burner", "welcome/nether"], icon="aeronautics:levitite",
  tasks=item("aeronautics:levitite", 8), desc="""
    &dLevitite&r is a magic crystal that holds a ship up all by itself. Crush &eEnd Stone&r
    into powder, mix it with zinc nuggets and water in a heated basin to get Levitite
    Blend, then heat the blend so it crystallizes. It spreads through the whole pool.

    Levitite can't climb by itself (you still need thrust), and it drags at low speed.
    You'll need End Stone, so this one waits until you reach &5the End&r.""",
  rewards=[give("create:zinc_nugget", 16)], tier=4)

# --- personal flight ------------------------------------------------------------------------
q("sa_jetpack", "Steam Jetpacks", deps=["engine", "welcome/nether"], icon="create_sa:brass_jetpack_chestplate",
  tasks=item("create_sa:andesite_jetpack_chestplate"), desc="""
    &eCreate Stuff 'N Additions&r jetpacks let you fly a little, and they &cburn fuel&r
    every second you use them.

    &eAndesite Jetpack&r: burns fuel like coal (refill at a &eFueling Tank&r).
    &eCopper&r: high-pressure water (refill at a &eFilling Tank&r or with water buckets).
    &eBrass&r: water and fuel together, as steam. Each one has a height limit.
    To refill by hand, hold the jetpack in your offhand and drop the fuel (see its tooltip).""",
  rewards=[give("minecraft:coal", 32)], tier=3)

q("jetpack", "Create Jetpack", deps=["sa_jetpack"], icon="create_jetpack:jetpack",
  tasks=item("create_jetpack:jetpack"), size=1.5, shape="hexagon", desc="""
    The &eCreate Jetpack&r runs on &bpressurized air&r, like a backtank: it empties while
    you fly. Place it down and spin it with rotation to refill it, just like a Copper
    Backtank. It has a hover mode and its own keys (see Options > Controls).

    It's a big mechanical-crafter recipe with an &eElytra&r inside, so it's a late reward.
    A netherite version exists too.""",
  rewards=[give("create:copper_backtank")], tier=4)

# --- where next -----------------------------------------------------------------------------
q("next", "Where Next?", deps=["steering", "propellers"], icon="minecraft:oak_sign", shape="square",
  desc="""
    You can fly! Now go places:

    &aExplorer's Guide&r: sky islands, far-off structures and new biomes to land at.
    &bCreate: Trains & Trade&r: run a cargo line between ship docks.
    &bCreate: Extras&r: mount Big Cannons on your ship (pirates!).

    Tip: Distant Horizons (optional, client-side) shows far terrain while you fly.""")
