from dsl import *

# The Hollow (docs/hollow-progression.md sections 3-4, docs/hollow-design.md). Arrival runs along the
# middle; four rows leave "first_light": survival (above), exploration (middle), the Lost Signal story
# (below) and the boss ladder (top). All converge on the Pale Beacon, the Sanctuary and "The Survey
# Complete". Gate materials (Hollow Embers, Holy Cross, Templar Artifact, bone staffs, echolocation
# organs, darksteel) are never rewards. Hand-placed (at=) to keep the tracks in their rows.
C = chapter("the_hollow", "The Hollow", group="explore", icon="strata:pale_lantern",
            subtitle="Keep your lights lit, read what they left, light the Pale Beacon")
q = C.quest

q("intro", "What is the Hollow?", icon="strata:hollow_ember", at=(0.0, 4.5),
  shape="gear", size=1.5, rewards=give("minecraft:soul_torch", 16), desc="""
    The &5Hollow&r is a horror dimension: endless night, thick fog, and every horror mob in the pack lives here and nowhere else. Going there is &eoptional&r, and it's &cdangerous&r.

    Why go? Its chests and its monsters hold &5Hollow Embers&r, a material that unlocks strong items all across the pack, and its bosses drop trophies you can't get anywhere else.

    The big goal: light a &bPale Beacon&r, the only safe ground in the Hollow, and find out what happened to the last people who tried.""")

q("lantern", "The Pale Lantern", deps="intro", icon="strata:pale_lantern", at=(1.75, 4.5), tier=2,
  tasks=item("strata:pale_lantern"), rewards=give("minecraft:soul_lantern", 2), desc="""
    Craft the &ePale Lantern&r from a &eCreaking Heart&r, &eresin clumps&r and a &esoul lantern&r. Press &eR&r on it for the recipe.

    Creaking Hearts sit inside the pale oak trees of &bPale Gardens&r. Mine one with &eSilk Touch&r, or it just breaks into resin. Taking the heart ends that garden's resin, so gather what you need first. The soul lantern needs soul sand or soil from the Nether.""")

q("enter", "Through the Static", deps="lantern", icon="minecraft:resin_bricks", at=(3.5, 4.5), tier=3,
  tasks=dim("strata:hollow", title="Enter the Hollow"), rewards=give("minecraft:cooked_beef", 8), desc="""
    Build a frame of &eResin Bricks&r the shape of a Nether portal and use the &ePale Lantern&r on it. The lantern isn't used up.

    The portal fills with grey static, like a dead TV channel. Step in. It links back to the Overworld at the same spot.""")

q("rules", "The Rules of the Dark", deps="enter", icon="minecraft:clock", at=(5.25, 4.5), shape="hexagon",
  rewards=give("minecraft:lantern", 4), desc="""
    The Hollow has its own rules:

    &5Always night:&r and fog so thick you see about 10 blocks. Hold a light in either hand to see further.
    &5No sleeping:&r beds don't work here (with one exception you'll learn about). Compasses and clocks spin.
    &5Sanity drains:&r watch the meter. Low sanity brings hallucinations, and below &c25%&r some of them become real and attack.
    &5It plays tricks:&r footsteps, whispers, a figure at the edge of your sight. Those can't hurt you.
    &5Scary but fair:&r every threat has a warning and a counter, and no single hit from a horror mob takes more than &c40%&r of your health. Bosses hit as hard as they like.

    Click the checkmark when you're ready.""")

q("first_light", "First Light", deps="rules", icon="sanity_renewed:garland", at=(7.0, 4.5), tier=2,
  tasks=[item("sanity_renewed:garland"), check()], rewards=give("minecraft:campfire", 2), desc="""
    Light is your best friend here. &eCampfires&r and &elanterns&r slowly restore sanity when you stay near them, and so do your friends: stick together.

    Make a &eGarland&r (Sanity: Renewed; press &eR&r on it) and build a small lit camp near the portal. Resting outside the Hollow also brings your sanity back. Click the checkmark once your camp is lit.""")

# --- survival track ---
q("detector", "Timey-Wimey Detector", deps="first_light", icon="weeping_angels:timey_wimey_detector",
  at=(8.75, 1.5), tier=2, tasks=item("weeping_angels:timey_wimey_detector"), rewards=give("minecraft:torch", 32), desc="""
    &cWeeping Angels&r are stone statues that only move when nobody is looking at them. Keep your eyes on them and back away, and keep your lights up.

    The &eTimey-Wimey Detector&r warns you when one is near. To break one, use a &epickaxe&r: other weapons barely scratch them.""")

