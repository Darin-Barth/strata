"""Small DSL for writing the Strata quest book in Python.

A chapter file in book/ looks like:

    from dsl import *
    C = chapter("create_basics", "Create: Getting Moving", group="tech", icon="create:cogwheel",
                subtitle="Rotation, belts and your first machines")
    C.quest("intro", "What is Create?", icon="create:wrench", desc='''
        Create is all about rotation...''')
    C.quest("alloy", "Andesite Alloy", deps="intro", tasks=item("create:andesite_alloy", 16), tier=2)

IDs are stable hashes of "<chapter>/<key>", so regenerating keeps players' progress.
Quests are laid out automatically as left-to-right trees (first in-chapter dependency = parent);
pass at=(x, y) to place one by hand. Dependencies on other chapters use "chapter_key/quest_key".
"""
import hashlib
import re
import textwrap

from snbt import Double, Float, Long

DX, DY = 1.75, 1.5


def make_id(*parts):
    h = hashlib.sha1("/".join(parts).encode()).hexdigest()[:16].upper()
    return "%X" % (int(h[0], 16) & 0x7) + h[1:]  # keep it a positive signed long


# A source line that starts a list item keeps its own line: "- x", "1. x", "&eLabel&r: x", "&eLabel:&r x".
LIST_ITEM_RE = re.compile(r"^([-*•] |\d+[.)] |&[0-9a-fk-or][^&]{1,40}(:&r|&r:))")


def text_lines(s):
    """Dedent and reflow: FTB Quests wraps text itself, so wrapped source lines are joined into one
    line per paragraph. Blank lines separate paragraphs; list items stay on their own lines."""
    if s is None:
        return []
    out = []
    for ln in textwrap.dedent(s).strip("\n").split("\n"):
        ln = ln.strip()
        if ln and out and out[-1] and not LIST_ITEM_RE.match(ln):
            out[-1] += " " + ln
        else:
            out.append(ln)
    return out


# ---- tasks -------------------------------------------------------------------------------
class Task:
    def __init__(self, type_, data, title=None, ids=()):
        self.type, self.data, self.title, self.ids = type_, data, title, ids


def item(iid, count=1, consume=False, title=None):
    d = {"item": {"count": 1, "id": iid}}
    if count > 1:
        d["count"] = Long(count)
    if consume:
        d["consume_items"] = True
    return Task("item", d, title, [("items", iid)])


def check(title=None):
    return Task("checkmark", {}, title)


def dim(dimension, title=None):
    return Task("dimension", {"dimension": dimension}, title, [("dimensions", dimension)])


def kill(entity, count=1, title=None):
    return Task("kill", {"entity": entity, "value": Long(count)}, title, [("entities", entity)])


def structure(sid, title=None):
    return Task("structure", {"structure": sid}, title, [("structures", sid)])


def biome(bid, title=None):
    return Task("biome", {"biome": bid}, title, [("biomes", bid)])


def adv(advancement, criterion="", title=None):
    return Task("advancement", {"advancement": advancement, "criterion": criterion}, title,
                [("advancements", advancement)])


def observe(entity, title=None, ticks=20):
    """Look at a living entity of this type for `ticks` (1 s by default)."""
    return Task("observation", {"observation_type": "entity_type", "observe_type": 5,
                                "timer": Long(ticks), "to_observe": entity}, title, [("entities", entity)])


# ---- rewards -----------------------------------------------------------------------------
class Reward:
    def __init__(self, type_, data, ids=()):
        self.type, self.data, self.ids = type_, data, ids


def xp(n):
    return Reward("xp", {"xp": n})


def levels(n):
    return Reward("xp_levels", {"xp_levels": n})


def give(iid, count=1):
    d = {"item": {"count": 1, "id": iid}}
    if count > 1:
        d["count"] = count
    return Reward("item", d, [("items", iid)])


# Quest loot bags (tools/build_quest_bags.py): opening one rolls a rarity, then an item from its pool.
BAGS = {"common": "strata:loot_bag_small", "uncommon": "strata:loot_bag",
        "rare": "strata:loot_bag_large", "epic": "strata:loot_bag_grand"}


def bag(size):
    """A quest loot bag; bigger bags have better rarity odds."""
    return give(BAGS[size])


# Default rewards by quest tier (generous by design); explicit rewards= are added on top.
TIER_REWARDS = {
    0: [],
    1: [xp(100)],
    2: [xp(250), bag("common")],
    3: [xp(500), bag("uncommon")],
    4: [levels(10), bag("rare")],
    5: [levels(20), bag("epic")],
}


# ---- quests and chapters -----------------------------------------------------------------
class Quest:
    def __init__(self, chapter, key, title, tasks, rewards, deps, desc, subtitle, icon, at, shape,
                 size, optional, any_dep, tier, hide_lines):
        self.chapter, self.key, self.title = chapter, key, title
        self.id = make_id(chapter.key, key)
        tasks = tasks if isinstance(tasks, list) else ([tasks] if tasks else [check()])
        self.tasks = tasks
        rewards = rewards if isinstance(rewards, list) else ([rewards] if rewards else [])
        self.rewards = TIER_REWARDS[tier] + rewards
        self.deps = [deps] if isinstance(deps, str) else list(deps or [])
        self.desc, self.subtitle, self.icon, self.at = text_lines(desc), subtitle, icon, at
        self.shape, self.size, self.optional, self.any_dep = shape, size, optional, any_dep
        self.hide_lines = hide_lines
        self.x = self.y = 0.0


class Chapter:
    def __init__(self, key, title, group, icon, subtitle):
        self.key, self.title, self.group, self.icon = key, title, group, icon
        self.subtitle = text_lines(subtitle)
        self.id = make_id("chapter", key)
        self.quests = []

    def quest(self, key, title, tasks=None, rewards=None, deps=None, desc=None, subtitle=None,
              icon=None, at=None, shape=None, size=None, optional=False, any_dep=False, tier=1,
              hide_lines=False):
        if any(q.key == key for q in self.quests):
            raise ValueError(f"duplicate quest key {self.key}/{key}")
        q = Quest(self, key, title, tasks, rewards, deps, desc, subtitle, icon, at, shape, size,
                  optional, any_dep, tier, hide_lines)
        self.quests.append(q)
        return q

    def layout(self):
        local = {q.key: q for q in self.quests}
        children = {q.key: [] for q in self.quests}
        roots = []
        for q in self.quests:
            parent = next((d for d in q.deps if d in local), None)
            (children[parent].append(q) if parent else roots.append(q))
        slot = [0.0]

        def place(q, depth):
            q.x = depth * DX
            kids = children[q.key]
            if not kids:
                q.y = slot[0] * DY
                slot[0] += 1
            else:
                for k in kids:
                    place(k, depth + 1)
                q.y = (kids[0].y + kids[-1].y) / 2
        for r in roots:
            place(r, 0)
            slot[0] += 0.5
        for q in self.quests:
            if q.at:
                q.x, q.y = q.at


_CHAPTERS = []


def chapter(key, title, group, icon, subtitle=None):
    c = Chapter(key, title, group, icon, subtitle)
    _CHAPTERS.append(c)
    return c


def all_chapters():
    return list(_CHAPTERS)


__all__ = ["chapter", "item", "check", "dim", "kill", "structure", "biome", "adv", "observe", "xp", "levels",
           "give", "bag", "Double", "Float", "Long"]
