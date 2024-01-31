import json
import re
f = open("C:/Users/91032/Desktop/handlish/hit_index.json", 'r', encoding="utf-8")
indexdoc=f.read()
index = json.loads(indexdoc)
f = open("C:/Users/91032/Desktop/handlish/HIT_cilin_utf8CT_zhconv.json", 'r', encoding="utf-8")
hitdoc=f.read()
hit = json.loads(hitdoc)
inp=["","NOT"]
o=["","N"]
f = open(r"C:\Users\91032\Desktop\handlish\BK\BK_compound3.json", 'r', encoding="utf-8")
doc = f.read()
f.close()
data = json.loads(doc)

for l in data["NOTcompound"]:#l is id
    cilin=[]
    may={}
    for w in data["NOTcompound"][l]:
        if w in index:
            for i in index[w]:#all cilin index
                if "#"not in i:#because which has # in id have many not same vocabulary
                    if i in may:
                        may[i]+=1
                    else:
                        may[i]=1
    print(may)
    # input()
    if len(may)>0:
        # if len(data["NOTcompound"][l])==1:
        #     for k in may:
        #         if k not in cilin:
        #             cilin.append(k) 

            # if list(may)[0] not in cilin:
            #     cilin.append(list(may)[0]) 
        if (max(may.values())>=2):
            # if((max(may.values()))==1) and (len(may)>1):
            #     max_keys = [key for key, value in may.items() if value >= 1]
            # else:
            max_keys = [key for key, value in may.items() if value >= 2]
            # print(max_keys)
            for k in max_keys:
                if k not in cilin:
                    cilin.append(k) 
    data["NOTcompound"][l]={"words":data["NOTcompound"][l],"cilin":cilin}
f = open(r"C:\Users\91032\Desktop\handlish\BK\BK_NC_expand1220.json", 'w+', encoding="utf-8")#with and without N
json.dump(data["NOTcompound"], f, ensure_ascii=False, indent=1)
f.close()
# for C in data["compound"]:
    # data={}        
        # print(l)
        # may={}
        # # maynum=0 #who is in index
        # for w in file[l]["original"]:
        #     # print(w)
        #     # input()
        #     if w in index:
        #         # maynum+=1
        #         # print(index[w])
        #         for i in index[w]:
#                     if "#"not in i:#because which has # in id have many not same vocabulary
#                         if i in may:
#                             may[i]+=1
#                         else:
#                             may[i]=1
#         if len(may)>0:
#             # print(file[l]["original"])
#             # print(may)
#             # input()
#             if (max(may.values())!=1):
#                 max_keys = [key for key, value in may.items() if value == max(may.values())]
#                 # print(max_keys)
#                 if len(max_keys)==1:
#                     # for words in hit[max_keys[0]]:
#                     if max_keys[0] not in file[l]["expand"]:
#                         file[l]["expand"].append(max_keys[0]) 
#                 else:# >1
#                     for k in max_keys:
#                         # print(k)
#                         # input()
#                         # for words in hit[k]:
#                         if k not in file[l]["expand"]:
#                             file[l]["expand"].append(k) 

#                 # input()
#             elif len(may)==1:
#                 # for words in hit[list(may)[0]]:
#                 if list(may)[0] not in file[l]["expand"]:
#                     file[l]["expand"].append(list(may)[0]) 
#     f = open(r"C:\Users\91032\Desktop\handlish\BK\BK_same_"+o[I]+"C_expand.json", 'w+', encoding="utf-8")#with and without N
#     json.dump(file, f, ensure_ascii=False, indent=1)
#     f.close()
