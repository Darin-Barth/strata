"""Upload a CurseForge modpack zip to Strata's CurseForge project (run by .github/workflows/curseforge.yml).

Uses CurseForge's upload API (https://support.curseforge.com/en/support/solutions/articles/9000197321):
looks up the game version IDs for the pack's Minecraft version and NeoForge, then posts the zip with the
GitHub release notes as its changelog. CurseForge reviews every file before it goes public.

Environment: CURSEFORGE_TOKEN (an API token from https://authors.curseforge.com/#/settings/api-tokens),
CURSEFORGE_PROJECT_ID (the number on the project's page), CHANGELOG (Markdown, optional),
RELEASE_TYPE (release, beta or alpha; default release).

Usage: python -I tools/curseforge_upload.py <zip> <display name>
"""
import json
import os
import re
import sys
import urllib.error
import urllib.request
import uuid

API = "https://minecraft.curseforge.com/api"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def call(path, token, data=None, content_type=None):
    req = urllib.request.Request(API + path, data=data, headers={"X-Api-Token": token})
    if content_type:
        req.add_header("Content-Type", content_type)
    try:
        return json.load(urllib.request.urlopen(req))
    except urllib.error.HTTPError as e:
        sys.exit(f"CurseForge {path}: HTTP {e.code} {e.read().decode(errors='replace')}")


def game_versions(token, minecraft):
    """IDs for the pack's Minecraft version and the NeoForge loader."""
    types = {t["id"]: t["slug"] for t in call("/game/version-types", token)}
    mc_type = "minecraft-" + "-".join(minecraft.split(".")[:2])          # 1.21.1 -> minecraft-1-21
    ids = []
    for v in call("/game/versions", token):
        slug = types.get(v["gameVersionTypeID"])
        if (slug == mc_type and v["name"] == minecraft) or (slug == "modloader" and v["name"] == "NeoForge"):
            ids.append(v["id"])
    if len(ids) != 2:
        sys.exit(f"Expected game version IDs for Minecraft {minecraft} and NeoForge, found {ids}")
    return ids


def main():
    zip_path, display = sys.argv[1], sys.argv[2]
    token, project = os.environ["CURSEFORGE_TOKEN"], os.environ["CURSEFORGE_PROJECT_ID"]
    pack = open(os.path.join(ROOT, "pack.toml"), encoding="utf-8").read()
    minecraft = re.search(r'^minecraft = "(.*)"', pack, re.M).group(1)
    metadata = {
        "changelog": os.environ.get("CHANGELOG") or display,
        "changelogType": "markdown",
        "displayName": display,
        "gameVersions": game_versions(token, minecraft),
        "releaseType": os.environ.get("RELEASE_TYPE") or "release",
    }
    boundary = uuid.uuid4().hex
    body = (f'--{boundary}\r\nContent-Disposition: form-data; name="metadata"\r\n\r\n{json.dumps(metadata)}\r\n'
            f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="{os.path.basename(zip_path)}"\r\n'
            f"Content-Type: application/zip\r\n\r\n").encode() + open(zip_path, "rb").read() + f"\r\n--{boundary}--\r\n".encode()
    result = call(f"/projects/{project}/upload-file", token, body, f"multipart/form-data; boundary={boundary}")
    print(f"Uploaded {os.path.basename(zip_path)} as CurseForge file {result['id']}; it goes public once CurseForge approves it.")


if __name__ == "__main__":
    main()
