"""Generate Strata's skill trees for Pufferfish's Skills (kubejs/data/...); design in
docs/skill-trees-rework.md.

The trees that came with the pack gave +1% to +3% per node, so nobody noticed a point. These have
noticeable nodes, two keystones per branch (cost 3 points) that change how you play, and branches
by playstyle. Every node can be unlocked at max level, but the XP curve makes that a long goal; the
level cap is the tree's total point cost (1.0 had no cap and kept giving points). This writes:
  * Combat and Mining (override Default Skill Trees' puffish_skills:combat / :mining, all files)
  * Fishing (our own strata:fishing)
  * Magic (overrides only definitions.json and experience.json of Iron's Spells Dynamic Skill
    Trees, so its layout stays): nodes twice as strong, the general tree has half the points
    (25, same top-end power), all four trees need a third of the XP, and keystones on the
    gateway nodes (-10% cooldowns at the end of Magic I, +10% spell power at the end of each
    school tree). Needs the add-on's jar: --irons-jar <path>.

Attributes come from Pufferfish's Attributes (puffish_skills:player.* / puffish_attributes:*),
Apothic Attributes (crit, life steal, dodge, draw speed, armor pierce, experience gained) and
vanilla. Run from the repo root (re-run after a skill-tree add-on update):
  python -I tools/build_skill_trees.py --out kubejs/data --irons-jar <irons_spells_dynamic_skilltree jar>
"""
import argparse
import json
import os
import re
import zipfile

STEP = 64


