from pytube import YouTube
import json

inf = open(r"C:\Users\91032\Desktop\TWsignTube\test\links_dlvid.json", 'r', encoding='UTF-8')
doc = inf.read()
inf.close()
vid_url = json.loads(doc)
for yChannel in vid_url:
    for h in vid_url[yChannel]:
        if h["video"]==False:
            yt = YouTube(h["url"])
            print(yt.title)
            try:
                yt.streams.filter().get_highest_resolution().download(r"C:\Users\91032\Desktop\TWsignTube\test")
                h["video"]=True
                
                outf = open(r"C:\Users\91032\Desktop\TWsignTube\test\links_dlvid.json", 'w', encoding='UTF-8')
                json.dump(vid_url, outf, ensure_ascii=False, indent=2)
                outf.close()
            except:
                print("error")


