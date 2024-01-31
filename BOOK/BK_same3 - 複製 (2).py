import json
import re
import copy
f = open(r"C:\Users\91032\Desktop\handlish\BK\BK_NC_expand1220.json", 'r', encoding="utf-8")
doc = f.read()
f.close()
data = json.loads(doc)

name=["HB1","HB2","TP1","TP2","TP3","DSchool","iSign"]
out={}
same={}
nocilin={}
nid=0
same_index={}
word={}
data2=copy.deepcopy(data)
#要跑很久
for i in range(len(data)-1):
    print(list(data)[i])
    if data[list(data)[i]]["cilin"]!=[]:
        for j in range(i+1,len(data)):
            if data[list(data)[j]]["cilin"]!=[]:
                if set(data[list(data)[i]]["cilin"])&set(data[list(data)[j]]["cilin"])!=set():
                    # print(list(data)[j])
                    # print(set(data[list(data)[i]]["cilin"])&set(data[list(data)[j]]["cilin"]))
                    data2[list(data)[j]]["words"]=list(set(data[list(data)[i]]["words"])|set(data[list(data)[j]]["words"]))
                    data2[list(data)[i]]["words"]=list(set(data[list(data)[i]]["words"])|set(data[list(data)[j]]["words"]))
                    data2[list(data)[j]]["cilin"]=list(set(data[list(data)[i]]["cilin"])|set(data[list(data)[j]]["cilin"]))
                    data2[list(data)[i]]["cilin"]=list(set(data[list(data)[i]]["cilin"])|set(data[list(data)[j]]["cilin"]))
                    j_id=list(data)[j]
                    i_id=list(data)[i]
                    if "source" not in data2[list(data)[i]]:
                        data2[list(data)[i]]["source"]=[]
                    if "source" not in data2[list(data)[j]]:
                        data2[list(data)[j]]["source"]=[]
                    try:                    
                        if i_id.split("_",1)[0] not in name:
                            i_id="ccu"
                        else:
                            i_id=i_id.split("_",1)[0]
                    except:
                        i_id="ccu"
                    try:                    
                        if j_id.split("_",1)[0] not in name:
                            j_id="ccu"
                        else:
                            j_id=j_id.split("_",1)[0]
                    except:
                        j_id="ccu"
                    data2[list(data)[i]]["source"]=list(set([i_id])|set([j_id])|set(data2[list(data)[i]]["source"]))
                    data2[list(data)[j]]["source"]=list(set([i_id])|set([j_id])|set(data2[list(data)[j]]["source"]))


# n=0
# print(out)
# for s in data2:
#     # print(word[s])
#     out["signNC_"+str(n)]=data2[s]
#     n+=1
print(out)
# for s in nocilin:
#     out["signNC_"+str(n)]=nocilin[s]
#     n+=1

# print(out)
outf = open("C:/Users/91032/Desktop/handlish/BK/BK_same_NC1220.json", 'w', encoding='UTF-8')
print("???")
json.dump(data2, outf, ensure_ascii=False, indent=1)
print("???")
outf.close()
# outf = open("C:/Users/91032/Desktop/handlish/BK/BK_same_NC_index2.json", 'w+', encoding='UTF-8')
# json.dump(same_index, outf, ensure_ascii=False, indent=1)
# outf.close()


