"""Minimal writer for FTB Library's SNBT style (one key per line, tabs, no commas)."""


class Long(int):
    pass


class Double(float):
    pass


class Float(float):
    pass


def _str(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def _key(k):
    # FTB quotes keys that aren't plain identifiers (lang keys contain dots, which are allowed bare)
    if all(c.isalnum() or c in "_.-+" for c in k):
        return k
    return _str(k)


def _num(v):
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, Long):
        return f"{int(v)}L"
    if isinstance(v, Double):
        return f"{float(v)}d"
    if isinstance(v, Float):
        return f"{float(v)}f"
    if isinstance(v, float):
        return f"{v}d"
    return str(v)


def _simple(v):
    return not isinstance(v, (dict, list))


def dumps(v, indent=0):
    t = "\t" * indent
    if isinstance(v, dict):
        if not v:
            return "{ }"
        # short all-scalar compounds (items, icons) stay on one line like the editor writes them
        if len(v) <= 3 and all(_simple(x) for x in v.values()):
            return "{ " + ", ".join(f"{_key(k)}: {dumps(x)}" for k, x in v.items()) + " }"
        lines = [f"{t}\t{_key(k)}: {dumps(x, indent + 1)}" for k, x in v.items()]
        return "{\n" + "\n".join(lines) + f"\n{t}}}"
    if isinstance(v, list):
        if not v:
            return "[ ]"
        if all(isinstance(x, str) for x in v) and sum(len(x) for x in v) < 60:
            return "[" + ", ".join(_str(x) for x in v) + "]"
        lines = [f"{t}\t{dumps(x, indent + 1)}" for x in v]
        return "[\n" + "\n".join(lines) + f"\n{t}]"
    if isinstance(v, str):
        return _str(v)
    return _num(v)


def write(path, data):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(dumps(data) + "\n")
