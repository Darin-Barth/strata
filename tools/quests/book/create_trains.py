from dsl import *

C = chapter("create_trains", "Create: Trains & Trade", group="tech", icon="create:track_station",
            subtitle="Railways, stations, packages and shops")
q = C.quest

q("intro", "Why Trains?", deps="welcome/path_tech", icon="create:controls", size=1.5,
  shape="gear", desc="""
    Strata has &cno free teleporting&r, so getting people and stuff around is a big deal.
    &eCreate trains&r are the answer: you build the train yourself, block by block,
    and it drives your tracks on a timetable.

    Trains carry players, chests and tanks between your bases, mines and farms.
    Later, they're how goods cross between far-away places before wireless exists.

    You'll need brass for most train parts (see &bCreate: Getting Moving&r).""")

# --- the railway ----------------------------------------------------------------------------
q("track", "Lay Some Track", deps="intro", icon="create:track",
  tasks=item("create:track", 64), desc="""
    &eTrain Track&r is placed like rails, but it curves and slopes smoothly.
    Click one spot, then click where the track should end: it builds the whole curve.
    Ponder it with &eW&r for the rules on curves and slopes.

    Train tracks don't need power; trains do the work.""",
  rewards=[give("minecraft:iron_nugget", 64), give("minecraft:gravel", 32)], tier=2)

q("station", "Train Station", deps="track", icon="create:track_station",
  tasks=item("create:track_station"), desc="""
    Hold a &eTrain Station&r, right-click a track, then place the station beside it.
    Stations are where trains are &eassembled&r, &edisassembled&r and where they stop.
    Name each station: schedules use the names.""",
  rewards=[give("minecraft:name_tag", 2)])

q("first_train", "Build a Train", deps="station", icon="create:railway_casing",
  tasks=[item("create:railway_casing", 4), item("create:controls")], size=1.5, shape="hexagon",
  desc="""
    Right-click the track at the station with &eTrain Casing&r to place a &ebogey&r.
    Build your train on top, add &eTrain Controls&r facing the front, glue it with
    Super Glue, and click &eAssemble&r on the station.

    Sit at the controls and drive with your movement keys. Start small!
    &eChairs&r (Bits 'n' Bobs, Interiors) keep passengers seated; &eHeadlamps&r and
    Steam 'n' Rails smokestacks and whistles make it look the part.""",
  rewards=[give("create:super_glue"), give("create:white_seat", 4)], tier=3)

q("schedule", "Timetables", deps="first_train", icon="create:schedule",
  tasks=item("create:schedule"), desc="""
    A &eTrain Schedule&r tells a train where to go and how long to wait.
    Write stops into it, then right-click a mob sitting at the controls (or yourself
    seated) with it. That mob becomes the &econductor&r and the train runs by itself.

    Loop between two stations and you have a shuttle.""",
  rewards=[give("minecraft:lead", 2), give("minecraft:paper", 8)], tier=2)

q("signals", "Signals", deps="schedule", icon="create:track_signal",
  tasks=item("create:track_signal", 4), desc="""
    More than one train on a line? Use &eTrain Signals&r to split track into sections.
    A train waits until the section ahead is empty, so trains don't crash.

    &eSemaphores&r from Steam 'n' Rails go on a pole above a signal and show its state
    like a real railway. A &eDisplay Link&r on a station can write the next arrival
    onto &eDisplay Boards&r or Bits 'n' Bobs &eNixie Boards&r.""",
  rewards=[give("minecraft:redstone", 16), give("create:andesite_alloy", 16)], tier=2)

# --- Steam 'n' Rails ------------------------------------------------------------------------
q("handcar", "Handcar", deps="track", icon="railways:handcar",
  tasks=item("railways:handcar"), desc="""
    &eSteam 'n' Rails&r adds lots of train extras. The &eHandcar&r is a tiny ready-made
    rail vehicle: put it on a track and ride. Pick it up again with a wrench.
    It also adds &enarrow&r, &ewide&r and &emonorail&r tracks, each with its own bogeys.""",
  rewards=[give("create:track", 16)])

q("coupler", "Coupling Cars", deps="first_train", icon="railways:track_coupler",
  tasks=item("railways:track_coupler"), desc="""
    The &eTrain Coupler&r joins two trains into one, or splits them apart, without
    disassembling anything. Select a track, place the coupler next to it and power it
    with redstone when the cars line up. Stations help with lining up.""",
  rewards=[give("minecraft:redstone", 8)])

q("switch", "Track Switches", deps="first_train", icon="railways:track_switch_andesite",
  tasks=item("railways:track_switch_andesite"), desc="""
    A &eTrack Switch&r forces trains at a junction to go left, right or straight.
    Use it to cycle, or control it with redstone. Brass switches are fancier.""",
  rewards=[give("create:track", 16)])

q("conductor", "A Robot Conductor", deps="schedule", icon="railways:white_conductor_cap",
  tasks=item("railways:white_conductor_cap"), desc="""
    No spare mob to drive your train? Put a &eConductor's Cap&r on an
    &eAndesite Casing&r and it becomes a little &eConductor&r that can run a schedule.

    Conductors also press buttons and flip levers you look at, and can wear a toolbox.""",
  rewards=[give("create:andesite_casing", 2)], tier=2)

