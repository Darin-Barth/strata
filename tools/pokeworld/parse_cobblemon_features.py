import re,json,sys
S=sys.argv[1]
cpf=open(S+'/cpf.txt').read(); cop=open(S+'/cop.txt').read(); cbt=open(S+'/cbt.txt').read()
def static_init(txt):
    return txt[txt.index('static {};'):]
# tag fields
tagf={}
last=None
for line in static_init(cbt).splitlines():
    m=re.search(r'// String (\S+)',line)
    if m: last=m.group(1)
    m=re.search(r'putstatic .*// Field (\w+):',line)
    if m and last: tagf[m.group(1)]=last; last=None
tagf={k:('cobblemon:'+v if ':' not in v else v) for k,v in tagf.items()}
vanilla={'IS_OVERWORLD':'minecraft:is_overworld','IS_NETHER':'minecraft:is_nether','IS_END':'minecraft:is_end'}
# feature fields
featf={}; last=None
for line in static_init(cpf).splitlines():
    m=re.search(r'// String (\S+)',line)
    if m: last=m.group(1)
    m=re.search(r'putstatic .*// Field (\w+):',line)
    if m and last: featf[m.group(1)]='cobblemon:'+last; last=None
reg=cpf[cpf.index('public final void register();'):cpf.index('static {};')]
out=[]; cur={}
for line in reg.splitlines():
    m=re.search(r'getstatic .*// Field (\w+):Lnet/minecraft/resources/ResourceKey',line)
    if m: cur={'feature':featf[m.group(1)]}; continue
    m=re.search(r'GenerationStep\$Decoration\.(\w+):',line)
    if m and 'feature' in cur: cur['step']=m.group(1).lower(); continue
    if 'aconst_null' in line and 'step' in cur: cur['tag']=None; continue
    m=re.search(r'getstatic .*// Field (net/minecraft/tags/BiomeTags|com/cobblemon/mod/common/api/tags/CobblemonBiomeTags)\.(\w+):',line)
    if m and 'step' in cur and m.group(2)!='INSTANCE':
        cur['tag']=vanilla[m.group(2)] if 'BiomeTags' in m.group(1) and 'Cobblemon' not in m.group(1) else tagf[m.group(2)]; continue
    m=re.search(r'CobblemonBiomeTags\.get(\w+):',line)
    if m and 'step' in cur: cur['tag']=tagf[m.group(1)]; continue
    if 'addFeatureToWorldGen' in line: out.append(cur); cur={}
# ores
last=None
for line in static_init(cop).splitlines():
    m=re.search(r'ldc.*// String ([a-z_]+)$',line)
    if m: last=m.group(1)
    m=re.search(r'CobblemonBiomeTags\.(\w+):',line)
    if m and last:
        out.append({'feature':'cobblemon:ore/'+last,'step':'underground_ores','tag':tagf[m.group(1)]}); last=None
json.dump(out,open(S+'/cobblemon_injected.json','w'),indent=1)
for o in out: print(o)