q("darksteel", "Darksteel", deps="detector", icon="grim_and_bleak:darksteel", at=(10.5, 1.5), tier=3,
  tasks=[item("grim_and_bleak:raw_darksteel"), item("grim_and_bleak:darksteel", 8), item("grim_and_bleak:darksteell_sword")],
  rewards=give("minecraft:iron_ingot", 16), desc="""
    Normal ores don't grow in the Hollow's grimstone. Its metal is &eDarksteel&r: mine &eDarksteel Ore&r and smelt the raw ore into ingots.

    Darksteel makes &eGrim & Bleak&r's tools, weapons and armor, and several of its weapons have useful extras. You'll also need ingots for the Cursed Amulet and the Gate Key later on.""")

q("listening", "Something Is Listening", deps="darksteel", icon="the_ravenous:anti_ravenous", at=(12.25, 1.5), tier=3,
  tasks=[kill("the_ravenous:the_screecher"), item("the_ravenous:anti_ravenous")],
  rewards=give("minecraft:golden_carrot", 8), desc="""
    &cThe Ravenous&r hunts by sound. Building, digging and opening chests can call it from far away, and it &ceats through blocks&r to reach you. A screech comes before the chase: when you hear it, move.

    Its young, the &cScreechers&r, carry an echolocation organ. Use one to craft the &eAnti-Ravenous&r: it stuns everything within 25 blocks and buys you time to run.""")

q("walls", "Sound Walls", deps="listening", icon="minecraft:obsidian", at=(14.0, 1.5), tier=2,
  tasks=[item("minecraft:obsidian", 32), check()], rewards=give("minecraft:obsidian", 16), desc="""
    Nothing you build here is safe by default: the Ravenous chews through planks and stone. &eObsidian&r is too tough for it, so a camp you want to keep needs obsidian walls.

    Build a shelter it can't eat into, then click the checkmark.""")

# --- exploration track ---
q("chapels", "Chapels", deps="first_light", icon="grim_and_bleak:holy_cross", at=(8.75, 4.5), tier=3,
  tasks=[structure("grim_and_bleak:chapel", title="Find a chapel"), item("grim_and_bleak:holy_cross")],
  rewards=give("minecraft:candle", 8), desc="""
    Old &eChapels&r stand in the Hollow's forests and plains, some of them in ruins. Each one keeps a single &eHoly Cross&r, which can't be crafted. Mine it to take it with you.

    A placed Holy Cross comforts you like a church. You'll need one for the &bPale Beacon&r and one for the Cursed Amulet, so find more than one chapel.""")

q("dead_rest", "The Dead Rest Here", deps="chapels", icon="minecraft:bone_block", at=(10.5, 4.5), tier=3,
  tasks=[structure("graveyard:crypt", title="Find a crypt"), structure("graveyard:large_graveyard", title="Find a large graveyard")],
  rewards=give("minecraft:bone_block", 4), desc="""
    &eThe Graveyard&r's crypts and graveyards are scattered through the Hollow, full of ghouls, revenants and worse.

    The crypts go deep: the best chest waits at the bottom. Bring light, food and a way out.""")

q("haunts", "Catacombs and the Haunted House", deps="dead_rest", icon="minecraft:cobweb", at=(12.25, 4.5), tier=3,
  tasks=[structure("weeping_angels:catacombs", title="Find the catacombs"), structure("graveyard:haunted_house", title="Find a haunted house")],
  rewards=give("minecraft:spyglass"), desc="""
    Two more places worth the fear:

    &eThe Catacombs&r: stone halls full of statues. Some of them are Weeping Angels. Count them before you turn around.
    &eThe Haunted House&r: a lonely house that isn't as empty as it looks.""")

q("fragments", "Bone Staff Fragments", deps="haunts", icon="graveyard:middle_bone_staff", at=(14.0, 4.5), tier=3,
  tasks=[structure("graveyard:ruins", title="Find Graveyard ruins"), item("graveyard:upper_bone_staff"),
         item("graveyard:middle_bone_staff"), item("graveyard:lower_bone_staff")], desc="""
    A broken staff lies scattered across the Hollow: the &eupper&r, &emiddle&r and &elower&r fragments, one in each of three Graveyard &eruins&r.

    Together they're the key to the Corrupted Champion's ritual.""")