# --- packages and logistics -----------------------------------------------------------------
q("packager", "Packages", deps="intro", icon="create:packager",
  tasks=[item("create:packager"), item("create:cardboard", 8)], desc="""
    Create can wrap items into &epackages&r with an address written on them.
    A &ePackager&r on a chest boxes up its items; packages then travel by belt, chain
    conveyor or train to the place with the matching name.

    Ponder the Packager with &eW&r: it's the start of Create's delivery network.""",
  rewards=[give("minecraft:paper", 16)], tier=2)

q("frogport", "Frogports and Chains", deps="packager", icon="create:package_frogport",
  tasks=[item("create:package_frogport", 2), item("create:chain_conveyor", 2)], desc="""
    &eChain Conveyors&r string chains between cogs; packages ride along them.
    A &ePackage Frogport&r (yes, a frog) catches and sends packages at each end.

    Trains can carry packages too, using &ePostboxes&r at stations.""",
  rewards=[give("minecraft:chain", 16)], tier=2)

q("stock", "Order from Storage", deps="frogport", icon="create:stock_ticker",
  tasks=item("create:stock_ticker"), desc="""
    A &eStock Ticker&r lists everything in the connected storage. Order what you need
    and it packages it up and sends it to you.""",
  rewards=[give("create:brass_ingot", 8)], tier=2)

q("cash_register", "Open a Shop", deps="stock", icon="createadditionallogistics:cash_register",
  tasks=item("createadditionallogistics:cash_register"), desc="""
    &eCreate: Additional Logistics&r adds a &eCash Register&r: a stock ticker for shops that
    writes every sale into a &eSales Ledger&r. Click a stock keeper with the ledger to
    restock what sold.

    It also adds the &ePackage Editor&r (rewrite addresses) and &eLazy Shafts&r
    (cheaper long shaft lines).""",
  rewards=[give("minecraft:emerald", 4)], optional=True)

q("silo", "Bigger Storage", deps="packager", icon="create_connected:item_silo",
  tasks=item("create_connected:item_silo", 4), desc="""
    &eCreate: Connected&r adds handy blocks: the &eItem Silo&r (a vault that stacks
    upward), the horizontal &eFluid Vessel&r, extra gearboxes and clutches, and the
    &eKinetic Battery&r that stores rotation.""",
  rewards=[give("create:iron_sheet", 8)], optional=True)

# --- money ----------------------------------------------------------------------------------
q("coins", "Money, Money", deps="intro", icon="numismatics:spur", desc="""
    &eCreate: Numismatics&r adds coins: &eSpur&r, &eBevel&r, &eSprocket&r, &eCog&r,
    &eCrown&r and &eSun&r, from smallest to biggest. Hover over a coin to see its value.

    Coins can't be crafted. Here are a few to start your economy. Sell things to friends
    and they flow around the server.""",
  rewards=[give("numismatics:spur", 32), give("numismatics:bevel", 8)])

q("vendor", "Vendors", deps="coins", icon="numismatics:vendor",
  tasks=item("numismatics:vendor"), desc="""
    A &eVendor&r is a shop block. Sneak-right-click to set it up: what it sells
    (or buys), how many, and the price in coins. Friends right-click it to trade,
    even when you're offline.

    Tip: drag an item from the EMI list into the filter slot to set it.
    A &eDepositor&r gives a redstone pulse when someone pays it: a ticket gate for your
    train, or a toll bridge.""",
  rewards=[give("numismatics:bevel", 4)], tier=2)

q("bank", "Open a Bank Account", deps="coins", icon="numismatics:bank_terminal",
  tasks=[item("numismatics:bank_terminal"), item("numismatics:white_card")], desc="""
    The &eBank Terminal&r opens your account: deposit coins so you don't carry them.
    A &eBank Card&r bound to your account pays at vendors and depositors.

    A &eBanking Guide&r on a Blaze Burner makes a &eBlaze Banker&r: a shared account,
    perfect for a team treasury.""",
  rewards=[give("numismatics:sprocket", 2)], tier=2)

q("trading_depot", "Automatic Villager Trades", deps="intro", icon="trading_floor:trading_depot",
  tasks=item("trading_floor:trading_depot"), desc="""
    &eCreate: Trading Floor&r's &eTrading Depot&r goes next to a villager's workstation.
    Feed it the trade items and the villager trades automatically, all day.
    (Villagers only trade during their working hours.) Two depots together handle
    trades that need two items.""",
  rewards=[give("minecraft:emerald", 8)], tier=2)

# --- where next -----------------------------------------------------------------------------
q("next", "Where Next?", deps=["schedule", "vendor"], icon="minecraft:oak_sign", shape="square",
  desc="""
    Rails are down and the shops are open. Next:

    &bCreate: Airships&r: take your goods into the sky.
    &bCreate: Power & Wires&r: diesel engines and steam for bigger trains.
    &bLogistics&r and &bStorage&r: more ways to move and keep items.""")
