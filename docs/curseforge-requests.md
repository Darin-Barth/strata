# CurseForge requests (drafts)

Two mods in the pack that need action on CurseForge before the CurseForge zip matches the Modrinth pack. The maintainer submits these.

## 1. Drive-By-Wire with Sable: CurseForge approved-list request

Status: being submitted through the request form. It is not on the list (all six tabs checked).

Where: CurseForge's Approved Non-CurseForge Mods list,
https://docs.google.com/spreadsheets/d/176Wv-PZUo9hFxy6oC6N8tWdquBLPRtSuLbNK-r0_byM/edit
(the request form is linked from the list; if it isn't there, open a ticket at https://support.curseforge.com).
Submit while signed in to the pack's CurseForge account. CurseForge says reviews take several days and they reply with approved or declined.

Text (paste into the form's fields, or as the ticket body):

> **Mod:** Drive-By-Wire with Sable
> **Page:** https://modrinth.com/mod/drive-by-wire-sable
> **Version:** 0.3.0 for Minecraft 1.21.1, NeoForge
> **File:** https://cdn.modrinth.com/data/KsqvI0hD/versions/zdSwg9kS/drivebywire-0.3.0.jar
> **Author:** Rew1nd on Modrinth (the mod's metadata lists StratoDonut)
> **License:** MIT, as set on the Modrinth project. It's a port of Drive-By-Wire by Endalion, also MIT
> (https://modrinth.com/mod/drive-by-wire), to the Sable physics library used by Create Aeronautics.
> **Not on CurseForge:** neither the port nor the original has a CurseForge project.
> **Note:** the jar's `neoforge.mods.toml` still says `license="All Rights Reserved"`. That's the line from NeoForge's
> example template (the file still has the template's comments); the project itself is published as MIT.
> **Why:** we'd like to include it in our modpack, Strata (Minecraft 1.21.1, NeoForge), and credit the author in the
> pack description.

Risk: the "All Rights Reserved" line in the jar could get it declined. If it is, ask the author on Modrinth to fix
that line or upload the mod to CurseForge.

## 2. Serene Seasons: GitHub issue asking for the 1.21.1 builds on CurseForge

Status: on hold. The pack uses 10.1.0.3, which CurseForge has. Optional: ask on Glitchfiend's Discord (search
"curseforge" first). When 10.1.0.9 appears on CurseForge, the pack switches to it.

Where: https://github.com/Glitchfiend/SereneSeasons/issues/new/choose (signed in to GitHub; pick the feature-request
template if it asks, and put the text under its headings). Related open issue: #590 (asks for 26.1 on CurseForge, no
reply since May).

**Title:** Upload 1.21.1 NeoForge builds 10.1.0.7–10.1.0.9 to CurseForge

> **Overview**
> The newest Serene Seasons for Minecraft 1.21.1 on CurseForge is 10.1.0.3 (February 2025). Modrinth has 10.1.0.7,
> 10.1.0.8 and 10.1.0.9 (August–September 2026), including the mixin stack overflow fix (#613) and the sub-season
> colour config (#606). Could those builds, or at least 10.1.0.9, be uploaded to CurseForge as well?
>
> **Why would this feature be useful?**
> CurseForge modpacks can only use files hosted on CurseForge, and its rules don't allow bundling a version the
> author hasn't uploaded there. So a 1.21.1 pack on CurseForge is stuck on 10.1.0.3 without the crash fix, while the
> same pack on Modrinth gets 10.1.0.9. We run a 1.21.1 NeoForge pack on both sites and would like both to use the
> same, fixed version. Thanks for the mod!
