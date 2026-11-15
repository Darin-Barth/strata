"""Write Incendium's per-tick clock with its all-mob scans limited to the Nether (Darin, Nov 14).

Usage: python -I tools/build_incendium_clock.py <Incendium jar>

Incendium's `incendium:clocks/main` runs every tick and walks every mob in every dimension three times
(`@e[type=#incendium:mobs_no_player...]`) to give them Incendium IDs, run their one-time setup and tick
Incendium's own mobs. All of that only does something for Nether biomes and Incendium structures, but the scans
cost about 5% of the live server's tick time with ~1,000 Overworld mobs (spark, Nov 14). This copies the mod's
function into `kubejs/data/incendium/function/clocks/main.mcfunction` with those three lines run `in
minecraft:the_nether` (`distance=0..` keeps a selector to the dimension it runs in). Everything else, including
players, items, frozen mobs and shields, is unchanged. Re-run after an Incendium update; it stops with an error if
the lines it rewrites have changed.
"""
import pathlib
import sys
import zipfile

SRC = 'data/incendium/function/clocks/main.mcfunction'
OUT = pathlib.Path(__file__).resolve().parent.parent / 'kubejs/data/incendium/function/clocks/main.mcfunction'
REWRITES = {
    'execute as @e[type=#incendium:mobs_no_player, tag=!in.checked] at @s run function incendium:entity/mob/init':
        'execute in minecraft:the_nether as @e[type=#incendium:mobs_no_player, tag=!in.checked, distance=0..] at @s run function incendium:entity/mob/init',
    'execute as @e[type=#incendium:mobs_no_player] unless score @s in.eid matches 0..32767 run function incendium:technical/entity_id/check':
        'execute in minecraft:the_nether as @e[type=#incendium:mobs_no_player, distance=0..] unless score @s in.eid matches 0..32767 run function incendium:technical/entity_id/check',
    'execute as @e[type=#incendium:mobs_no_player, tag=in.ticking_entity] at @s run function incendium:entity/mob/main':
        'execute in minecraft:the_nether as @e[type=#incendium:mobs_no_player, tag=in.ticking_entity, distance=0..] at @s run function incendium:entity/mob/main',
}


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    text = zipfile.ZipFile(sys.argv[1]).read(SRC).decode('utf-8').replace('\r\n', '\n')
    for old, new in REWRITES.items():
        if text.count(old) != 1:
            sys.exit(f'Incendium changed: line not found once in {SRC}:\n  {old}')
        text = text.replace(old, new)
    header = ('# Strata override, written by tools/build_incendium_clock.py (re-run after an Incendium update).\n'
              '# The three all-mob scans run in the Nether only; everything else is Incendium\'s own clock.\n')
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(header + text, encoding='utf-8', newline='\n')
    print('wrote', OUT.relative_to(OUT.parents[5]).as_posix())


if __name__ == '__main__':
    main()
