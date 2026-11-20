"""Build Strata Tweaks into mods/strata-tweaks-<version>.jar.

Usage: python -I tools/strata-tweaks/build.py <JDK 21 home> <NeoForge server libraries dir> <Create jar> <client libraries dir>

No Gradle: compiles the sources with javac against the jars of an installed NeoForge 21.1 server (its
`libraries/` folder; Minecraft's classes come from the Mojang-named `server-*-srg.jar`) and against Create's jar
(the diving helmets and boots extend its classes), and packs the result. The Omnistrata's wheel is client code,
so the game's client classes are needed too: the last argument is a launcher's `libraries/` folder with NeoForge
21.1 installed (Modrinth App: `%APPDATA%/ModrinthApp/meta/libraries`); its `client-*-srg.jar` and
`neoforge-*-client.jar` go on the class path after the server's jars.
"""
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent.parent


def main():
    if len(sys.argv) != 5:
        sys.exit(__doc__)
    jdk, libs = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
    version = re.search(r'^version = "([^"]+)"', (HERE / 'resources/META-INF/neoforge.mods.toml').read_text(), re.M)[1]
    jars = [p for p in libs.rglob('*.jar') if not re.search(r'server-1\.21\.1(-\d+\.\d+)?(-(slim|extra|unpacked))?\.jar$', p.name)]
    jars.append(pathlib.Path(sys.argv[3]).resolve())
    if not jars[-1].is_file():
        sys.exit('no Create jar at ' + sys.argv[3])
    client = [p for p in pathlib.Path(sys.argv[4]).rglob('*.jar')
              if re.search(r'^(client-1\.21\.1-\d+\.\d+-srg|neoforge-21\.1\.\d+-client)\.jar$', p.name)]
    if len(client) < 2:
        sys.exit('no client-*-srg.jar and neoforge-*-client.jar under ' + sys.argv[4])
    jars += client
    if not any(p.name.endswith('-srg.jar') for p in jars):
        sys.exit('no Mojang-named Minecraft jar (server-*-srg.jar) under ' + str(libs))
    sources = sorted(str(p) for p in (HERE / 'src').rglob('*.java'))
    with tempfile.TemporaryDirectory() as tmp:
        out = pathlib.Path(tmp) / 'classes'
        cp = pathlib.Path(tmp) / 'cp.txt'
        cp.write_text(';'.join(str(p) for p in jars) if sys.platform == 'win32' else ':'.join(str(p) for p in jars))
        subprocess.run([str(jdk / 'bin' / 'javac'), '--release', '21', '-proc:none', '-cp', '@' + str(cp),
                        '-d', str(out), *sources], check=True)
        shutil.copytree(HERE / 'resources', out, dirs_exist_ok=True)
        target = REPO / 'mods' / f'strata-tweaks-{version}.jar'
        for old in (REPO / 'mods').glob('strata-tweaks-*.jar'):
            old.unlink()
        subprocess.run([str(jdk / 'bin' / 'jar'), '--create', '--file', str(target), '--date', '2026-01-01T00:00:00Z',
                        '-C', str(out), '.'], check=True)
    print('wrote', target.relative_to(REPO).as_posix())


if __name__ == '__main__':
    main()
