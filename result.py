import json
import os
date=[2,3,4,5,6,9,10,11,12,13]
out={}
for day in date:
    subpath=open(r"C:\Users\wendy\OneDrive\Desktop\star\10"+"%02d"%day+r"ok\all2.json", 'r', encoding='UTF-8').read()
    subfile = json.loads(subpath)
    for data in subfile:
        out[data]=subfile[data]

yourPath = r"C:\Users\wendy\OneDrive\Desktop\star\result.json"
outf = open(yourPath, 'w+', encoding='UTF-8')
json.dump(out, outf, ensure_ascii=False, indent=1)
outf.close()
