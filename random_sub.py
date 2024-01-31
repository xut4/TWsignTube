import json
import random

json_original=r"C:\Users\91032\Desktop\handlish\sign_index.json"
z_original=r"C:\Users\91032\Desktop\handlish\sub_index.json"
json_new=r"C:\Users\91032\Desktop\handlish\random_sign_index.json"
z_new=r"C:\Users\91032\Desktop\handlish\random_sub_index.json"

inf = open(json_original, 'r', encoding='UTF-8')
doc = inf.read()
inf.close()
vid_url = json.loads(doc)
vid=vid_url.copy()
for word in vid_url:
    print(vid_url[word])
    if(word.strip()==""):#found that the key is whitespace
        del vid[word]    #delete it
    else:
        arr={}
        for subid in vid[word]:
            try:
                yt,mov,type,sub=subid.split("_")
                if(yt+"_"+mov in arr):
                    if(subid not in arr[yt+"_"+mov]):
                            arr[yt+"_"+mov].append(subid)
                else:
                    arr[yt+"_"+mov]=[subid] 
            except:
                yt,date,mov,type,sub=subid.split("_")
            # yt,mov,type,sub=subid.split("_")
            # print(mov)
                if(yt+"_"+date+"_"+mov in arr):
                    if(subid not in arr[yt+"_"+date+"_"+mov]):
                        arr[yt+"_"+date+"_"+mov].append(subid)
                else:
                    arr[yt+"_"+date+"_"+mov]=[subid] 
        random.seed(0)
        x = {k:arr[k] for k in random.sample(list(arr.keys()), len(arr))}
        vid[word]=x

outf = open(json_new, 'w', encoding='UTF-8')
json.dump(vid, outf, ensure_ascii=False, indent=2)
outf.close()

inf = open(z_original, 'r', encoding='UTF-8')
doc = inf.read()
inf.close()
vid_url = json.loads(doc)
vid=vid_url.copy()
for word in vid_url:
    print(vid_url[word])
    if(word.strip()==""):#found that the key is whitespace
        del vid[word]    #delete it
    else:
        arr={}
        for subid in vid[word]:
            try:
                yt,mov,type,sub=subid.split("_")
                if(yt+"_"+mov in arr):
                    if(subid not in arr[yt+"_"+mov]):
                            arr[yt+"_"+mov].append(subid)
                else:
                    arr[yt+"_"+mov]=[subid] 
            except:
                yt,date,mov,type,sub=subid.split("_")
            # yt,mov,type,sub=subid.split("_")
            # print(mov)
                if(yt+"_"+date+"_"+mov in arr):
                    if(subid not in arr[yt+"_"+date+"_"+mov]):
                        arr[yt+"_"+date+"_"+mov].append(subid)
                else:
                    arr[yt+"_"+date+"_"+mov]=[subid] 
        random.seed(0)
        x = {k:arr[k] for k in random.sample(list(arr.keys()), len(arr))}
        vid[word]=x

outf = open(z_new, 'w', encoding='UTF-8')
json.dump(vid, outf, ensure_ascii=False, indent=2)
outf.close()