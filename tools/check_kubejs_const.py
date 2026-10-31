"""Find `const` declarations inside nested blocks (loops, try/catch, if/else, ...) in KubeJS scripts.

KubeJS's Rhino (2101) scopes these wrongly: a `const` inside a for/while body keeps its first value
on every iteration, one inside try/catch or a top-level `if` throws "redeclaration of var", and two
block consts with the same name in one function clash. `let` is fine everywhere; `const` is safe
only directly in a function body or at the top level of a script. (Tested Oct 26 on the server.)

Usage: python -I tools/check_kubejs_const.py [kubejs dir]   -> lists offending lines, exit 1 if any
"""
import os
import re
import sys

LOOP_OR_TRY = {"for", "while", "do", "try", "catch", "finally"}


def strip(src):
    """Blank out comments, strings and template literals (keeping newlines and length)."""
    out, i, n = [], 0, len(src)
    while i < n:
        c = src[i]
        if src.startswith("//", i):
            j = src.find("\n", i); j = n if j < 0 else j
            out.append(" " * (j - i)); i = j
        elif src.startswith("/*", i):
            j = src.find("*/", i + 2); j = n if j < 0 else j + 2
            out.append(re.sub(r"[^\n]", " ", src[i:j])); i = j
        elif c in "'\"`":
            j = i + 1
            while j < n and src[j] != c:
                j += 2 if src[j] == "\\" else 1
            out.append(c + re.sub(r"[^\n]", " ", src[i + 1:j]) + (c if j < n else "")); i = j + 1
        else:
            out.append(c); i += 1
    return "".join(out)


def block_kind(text, brace):
    """What opened the block at `brace`: a loop/try keyword, 'function', or 'other'."""
    k = brace - 1
    while k >= 0 and text[k].isspace():
        k -= 1
    if text[k - 1:k + 1] == "=>":
        return "function"
    if text[k] == ")":
        depth = 0
        while k >= 0:
            if text[k] == ")": depth += 1
            elif text[k] == "(":
                depth -= 1
                if depth == 0: break
            k -= 1
        m = re.search(r"(\w+)\s*$", text[:k])
        word = m.group(1) if m else ""
        if word in ("for", "while", "catch"): return word
        if word in ("if", "switch", "with"): return "other"
        return "function"                      # function name(...) {  or method(...) {
    m = re.search(r"(\w+)\s*$", text[:k + 1])
    word = m.group(1) if m else ""
    return word if word in LOOP_OR_TRY else "other"


def check(path):
    src = strip(open(path, encoding="utf-8").read())
    stack, bad = [], []
    for i, c in enumerate(src):
        if c == "{":
            stack.append(block_kind(src, i))
        elif c == "}":
            if stack: stack.pop()
        elif src.startswith("const", i) and (i == 0 or not (src[i - 1].isalnum() or src[i - 1] in "_$")) \
                and not (src[i + 5:i + 6].isalnum() or src[i + 5:i + 6] in "_$"):
            inner = []
            for kind in reversed(stack):
                if kind == "function": break
                inner.append(kind)
            if inner:
                bad.append(src.count("\n", 0, i) + 1)
    return bad


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "kubejs"
    found = 0
    for d, _, files in os.walk(root):
        for f in sorted(files):
            if f.endswith(".js"):
                p = os.path.join(d, f)
                lines = open(p, encoding="utf-8").read().split("\n")
                for ln in check(p):
                    found += 1
                    print(f"{p}:{ln}: {lines[ln - 1].strip()[:110]}")
    print(f"{found} const declaration(s) inside nested blocks")
    sys.exit(1 if found else 0)


if __name__ == "__main__":
    main()
