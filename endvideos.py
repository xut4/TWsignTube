# importing modules
import json

json_original=r"C:\Users\91032\Desktop\TWsignTube\test\links.json"
json_new=r"C:\Users\91032\Desktop\TWsignTube\test\links_mix.json"
ccfile=r"C:\Users\91032\Desktop\TWsignTube\test\json"
#\@DeafNewsTV_json"
inf = open(json_original, 'r', encoding='UTF-8')
doc = inf.read()
inf.close()
vid_url = json.loads(doc)
# 想爬取的youtube
# youtuber = ['@DeafNewsTV'
# ,            '@hsiyunlin'
#             ]
videolink = {}
n=0
for yChannel in vid_url:
    vid=1
    for video in vid_url[yChannel] :
        id=yChannel+"_"+str(vid)
        print(id)
        vid+=1
        subs={}
        if video["cc"]==True :
            inf = open(ccfile+"/"+video["name"]+".json", 'r', encoding='UTF-8')
            doc = inf.read()
            inf.close()
            cc_url = json.loads(doc)
            ccnum=1
            for cc in cc_url:
                subid=id+"_z_"+str(ccnum) #z means 中文
                subs[subid]={"start_time":float(cc["start_time"]),"end_time":float(cc["end_time"]),"text":cc["text"],"breaktext":[]}
                ccnum+=1
        videolink[id]={"channel":yChannel,"name":video["name"],"url":video["url"],"subtitles":subs,"sign":{}}
    n+=1
		

outf = open(json_new, 'w', encoding='UTF-8')
json.dump(videolink, outf, ensure_ascii=False, indent=2)
outf.close()