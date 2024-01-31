import json
import re
import copy
f = open(r"C:\Users\91032\Desktop\handlish\BK\BK_same_NC1220.json", 'r', encoding="utf-8")
doc = f.read()
f.close()
data = json.loads(doc)

name=["HB1","HB2","TP1","TP2","TP3","DSchool","iSign"]
out={}
same={}
nocilin=[]
# nid=0
all=set()
# data2=copy.deepcopy(data)
for i in range(len(data)-1):
    # print(list(data)[i])
    if data[list(data)[i]]["cilin"]!=[]:
        if str(sorted(data[list(data)[i]]["cilin"])) not in same:
            same[str(sorted(data[list(data)[i]]["cilin"]))]=[list(data)[i]]
        else:
            same[str(sorted(data[list(data)[i]]["cilin"]))].append(list(data)[i])
    else:
        nocilin.append(list(data)[i])

# print(same)

#合併
n=0
for i in same:
    allw=[]
    alls=[]
    allc=[]
    for j in same[i]:
        print(j)
        allw=sorted(list(set(data[j]["words"])|set(allw)))
        allc=sorted(list(set(data[j]["cilin"])|set(allc)))
        if "source"not in data[j]:
            try:                    
                if j.split("_",1)[0] not in name:
                    data[j]["source"]=["ccu"]
                else:
                    data[j]["source"]=[j.split("_",1)[0]]
            except:
                data[j]["source"]=["ccu"]
        alls=sorted(list(set(data[j]["source"])|set(alls)))
    
    out["signNC_"+str(n)]={"words":allw,"cilin":allc,"source":alls}
    all=all|set(allw)-set("")
    n+=1
# print(out)

#將nocilin加入
noo=[]
for i in nocilin:
    if data[i]["words"]!=[]:
        if (set(data[i]["words"])-set(""))&all!=(set(data[i]["words"])-set("")):
            try:                    
                if i.split("_",1)[0] not in name:
                    data[i]["source"]=["ccu"]
                else:
                    data[i]["source"]=[i.split("_",1)[0]]
            except:
                data[i]["source"]=["ccu"]
            data[i]["words"]=sorted(list(set(data[i]["words"])-set("")))
            noo.append(data[i])
            all=all|(set(data[i]["words"])-set(""))
# print(out)
# print(len(noo))
no=copy.deepcopy(noo)
for i in range(len(noo)-1):
    for j in range(i,len(noo)):
        if len(noo[i]["words"])<len(noo[j]["words"]):
            # print(noo[i])
            if set(noo[i]["words"])&set(noo[j]["words"])==set(noo[i]["words"]):
                # print(noo[i]["words"])
                no.pop(no.index( noo[i]))
                break
for i in no:
    out["signNC_"+str(n)]=i
    n+=1
outf = open("C:/Users/91032/Desktop/handlish/BK/BK_same_NC_expand1220.json", 'w', encoding='UTF-8')
# print("???")
json.dump(out, outf, ensure_ascii=False, indent=1)
# print("???")
outf.close()


