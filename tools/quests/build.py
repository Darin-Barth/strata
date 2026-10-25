"""Generate config/ftbquests/quests/ from the Python chapter files in tools/quests/book/.

Usage: python -I tools/quests/build.py [--no-check] [--out DIR] [--only chap1,chap2]
  --out DIR   write somewhere else (e.g. a scratch folder) instead of config/ftbquests/quests
  --only ...  build just these chapter files (dependencies on other chapters are skipped)
Then run `packwiz refresh`. Text goes to lang/en_us.snbt (the format FTB Quests 2101.1.x's own
editor saves), so in-game edits and these sources use the same keys. The generator owns the
whole quests folder: it is wiped and rewritten on every build, so make lasting edits here.
"""
import importlib
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import dsl  # noqa: E402
import snbt  # noqa: E402
from snbt import Double, Float, Long  # noqa: E402

REPO = os.path.normpath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(REPO, "config", "ftbquests", "quests")
FILE_ID = "0000000000000001"


# FTB Quests reads "&" as a colour/format code; a literal ampersand must be written "\&".
AMP_RE = re.compile(r"(?<!\\)&(?![0-9a-fk-orA-FK-OR])")


def escape_amp(text):
    return AMP_RE.sub(lambda m: "\\&", text)


def build(out=OUT, only=None):
    sys.path.insert(0, os.path.join(HERE, "book"))
    order = importlib.import_module("_order")
    tables_mod = importlib.import_module("_tables")
    missing = [n for n in order.CHAPTERS if not os.path.exists(os.path.join(HERE, "book", n + ".py"))]
    if missing:
        print(f"WARNING: {len(missing)} chapter files not written yet: {', '.join(missing)}")
    for name in order.CHAPTERS:
        if name not in missing and (only is None or name == "welcome" or name in only):
            importlib.import_module(name)
    chapters = dsl.all_chapters()

    lang = {f"file.{FILE_ID}.title": "Strata"}
    quest_ids = {(c.key, q.key): q.id for c in chapters for q in c.quests}

    # reward tables
    table_ids = {}
    tables_out = []
    for i, (key, (title, icon, entries)) in enumerate(tables_mod.TABLES.items()):
        tid = dsl.make_id("table", key)
        table_ids[key] = tid
        rewards = []
        for j, (iid, count, weight) in enumerate(entries):
            r = {"id": dsl.make_id("table", key, str(j)), "item": {"count": 1, "id": iid}}
            if count > 1:
                r["count"] = count
            if weight != 1:
                r["weight"] = Float(weight)
            rewards.append(r)
        tables_out.append((key, {"id": tid, "order_index": i, "icon": {"id": icon}, "loot_size": 1,
                                 "rewards": rewards}))
        lang[f"reward_table.{tid}.title"] = title

    # groups
    groups_out = []
    group_ids = {}
    for key, title, icon in order.GROUPS:
        gid = dsl.make_id("group", key)
        group_ids[key] = gid
        groups_out.append({"id": gid, "icon": {"id": icon}})
        lang[f"chapter_group.{gid}.title"] = title

    chapters_out = []
    order_in_group = {}
    for c in chapters:
        c.layout()
        gkey = c.group or ""
        idx = order_in_group.get(gkey, 0)
        order_in_group[gkey] = idx + 1
        quests = []
        for q in c.quests:
            deps = []
            for d in q.deps:
                ref = tuple(d.split("/", 1)) if "/" in d else (c.key, d)
                if ref not in quest_ids and only is not None and ref[0] != c.key:
                    print(f"note: skipped dependency {c.key}/{q.key} -> {d} (chapter not built)")
                    continue
                if ref not in quest_ids:
                    raise SystemExit(f"{c.key}/{q.key}: unknown dependency {d}")
                deps.append(quest_ids[ref])
            qd = {"id": q.id, "x": Double(q.x), "y": Double(q.y)}
            if deps:
                qd["dependencies"] = deps
            if q.any_dep and len(deps) > 1:
                qd["dependency_requirement"] = "one_completed"
            if q.icon:
                qd["icon"] = {"id": q.icon}
            if q.shape:
                qd["shape"] = q.shape
            if q.size:
                qd["size"] = Double(q.size)
            if q.optional:
                qd["optional"] = True
            if q.hide_lines:
                qd["hide_dependency_lines"] = True
            tasks = []
            for i, t in enumerate(q.tasks):
                tid = dsl.make_id(c.key, q.key, "task", str(i))
                tasks.append({"id": tid, "type": t.type, **t.data})
                if t.title:
                    lang[f"task.{tid}.title"] = t.title
            qd["tasks"] = tasks
            rewards = []
            for i, r in enumerate(q.rewards):
                rid = dsl.make_id(c.key, q.key, "reward", str(i))
                data = dict(r.data)
                if r.type == "random":
                    tkey = data.pop("table")
                    data["table_id"] = Long(int(table_ids[tkey], 16))
                rewards.append({"id": rid, "type": r.type, **data})
            if rewards:
                qd["rewards"] = rewards
            quests.append(qd)
            lang[f"quest.{q.id}.title"] = q.title
            if q.subtitle:
                lang[f"quest.{q.id}.quest_subtitle"] = q.subtitle
            if q.desc:
                lang[f"quest.{q.id}.quest_desc"] = q.desc
        chapters_out.append((c.key, {
            "default_hide_dependency_lines": False,
            "default_quest_shape": "",
            "filename": c.key,
            "group": group_ids[c.group] if c.group else "",
            "icon": {"id": c.icon},
            "id": c.id,
            "images": [],
            "order_index": idx,
            "quest_links": [],
            "quests": quests,
        }))
        lang[f"chapter.{c.id}.title"] = c.title
        if c.subtitle:
            lang[f"chapter.{c.id}.chapter_subtitle"] = c.subtitle

    data = {
        "default_autoclaim_rewards": "disabled",
        "default_consume_items": False,
        "default_quest_disable_jei": False,
        "default_quest_shape": "circle",
        "default_reward_team": False,
        "detection_delay": 20,
        "disable_gui": False,
        "drop_book_on_death": False,
        "drop_loot_crates": False,
        "emergency_items_cooldown": 300,
        "grid_scale": Double(0.5),
        "icon": {"id": "minecraft:compass"},
        "lock_message": "",
        "pause_game": False,
        "progression_mode": "linear",
        "show_lock_icons": True,
        "version": 13,
    }

    OUT = out
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    for sub in ("chapters", "reward_tables", "lang"):
        os.makedirs(os.path.join(OUT, sub))
    snbt.write(os.path.join(OUT, "data.snbt"), data)
    snbt.write(os.path.join(OUT, "chapter_groups.snbt"), {"chapter_groups": groups_out})
    for key, cd in chapters_out:
        snbt.write(os.path.join(OUT, "chapters", key + ".snbt"), cd)
    for key, td in tables_out:
        snbt.write(os.path.join(OUT, "reward_tables", key + ".snbt"), td)
    lang = {k: ([escape_amp(x) for x in v] if isinstance(v, list) else escape_amp(v)) for k, v in lang.items()}
    snbt.write(os.path.join(OUT, "lang", "en_us.snbt"), lang)
    nq = sum(len(c.quests) for c in chapters)
    print(f"wrote {len(chapters)} chapters, {nq} quests, {len(tables_out)} reward tables to {OUT}")


if __name__ == "__main__":
    args = sys.argv[1:]
    out = args[args.index("--out") + 1] if "--out" in args else OUT
    only = set(args[args.index("--only") + 1].split(",")) if "--only" in args else None
    build(out, only)
    if "--no-check" not in args:
        import check_ids
        sys.exit(check_ids.main([out]))
