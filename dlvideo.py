# importing modules
import json

# using the srt variable with the list of dictionaries
# obtained by the .get_transcript() function
json_original=r"C:\Users\91032\Desktop\TWsignTube\test\links.json"
# json_new="C:/Users/wendy/OneDrive/Desktop/linkscc.json"

inf = open(json_original, 'r', encoding='UTF-8')
doc = inf.read()
inf.close()
vid_url = json.loads(doc)
# 想爬取的youtube
# youtuber = ['@DeafNewsTV'
# ,            '@hsiyunlin'
#             ]
videolink = {}
for yChannel in vid_url:
    container = [] # 結果整理成list
    for video in vid_url[yChannel] :
        if video["cc"]==False :
            container.append({"name":video["name"], "url":video["url"],"video":False})
    videolink[yChannel]=container
		

outf = open(r"C:\Users\91032\Desktop\TWsignTube\test\links_dlvid.json", 'w', encoding='UTF-8')
json.dump(videolink, outf, ensure_ascii=False, indent=2)
outf.close()