# --- story track: Lost Signal ---
q("page_1", "Lost Signal: Static", deps="first_light", icon="strata:pale_survey_page_1", at=(8.75, 7.5),
  tasks=item("strata:pale_survey_page_1"), desc="""
    &7Pages of an old expedition log turn up in chests in the Hollow, one page per chest, always in order. Everyone finds their own copies.&r

    &o"Pale Survey, day one. The lantern woke the frame and the portal filled with static, like a dead channel. Four of us went through: Ashe, Callow, Vale and I. It is always night here, our compasses spin, and Callow says the fog swallows her lines after ten paces. We camp by the portal and keep the lanterns burning. Marrow, surveyor."&r""")

q("page_2", "Lost Signal: Footsteps", deps="page_1", icon="strata:pale_survey_page_2", at=(10.5, 7.5),
  tasks=item("strata:pale_survey_page_2"), desc="""
    &o"Day three. Vale hears footsteps behind her that stop when she turns. I hear them too. The longer we stay out, the more the shapes at the edge of the light stop being shapes and start walking. Firelight helps, and so does staying close together. Vale wove us garlands; we wear them and don't talk about why."&r""")

q("page_3", "Lost Signal: The Listener", deps="page_2", icon="strata:pale_survey_page_3", at=(12.25, 7.5),
  tasks=item("strata:pale_survey_page_3"), desc="""
    &o"Day six. Ashe built a hut of planks and the forest answered. Something screamed far off, then closer, then it came through the walls like they were bread. It hears hammers, doors, the lids of chests. We lost the hut and half the supplies. Ashe says obsidian might be too hard for it to chew. We build quietly now."&r""")

q("page_4", "Lost Signal: Statues", deps="page_3", icon="strata:pale_survey_page_4", at=(14.0, 7.5),
  tasks=item("strata:pale_survey_page_4"), desc="""
    &o"Day nine. There are statues in the catacombs that were not there yesterday. Callow mapped them, looked down to mark the page, and when she looked up one stood right beside her. Then she was gone. We found her compass on the floor, still spinning. They do not move while you watch them. Never stop watching."&r""")

q("page_5", "Lost Signal: Embers", deps="page_4", icon="strata:pale_survey_page_5", at=(15.75, 7.5),
  tasks=item("strata:pale_survey_page_5"), desc="""
    &o"Day twelve. The embers the dead things leave behind burn without wood, a cold pale light, and nothing came near it all night. Inside that light I slept for the first time since we came through. If we could make the light last, set it in something and feed it, we could hold ground here. A sanctuary. Ashe has gone to find the parts."&r""")

q("page_6", "Lost Signal: The Last Entry", deps="page_5", icon="strata:pale_survey_page_6", at=(17.5, 7.5), tier=2,
  tasks=item("strata:pale_survey_page_6"), desc="""
    &o"Last entry. If anyone reads this, here is the plan: the cross from a chapel to keep it holy, the staff of the thing in the sky prison, the artifact the templar carries, our lantern at its heart, and embers at its corners and along its base. Feed it an ember every day or it goes dark. Ashe never came back with the staff, and we hear the screaming again. If the light is burning when you find this, we made it."&r

    &7The rest of the page is blank.&r""")

# --- boss ladder ---
q("templar", "The Damned Templar", deps=["darksteel", "chapels"], icon="grim_and_bleak:templar_artifact", at=(12.25, -1.5), tier=4,
  tasks=[item("grim_and_bleak:cursed_amulet"), kill("grim_and_bleak:damned_templar"), item("grim_and_bleak:templar_artifact")], desc="""
    The &cDamned Templar&r is a fallen knight. Call it with a &eCursed Amulet&r (darksteel, a &eBanshee Collar&r and a &eHoly Cross&r; press &eR&r on it), or meet one in the &bgrimstone mountains&r.

    &6Drops:&r the &eTemplar Artifact&r (the Thunder Sword and the Pale Beacon each need one, so expect to fight it more than once), unbreakable templar armor or its claymore.""")

q("mutants", "Mutants", deps="templar", icon="mutantmonsters:hulk_hammer", at=(14.0, -1.5), tier=4,
  tasks=kill_tag("strata:hollow_mutants", 2, title="Kill two of the four mutants"), desc="""
    Four huge &cmutants&r roam the Hollow: the Mutant &cZombie&r, &cSkeleton&r, &cCreeper&r and &cEnderman&r. They're big and their attacks are easy to read, but they hit hard and take a lot of killing. Beat any two.

    &6Drops:&r the &eHulk Hammer&r, mutant skeleton armor, &eCreeper Shards&r and Endersoul Fragments (toss an Ender Eye near them for the &eEndersoul Hand&r). Mutants often drop &5Hollow Embers&r too.""")

