"""Scan a dimension's region files for Cobblemon blocks and structure starts.

Usage: python tools/pokeworld/scan_regions.py <world>/region [<world>/dimensions/pokeworld/pokeworld/region]

For every region folder prints: chunks scanned, chunks containing any block from a
namespace of interest (palette scan of every section), counts per block, and structure
starts per structure id. Only reads fully generated chunks (Status minecraft:full).
"""
import gzip
import io
import os
import struct
import sys
import zlib
from collections import Counter

WATCH = ('cobblemon:',)
STRUCT_WATCH = ('cobblemon', 'integrated_cobblemon', 'cobblestructures', 'cobblemon_simple_center',
                'cobblemonextrastructures', 'pokeworld')


def read_nbt(buf):
    def rd(fmt):
        n = struct.calcsize(fmt)
        v = struct.unpack(fmt, buf.read(n))
        return v[0] if len(v) == 1 else v

    def rstr():
        return buf.read(rd('>H')).decode('utf-8', 'replace')

    def payload(t):
        if t == 1: return rd('>b')
        if t == 2: return rd('>h')
        if t == 3: return rd('>i')
        if t == 4: return rd('>q')
        if t == 5: return rd('>f')
        if t == 6: return rd('>d')
        if t == 7: n = rd('>i'); buf.read(n); return None
        if t == 8: return rstr()
        if t == 9:
            et = rd('>b'); n = rd('>i')
            return [payload(et) for _ in range(n)]
        if t == 10:
            d = {}
            while True:
                tt = rd('>b')
                if tt == 0: return d
                k = rstr(); d[k] = payload(tt)
        if t == 11: n = rd('>i'); buf.read(4 * n); return None
        if t == 12: n = rd('>i'); buf.read(8 * n); return None
        raise ValueError(t)

    t = rd('>b'); rstr()
    return payload(t)


def scan(region_dir):
    blocks, starts = Counter(), Counter()
    chunks = hit_chunks = 0
    for fn in sorted(os.listdir(region_dir)):
        if not fn.endswith('.mca'):
            continue
        data = open(os.path.join(region_dir, fn), 'rb').read()
        if len(data) < 8192:
            continue
        for i in range(1024):
            off = int.from_bytes(data[i * 4:i * 4 + 3], 'big')
            if off == 0:
                continue
            p = off * 4096
            length = int.from_bytes(data[p:p + 4], 'big')
            comp = data[p + 4]
            raw = data[p + 5:p + 4 + length]
            raw = zlib.decompress(raw) if comp == 2 else gzip.decompress(raw) if comp == 1 else raw
            c = read_nbt(io.BytesIO(raw))
            if c.get('Status') != 'minecraft:full':
                continue
            chunks += 1
            found = False
            for s in c.get('sections', []):
                for st in (s.get('block_states') or {}).get('palette', []):
                    name = st.get('Name', '')
                    if name.startswith(WATCH):
                        blocks[name] += 1
                        found = True
            hit_chunks += found
            for sid in ((c.get('structures') or {}).get('starts') or {}):
                if sid.split(':')[0] in STRUCT_WATCH or sid.startswith('minecraft:village'):
                    starts[sid] += 1
    print(f'== {region_dir}')
    print(f'full chunks: {chunks}; chunks with cobblemon: blocks: {hit_chunks}')
    for k, v in blocks.most_common():
        print(f'  block {k}: {v} chunk-sections')
    for k, v in starts.most_common():
        print(f'  structure start {k}: {v}')


if __name__ == '__main__':
    for d in sys.argv[1:]:
        scan(d)
