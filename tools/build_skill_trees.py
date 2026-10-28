"""Generate Strata's skill trees for Pufferfish's Skills (kubejs/data/...); design in
docs/skill-trees-rework.md.

The trees that came with the pack gave +1% to +3% per node, so nobody noticed a point. These are
fewer, bigger nodes with keystones (cost 3 points) that change how you play, and branches by
playstyle so you can't take everything. A maxed tree ends near the old total, concentrated where
you chose. This writes:
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


def tree(out, ns, cat, category, root, branches, experience):
    """root: definition id; branches: [(dx, dy, [definition ids from the root outwards])]."""
    skills = {"0_0": {"x": 0, "y": 0, "definition": root, "root": True}}
    links = []
    for dx, dy, chain in branches:
        prev = "0_0"
        for i, defn in enumerate(chain, 1):
            key = f"{dx * i}_{dy * i}"
            skills[key] = {"x": dx * i * STEP, "y": dy * i * STEP, "definition": defn}
            links.append([prev, key])
            prev = key
    base = f"{ns}/puffish_skills/categories/{cat}"
    write(out, f"{base}/category.json", category)
    write(out, f"{base}/skills.json", skills)
    write(out, f"{base}/connections.json", {"normal": {"bidirectional": links}})
    write(out, f"{base}/experience.json", experience)


# --- Combat -------------------------------------------------------------------------------------
MELEE, RANGED = "puffish_skills:player.melee_damage", "puffish_skills:player.ranged_damage"
RESIST = "puffish_skills:player.resistance"
AA = "apothic_attributes:"

COMBAT_DEFS = {
    "root": define("+2 Health", effect("health_boost"), [attr("generic.max_health", 2)]),
    "melee": define("+6% Melee Damage", effect("strength"), [attr(MELEE, 0.06, "multiply_total")]),
    "attack_speed": define("+5% Attack Speed", item("golden_sword"), [attr("generic.attack_speed", 0.05, "multiply_total")]),
    "bloodthirst": define("Bloodthirst: 5% Life Steal", item("redstone_block"), [attr(AA + "life_steal", 0.05)],
                          True, "Heal for 5% of the damage you deal."),
    "ranged": define("+6% Ranged Damage", item("arrow"), [attr(RANGED, 0.06, "multiply_total")]),
    "draw_speed": define("+10% Draw Speed", item("bow"), [attr(AA + "draw_speed", 0.10)]),
    "deadeye": define("Deadeye: +20% Arrow Speed, 3 Armor Pierce", item("spectral_arrow"),
                      [attr(AA + "arrow_velocity", 0.20), attr(AA + "armor_pierce", 3)], True,
                      "Arrows fly faster and ignore 3 points of armor."),
    "health": define("+2 Health", effect("health_boost"), [attr("generic.max_health", 2)]),
    "resistance": define("+2% Resistance", effect("resistance"), [attr(RESIST, 0.02, "multiply_total")]),
    "bulwark": define("Bulwark: 5% Dodge Chance", item("shield"), [attr(AA + "dodge_chance", 0.05)], True,
                      "5% of attacks miss you completely."),
    "crit_damage": define("+5% Crit Damage", item("iron_sword"), [attr(AA + "crit_damage", 0.05)]),
    "move_speed": define("+4% Movement Speed", effect("speed"), [attr("generic.movement_speed", 0.04, "multiply_total")]),
    "executioner": define("Executioner: +10% Crit Chance, +25% Crit Damage", item("netherite_sword"),
                          [attr(AA + "crit_chance", 0.10), attr(AA + "crit_damage", 0.25)], True),
}
COMBAT_BRANCHES = [
    (-1, 0, ["melee"] * 4 + ["attack_speed", "bloodthirst"]),        # Warrior
    (1, 0, ["ranged"] * 4 + ["draw_speed", "deadeye"]),               # Ranger
    (0, -1, ["health"] * 3 + ["resistance"] * 2 + ["bulwark"]),      # Guardian
    (0, 1, ["crit_damage"] * 3 + ["move_speed"] * 2 + ["executioner"]),  # Duelist
]
# 25 levels (the old curve's first 25); the tree costs 33 points, so you pick.
COMBAT_XP = [10, 11, 12, 14, 17, 20, 23, 26, 29, 33, 37, 40, 45, 49, 53, 58, 63, 67, 72, 77, 82, 88, 93, 99, 104]
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
    "experience": define("+10% Experience Gained", item("experience_bottle"), [attr(AA + "experience_gained", 0.10)]),
    "deep_delver": define("Deep Delver: Safer Falls, +10% Sprint Speed", item("lantern"),
                          [attr("minecraft:generic.safe_fall_distance", 4),
                           attr("puffish_attributes:sprinting_speed", 0.10, "multiply_base")], True,
                          "Fall 4 blocks further without damage."),
}
MINING_BRANCHES = [
    (-1, 0, ["speed"] * 5 + ["tunneler"]),                       # Speed
    (1, 0, ["speed"] * 2 + ["lucky_strike"] * 2),                # Prospector
    (0, -1, ["experience"] * 2 + ["deep_delver"]),               # Delver
]
MINING_XP = [250] * 10 + [500] * 10                               # 20 levels; the tree costs 22 points


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
FISHING_XP = [60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340]   # tree costs 23 points

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
        write(out, f"irons_skills/puffish_skills/categories/{cat}/experience.json", exp)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="kubejs/data")
    ap.add_argument("--irons-jar")
    a = ap.parse_args()
    bg = "textures/gui/advancements/backgrounds/"
    tree(a.out, "puffish_skills", "combat", {"unlocked_by_default": True, "title": "Combat",
         "icon": item("diamond_sword"), "background": bg + "adventure.png"}, "root", COMBAT_BRANCHES,
         {"experience_per_level": {"type": "values", "data": {"values": COMBAT_XP}}, "sources": [KILL_SOURCE]})
    write(a.out, "puffish_skills/puffish_skills/categories/combat/definitions.json", COMBAT_DEFS)
    tree(a.out, "puffish_skills", "mining", {"unlocked_by_default": True, "title": "Mining",
         "icon": item("diamond_pickaxe"), "background": bg + "stone.png"}, "root", MINING_BRANCHES,
         {"experience_per_level": {"type": "values", "data": {"values": MINING_XP}}, "sources": [mining_source()]})
    write(a.out, "puffish_skills/puffish_skills/categories/mining/definitions.json", MINING_DEFS)
    tree(a.out, "strata", "fishing", {"unlocked_by_default": True, "title": "Fishing", "icon": item("fishing_rod"),
         "background": "textures/block/dark_prismarine.png"}, "luck_root", FISHING_BRANCHES,
         {"experience_per_level": {"type": "values", "data": {"values": FISHING_XP}},
          "sources": [{"type": "puffish_skills:fish_item", "data": {"experience": "10"}}]})
    write(a.out, "strata/puffish_skills/categories/fishing/definitions.json", FISHING_DEFS)
    if a.irons_jar:
        magic(a.out, a.irons_jar)
    else:
        print("no --irons-jar: magic trees left as they are")
    print(f"Skill trees written to {a.out}")


if __name__ == "__main__":
    main()
