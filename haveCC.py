# importing modules
import json
from youtube_transcript_api import YouTubeTranscriptApi
json_original=r"C:\Users\91032\Desktop\TWsignTube\test\links.json"
# json_new="C:/Users/wendy/OneDrive/Desktop/linkscc.json"
inf = open(json_original, 'r', encoding='UTF-8')
doc = inf.read()
inf.close()
vid_url = json.loads(doc)
for yChannel in vid_url:
	for video in vid_url[yChannel]:
		haveCC=False
		try:
			print(video["name"])
			srt = YouTubeTranscriptApi.get_transcript(video["url"].strip('https://www.youtube.com/watch?v=') ,languages=['zh-TW'])
		# creating or overwriting a file "subtitles.txt" with
		# the info inside the context manager  /"+yChannel+"
			with open("C:/Users/91032/Desktop/TWsignTube/test/txt/"+video["name"]+".txt", "a+", encoding='UTF-8') as f:
				# iterating through each element of list srt
				for i in srt:
				# writing each element of srt on a new line
					f.write("{}\n".format(i))
			haveCC=True
			print(video["cc"])
			video["cc"]=True
			print(video["cc"])
		except:
			print("no Subtitles!")

outf = open(r'C:\Users\91032\Desktop\TWsignTube\test\links.json', 'w', encoding='UTF-8')
json.dump(vid_url, outf, ensure_ascii=False, indent=2)
outf.close()