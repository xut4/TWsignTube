import json
#make subtitles word index
f = open(r"C:\Users\91032\Desktop\data\ckiptagger-master\after_alignment5.json", 'r', encoding="utf-8")
soutput="C:/Users/91032/Desktop/handlish/sign_index.json"
zoutput="C:/Users/91032/Desktop/handlish/sub_index.json"
# sign_index
doc = f.read()
f.close()
srts = json.loads(doc)
out={}
for video in srts:
    for h in srts[video]["sign"]:
        for word in srts[video]["sign"][h]["breaktext"]:
            if(word.upper() in out):
                out[word.upper()].append(h)
            else:
                out[word.upper()]=[h]

outf = open(soutput, 'w', encoding='UTF-8')
json.dump(out, outf, ensure_ascii=False, indent=2)
outf.close()
out={}
for video in srts:
    for h in srts[video]["subtitles"]:
        for word in srts[video]["subtitles"][h]["breaktext"]:
            if(word.upper() in out):
                out[word.upper()].append(h)
            else:
                out[word.upper()]=[h]

outf = open(zoutput, 'w', encoding='UTF-8')
json.dump(out, outf, ensure_ascii=False, indent=2)
outf.close()

    
