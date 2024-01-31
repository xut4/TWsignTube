# importing modules
import json

# using the srt variable with the list of dictionaries
# obtained by the .get_transcript() function
json_original=r"C:\Users\91032\Desktop\TWsignTube\test\links_dlvid.json"
json_new=r"C:\Users\91032\Desktop\TWsignTube\test\NOvideo.json"

inf = open(json_original, 'r', encoding='UTF-8')
doc = inf.read()
inf.close()
vid_url = json.loads(doc)
videolink = {}
for yChannel in vid_url:
    container = [] # 結果整理成list
    for video in vid_url[yChannel] :
        if video["video"]==False :
            container.append(video)
    videolink[yChannel]=container
		

outf = open(json_new, 'w', encoding='UTF-8')
json.dump(videolink, outf, ensure_ascii=False, indent=2)
outf.close()