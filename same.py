import pysrt
import json
from datetime import datetime
import os
# Dynamic Programming implementation of LCS problem

def lcs(X, Y):
	# find the length of the strings
	m = len(X)
	n = len(Y)

	# declaring the array for storing the dp values
	L = [[None]*(n + 1) for i in range(m + 1)]

	"""Following steps build L[m + 1][n + 1] in bottom up fashion
	Note: L[i][j] contains length of LCS of X[0..i-1]
	and Y[0..j-1]"""
	for i in range(m + 1):
		for j in range(n + 1):
			if i == 0 or j == 0 :
				L[i][j] = 0
			elif X[i-1] == Y[j-1]:
				L[i][j] = L[i-1][j-1]+1
			else:
				L[i][j] = max(L[i-1][j], L[i][j-1])

	# L[m][n] contains the length of LCS of X[0..n-1] & Y[0..m-1]
	bice=L[m][n]*2/(len(X)+len(Y))
	return bice
# end of function lcs


json_original="C:/Users/wendy/OneDrive/Desktop/videos.json"#for know video's title
json_new='D:/CCs/xut/'

inf = open(json_original, 'r', encoding='UTF-8')
doc = inf.read()
inf.close()
c_url = json.loads(doc)
n=0
for video in c_url:
    subdic={}
    subcontainer = [] # 結果整理成list
    try:
        subs = pysrt.open("D:/CCs/"+video["channel"]+"/"+video["name"]+".srt")
        # print(video["name"])
        x=""
        y=""
        # i=0
        for sub in subs:
            # print(sub)
            # print(subcontainer)
            # i=i+1
            y=sub.text
            y_start=f'{sub.start.hours}:{sub.start.minutes}:{sub.start.seconds}'
            y_end=f'{sub.end.hours}:{sub.end.minutes}:{sub.end.seconds}'
            bice=lcs(x,y)
            # print (bice)  

            if(len(x)<8&len(y)<8):
                point=0.5
            else:
                point=0.6
            if(bice>point):#very close
                subcontainer[-1]["sentence"].append(y)
                # print(subcontainer)
                subcontainer[-1]["end"]=y_end
            else:
                subcontainer.append({"text":y, "start_time":y_start,"end_time":y_end,"sentence":[]})
            x=y
        ccs={"id":video,"name":video["name"], "url":video["url"],"sub":subcontainer}
        outf = open(json_new+video["channel"]+"/"+video["name"]+".json", 'w', encoding='UTF-8')
        json.dump(ccs, outf, ensure_ascii=False, indent=1)
        outf.close()        
    except Exception as inst:
        print("no srt")
        print(inst)
    n+=1

	
    