def write(out, rel, data):
    path = os.path.join(out, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def attr(attribute, value, op="addition"):
    return {"type": "puffish_skills:attribute", "data": {"attribute": attribute, "value": value, "operation": op}}


def item(i):
    return {"type": "item", "data": {"item": i}}


def effect(e):
    return {"type": "effect", "data": {"effect": e}}


def define(title, icon, rewards, keystone=False, description=None):
    d = {"title": title, "icon": icon, "rewards": rewards}
    if keystone:
        d["frame"] = {"type": "advancement", "data": {"frame": "challenge"}}
        d["cost"] = 3
        d["description"] = (description + " " if description else "") + "Keystone: costs 3 points."
    elif description:
        d["description"] = description
    return d


def curve(levels, total, first):
    """XP per level rising in a straight line from `first`, summing to about `total`."""
    step = (total - first * levels) / (levels * (levels - 1) / 2)
    return [round(first + step * i) for i in range(levels)]


def tree_cost(defs, root, branches):
    return sum(defs[d].get("cost", 1) for d in [root] + [x for _, _, chain in branches for x in chain])


def tree(out, ns, cat, category, root, branches, defs, total_xp, first_xp, sources):
    """root: definition id; branches: [(dx, dy, [definition ids from the root outwards])].
    Every node can be unlocked at max level: the level cap equals the tree's total point cost
    (Pufferfish's Skills keeps giving points past the XP list without a level_limit)."""
    skills = {"0_0": {"x": 0, "y": 0, "definition": root, "root": True}}
    links = []
    for dx, dy, chain in branches:
        prev = "0_0"
        for i, defn in enumerate(chain, 1):
            key = f"{dx * i}_{dy * i}"
            skills[key] = {"x": dx * i * STEP, "y": dy * i * STEP, "definition": defn}
            links.append([prev, key])
            prev = key
    levels = tree_cost(defs, root, branches)
    base = f"{ns}/puffish_skills/categories/{cat}"
    write(out, f"{base}/category.json", category)
    write(out, f"{base}/skills.json", skills)
    write(out, f"{base}/connections.json", {"normal": {"bidirectional": links}})
    write(out, f"{base}/definitions.json", defs)
    write(out, f"{base}/experience.json", {"level_limit": levels, "experience_per_level": {
        "type": "values", "data": {"values": curve(levels, total_xp, first_xp)}}, "sources": sources})
    return levels


# --- Combat -------------------------------------------------------------------------------------
MELEE, RANGED = "puffish_skills:player.melee_damage", "puffish_skills:player.ranged_damage"
RESIST = "puffish_skills:player.resistance"
AA = "apothic_attributes:"

# Every node can be unlocked at max level (Darin, Oct 30); 4 branches of 10 nodes with 2 keystones
# each. Small nodes are smaller than 1.0's so a full tree ends about 1.5x the old maximum.
COMBAT_DEFS = {
    "root": define("+2 Health", effect("health_boost"), [attr("generic.max_health", 2)]),
    # Warrior
    "melee": define("+4% Melee Damage", effect("strength"), [attr(MELEE, 0.04, "multiply_total")]),
    "attack_speed": define("+4% Attack Speed", item("golden_sword"), [attr("generic.attack_speed", 0.04, "multiply_total")]),
    "bloodthirst": define("Bloodthirst: 4% Life Steal", item("redstone_block"), [attr(AA + "life_steal", 0.04)],
                          True, "Heal for 4% of the damage you deal."),
    "sunder": define("Sunder: Shred 15% Armor", item("netherite_axe"), [attr(AA + "armor_shred", 0.15)],
                     True, "Your hits ignore 15% of the target's armor."),
    # Ranger
    "ranged": define("+4% Ranged Damage", item("arrow"), [attr(RANGED, 0.04, "multiply_total")]),
    "draw_speed": define("+6% Draw Speed", item("bow"), [attr(AA + "draw_speed", 0.06)]),
    "deadeye": define("Deadeye: +20% Arrow Speed, 3 Armor Pierce", item("spectral_arrow"),
                      [attr(AA + "arrow_velocity", 0.20), attr(AA + "armor_pierce", 3)], True,
                      "Arrows fly faster and ignore 3 points of armor."),
    "sharpshooter": define("Sharpshooter: +15% Ranged Damage, +15% Draw Speed", item("crossbow"),
                           [attr(RANGED, 0.15, "multiply_total"), attr(AA + "draw_speed", 0.15)], True),
    # Guardian
    "health": define("+2 Health", effect("health_boost"), [attr("generic.max_health", 2)]),
    "resistance": define("+2% Resistance", effect("resistance"), [attr(RESIST, 0.02, "multiply_total")]),
    "bulwark": define("Bulwark: 5% Dodge Chance", item("shield"), [attr(AA + "dodge_chance", 0.05)], True,
                      "5% of attacks miss you completely."),
    "unbreakable": define("Unbreakable: +4 Health, +20% Healing", item("totem_of_undying"),
                          [attr("generic.max_health", 4), attr(AA + "healing_received", 0.20)], True,
                          "Every source of healing heals you 20% more."),
    # Duelist
    "crit_damage": define("+4% Crit Damage", item("iron_sword"), [attr(AA + "crit_damage", 0.04)]),
    "move_speed": define("+3% Movement Speed", effect("speed"), [attr("generic.movement_speed", 0.03, "multiply_total")]),
    "precision": define("Precision: +6% Crit Chance", item("diamond_sword"), [attr(AA + "crit_chance", 0.06)], True),
    "executioner": define("Executioner: +8% Crit Chance, +25% Crit Damage", item("netherite_sword"),
                          [attr(AA + "crit_chance", 0.08), attr(AA + "crit_damage", 0.25)], True),
}
COMBAT_BRANCHES = [
    (-1, 0, ["melee", "melee", "attack_speed", "melee", "bloodthirst",
             "melee", "attack_speed", "melee", "attack_speed", "sunder"]),                 # Warrior
    (1, 0, ["ranged", "ranged", "draw_speed", "ranged", "deadeye",
            "ranged", "draw_speed", "ranged", "draw_speed", "sharpshooter"]),             # Ranger
    (0, -1, ["health", "health", "resistance", "health", "bulwark",
             "resistance", "health", "resistance", "resistance", "unbreakable"]),          # Guardian
    (0, 1, ["crit_damage", "crit_damage", "move_speed", "crit_damage", "precision",
            "crit_damage", "move_speed", "crit_damage", "move_speed", "executioner"]),    # Duelist
]
COMBAT_TOTAL_XP, COMBAT_FIRST_XP = 20000, 60   # 1.0's whole tree was 1,262 XP
KILL_SOURCE = {"type": "puffish_skills:kill_entity", "data": {
    "variables": {"dropped_xp": {"operations": [{"type": "get_dropped_experience"}]},
                  "max_health": {"operations": [{"type": "get_killed_living_entity"}, {"type": "get_max_health"}]}},
    "experience": "dropped_xp + max_health / 20",
    "anti_farming": {"limit_per_chunk": 15, "reset_after_seconds": 300}}}

# --- Mining -------------------------------------------------------------------------------------
MINE_SPEED, FORTUNE = "puffish_skills:player.mining_speed", "puffish_skills:player.fortune"
MINING_DEFS = {
    "root": define("+8% Mining Speed", item("iron_pickaxe"), [attr(MINE_SPEED, 0.08, "multiply_base")]),
    "speed": define("+8% Mining Speed", effect("haste"), [attr(MINE_SPEED, 0.08, "multiply_base")]),
    "tunneler": define("Tunneler: +20% Shovel and Axe Speed", item("diamond_shovel"),
                       [attr("puffish_attributes:shovel_speed", 0.20, "multiply_base"),
                        attr("puffish_attributes:axe_speed", 0.20, "multiply_base")], True),
    "lucky_strike": define("Lucky Strike: +1 Fortune", item("emerald"), [attr(FORTUNE, 1)], True,
                           "One whole level of Fortune on everything you mine."),
    "experience": define("+6% Experience Gained", item("experience_bottle"), [attr(AA + "experience_gained", 0.06)]),
    "deep_delver": define("Deep Delver: Safer Falls, +10% Sprint Speed", item("lantern"),
                          [attr("minecraft:generic.safe_fall_distance", 4),
                           attr("puffish_attributes:sprinting_speed", 0.10, "multiply_base")], True,
                          "Fall 4 blocks further without damage."),
    "speed_small": define("+5% Mining Speed", effect("haste"), [attr(MINE_SPEED, 0.05, "multiply_base")]),
    "excavator": define("Excavator: +20% Mining Speed", item("netherite_pickaxe"),
                        [attr(MINE_SPEED, 0.20, "multiply_base")], True),
    "safe_fall": define("+1 Safe Fall Distance", item("feather"), [attr("minecraft:generic.safe_fall_distance", 1)]),
    "spelunker": define("Spelunker: +15% Experience, +10% Movement Speed", item("spyglass"),
                        [attr(AA + "experience_gained", 0.15), attr("generic.movement_speed", 0.10, "multiply_total")], True,
                        "Deep caves reward the curious."),
}
MINING_BRANCHES = [
    (-1, 0, ["speed_small"] * 3 + ["speed_small", "tunneler"] + ["speed_small"] * 4 + ["excavator"]),     # Speed
    (1, 0, ["speed_small", "experience", "speed_small", "experience", "lucky_strike",
            "speed_small", "experience", "speed_small", "experience", "lucky_strike"]),               # Prospector
    (0, -1, ["experience", "safe_fall", "experience", "safe_fall", "deep_delver",
             "experience", "safe_fall", "experience", "safe_fall", "spelunker"]),                     # Delver
]
MINING_TOTAL_XP, MINING_FIRST_XP = 45000, 200   # 1.0's whole tree was 7,500 XP


def mining_source():
    def test(name, block):
        return {name: {"operations": [{"type": "get_mined_block_state"}, {"type": "puffish_skills:test", "data": {"block": block}}]}}
    v = {"silk_touch": {"operations": [{"type": "get_tool_item_stack"}, {"type": "puffish_skills:test",
                                       "data": {"nbt": "{Enchantments:[{id:\"minecraft:silk_touch\"}]}"}}]}}
    for n, b in [("stone_like", "#base_stone_overworld"), ("deepslate", "deepslate"), ("ore", "#c:ores"),
                 ("deep_ore", "#c:ores_in_ground/deepslate"), ("nether_ore", "#c:ores_in_ground/netherrack")]:
        v.update(test(n, b))
    return {"type": "puffish_skills:mine_block", "data": {"variables": v, "experience": [
        {"condition": "!silk_touch & stone_like", "expression": "1"},
        {"condition": "!silk_touch & deepslate", "expression": "2"},
        {"condition": "!silk_touch & ore & !deep_ore & !nether_ore", "expression": "10"},
        {"condition": "!silk_touch & (deep_ore | nether_ore)", "expression": "12"}]}}


# --- Fishing (ours; values doubled, Sea Legs keystone) -----------------------------------------
LUCK, BREATH, SWIM = "minecraft:generic.luck", "minecraft:generic.oxygen_bonus", "minecraft:generic.water_movement_efficiency"
FISHING_DEFS = {
    "luck_root": define("+0.5 Luck", effect("luck"), [attr(LUCK, 0.5)]),
    "luck": define("+0.5 Luck", effect("luck"), [attr(LUCK, 0.5)]),
    "luck_cap": define("Sea's Favor: +2 Luck", item("heart_of_the_sea"), [attr(LUCK, 2.0)], True),
    "breath": define("+2 Breath", effect("water_breathing"), [attr(BREATH, 2.0)]),
    "swim": define("+20% Swim Speed", effect("dolphins_grace"), [attr(SWIM, 0.2)]),
    "dig": define("+50% Underwater Mining", item("prismarine_shard"), [attr("minecraft:player.submerged_mining_speed", 0.5)]),
    "diver_cap": define("Deep Diver: +4 Breath, +20% Swim Speed", item("turtle_helmet"), [attr(BREATH, 4.0), attr(SWIM, 0.2)]),
    "sea_legs": define("Sea Legs: +20% Swim Speed, +4 Breath", item("nautilus_shell"), [attr(SWIM, 0.2), attr(BREATH, 4.0)], True,
                       "Made for the Abyssal Plain."),
    "heart": define("+2 Hearts", effect("health_boost"), [attr("minecraft:generic.max_health", 4)]),
    "stride": define("+6% Speed", effect("speed"), [attr("minecraft:generic.movement_speed", 0.06, "multiply_base")]),
    "sailor_cap": define("Old Salt: +2 Hearts, +1 Luck", item("conduit"), [attr("minecraft:generic.max_health", 4), attr(LUCK, 1.0)], True),
}
FISHING_BRANCHES = [
    (0, -1, ["luck"] * 3 + ["luck_cap"]),
    (-1, 0, ["breath", "swim", "breath", "dig", "diver_cap", "sea_legs"]),
    (1, 0, ["stride", "heart", "stride", "sailor_cap"]),
]
FISHING_TOTAL_XP, FISHING_FIRST_XP = 6000, 80   # 10 XP a catch; 1.0's 15 levels were 3,300 XP

# --- Magic (Iron's Spells Dynamic Skill Trees) ---------------------------------------------------
MAGIC_LEVELS = {"magic1": 25}                 # others keep their level count
MAGIC_KEYSTONES = {
    ("magic1", "extra_spell_power+0.03"): attr("irons_spellbooks:cooldown_reduction", 0.10),
    ("school1", "secondary_school_unlock"): attr("irons_spellbooks:spell_power", 0.10),
    ("school2", "magic2_unlock"): attr("irons_spellbooks:spell_power", 0.10),
}


def magic(out, jar):
    z = zipfile.ZipFile(jar)
    base = "data/irons_skills/puffish_skills/categories"
    for cat in ["magic1", "magic2", "school1", "school2"]:
        defs = json.loads(z.read(f"{base}/{cat}/definitions.json"))
        for key, d in defs.items():
            for r in d.get("rewards", []):
                if r["type"] == "puffish_skills:attribute":
                    r["data"]["value"] = round(r["data"]["value"] * 2, 4)
            m = re.match(r"\+([\d.]+) (.*)", d["title"])
            if m:
                v = float(m.group(1)) * 2
                name = m.group(2)
                d["title"] = f"+{v:g} {name}" if "Mana" in name and "Regen" not in name else f"+{v * 100:g}% {name}"
            extra = MAGIC_KEYSTONES.get((cat, key))
            if extra:
                d.setdefault("rewards", []).append(extra)
                bonus = "-10% Cooldowns" if "cooldown" in extra["data"]["attribute"] else "+10% Spell Power"
                d["title"] = f"{d['title']} (Keystone: {bonus})"
                d["frame"] = {"type": "advancement", "data": {"frame": "challenge"}}
        write(out, f"irons_skills/puffish_skills/categories/{cat}/definitions.json", defs)
        exp = json.loads(z.read(f"{base}/{cat}/experience.json"))
        vals = exp["experience_per_level"]["data"]["values"]
        n = MAGIC_LEVELS.get(cat, len(vals))
        total = sum(vals) / 3
        # same shape as the add-on's curve, n levels, a third of the XP
        step = len(vals) / n
        shape = [vals[min(int(i * step), len(vals) - 1)] for i in range(n)]
        exp["experience_per_level"]["data"]["values"] = [max(10, round(v * total / sum(shape))) for v in shape]
        exp["level_limit"] = n   # without it Pufferfish's Skills keeps giving points past the list
        write(out, f"irons_skills/puffish_skills/categories/{cat}/experience.json", exp)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="kubejs/data")
    ap.add_argument("--irons-jar")
    a = ap.parse_args()
    bg = "textures/gui/advancements/backgrounds/"
    n = tree(a.out, "puffish_skills", "combat", {"unlocked_by_default": True, "title": "Combat",
             "icon": item("diamond_sword"), "background": bg + "adventure.png"}, "root", COMBAT_BRANCHES,
             COMBAT_DEFS, COMBAT_TOTAL_XP, COMBAT_FIRST_XP, [KILL_SOURCE])
    print(f"Combat: {n} levels, {COMBAT_TOTAL_XP} XP")
    n = tree(a.out, "puffish_skills", "mining", {"unlocked_by_default": True, "title": "Mining",
             "icon": item("diamond_pickaxe"), "background": bg + "stone.png"}, "root", MINING_BRANCHES,
             MINING_DEFS, MINING_TOTAL_XP, MINING_FIRST_XP, [mining_source()])
    print(f"Mining: {n} levels, {MINING_TOTAL_XP} XP")
    n = tree(a.out, "strata", "fishing", {"unlocked_by_default": True, "title": "Fishing", "icon": item("fishing_rod"),
             "background": "textures/block/dark_prismarine.png"}, "luck_root", FISHING_BRANCHES,
             FISHING_DEFS, FISHING_TOTAL_XP, FISHING_FIRST_XP,
             [{"type": "puffish_skills:fish_item", "data": {"experience": "10"}}])
    print(f"Fishing: {n} levels, {FISHING_TOTAL_XP} XP")
    if a.irons_jar:
        magic(a.out, a.irons_jar)
    else:
        print("no --irons-jar: magic trees left as they are")
    print(f"Skill trees written to {a.out}")


if __name__ == "__main__":
    main()