q("champion", "The Corrupted Champion", deps=["mutants", "fragments"], icon="graveyard:vial_of_blood", at=(15.75, -1.5), tier=4,
  tasks=[item("graveyard:vial_of_blood"), structure("graveyard:lich_prison", title="Find the lich prison"), kill("graveyard:lich")], desc="""
    The &cCorrupted Champion&r sleeps in a prison high in the sky. To wake it:

    1. Fill a &eVial of Blood&r from the Hollow's corrupted villagers, pillagers and acolytes.
    2. Lay the three &ebone staff fragments&r on the altar in the &blich prison&r.
    3. Pour the blood on the altar at night. Here, it's always night.

    It has two phases, heals itself and calls up to 30 undead. Bring friends. &6Drops:&r a &ebone staff&r in one of five colours, which also binds a Ghouling companion.""")

q("gate_guardian", "The Gate Guardian", deps="champion", icon="grim_and_bleak:thunder_sword", at=(17.5, -1.5), tier=5,
  shape="hexagon", size=1.5,
  tasks=[item("grim_and_bleak:gate_key"), item("grim_and_bleak:thunder_sword"),
         structure("grim_and_bleak:dimensional_gate", title="Find the Dimensional Gate"), kill("grim_and_bleak:gate_guardian")], desc="""
    The &cGate Guardian&r is the Hollow's final boss. It stands dormant at the &bDimensional Gate&r until a &eGate Key&r (darksteel and suffering flesh) wakes it.

    It's heavily armored, shrugs off fire, explosions and potions, and calls copies of itself. Forge the &eThunder Sword&r first (it needs the Templar Artifact) and land the killing blow with it, or it drops nothing. When it dies, a holy smite hits everything around it: stand back.""")

q("ravenous", "The Ravenous", deps=["gate_guardian", "listening"], icon="the_ravenous:ravenous_trophy", at=(19.25, -1.5), tier=5,
  optional=True, tasks=[kill("the_ravenous:the_ravenous"), item("the_ravenous:the_ravenous_echolocation_organ")], desc="""
    &7Optional: for the brave.&r

    Stop running and hunt &cthe Ravenous&r down. It grows stronger in phases as it eats, and lays eggs that hatch Screechers. Finish it in its last phase for its &eEcholocation Organ&r.

    Bragging rights, and an upgrade for your Pale Beacon: right-click the beacon with the organ to widen its safe circle to &e48&r blocks and warn everyone inside when a horror mob comes within &e64&r.""")

# --- the big goal ---
q("beacon", "The Pale Beacon", deps=["champion", "chapels"], icon="strata:pale_beacon", at=(17.5, 4.5), tier=4,
  tasks=item("strata:pale_beacon"), desc="""
    The Survey never finished it. You can. Craft the &ePale Beacon&r:

    &5Hollow Ember&r, &eHoly Cross&r, &5Hollow Ember&r
    a &eBone Staff&r (any colour), the &ePale Lantern&r, the &eTemplar Artifact&r
    three &5Hollow Embers&r along the bottom

    That's 5 Hollow Embers. The lantern goes into it, so craft another if you ever need to relight a portal. The beacon can only be placed in the Hollow.""")

q("sanctuary", "Sanctuary", deps=["beacon", "walls"], icon="minecraft:red_bed", at=(19.25, 4.5), tier=4,
  tasks=check(), rewards=give("minecraft:soul_lantern", 4), desc="""
    Place the beacon in the Hollow. It starts &cdark&r: right-click it with a &5Hollow Ember&r to light it for one in-game day (20 minutes). It holds up to &e7&r days of Embers, and right-clicking with an empty hand shows how long it has left.

    While it's lit, within &e24&r blocks: sanity comes back, the tricks stop, no horror mobs spawn, and the Ravenous isn't sent after you and can't eat the beacon. &eBeds work&r: sleep there to set your respawn point in the Hollow.

    &cUnfed, it goes dark&r and all of that stops. The Ravenous can still eat your walls, so keep them obsidian. Light it, sleep beside it, then click the checkmark.""")

q("survey_complete", "The Survey Complete", deps=["sanctuary", "page_6", "gate_guardian"], icon="strata:pale_beacon",
  at=(21.0, 4.5), tier=5, shape="gear", size=2.0, rewards=give("minecraft:totem_of_undying"), desc="""
    The Pale Survey came to map the Hollow, and it ended with a plan nobody lived to finish. You finished it.

    Your beacon is burning, its light holds the dark back, and the Gate Guardian has fallen. Keep it fed and it will be here every time you come back.

    Show your Sanctuary to your friends, then click the checkmark. The signal is back.""")
