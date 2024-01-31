import docx
import json
import os
import re
import numpy

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
	return L[m][n]
def Bice(X,Y):
    return lcs(X, Y)*2/(len(X)+len(Y))
# 列出指定路徑底下所有檔案(包含資料夾)

date=[2,4,5,6,9,10,11,12,13]
for day in date:
    yourPath = r"C:\Users\wendy\OneDrive\Desktop\star\10"+"%02d"%day+"ok"
    subpath=open(r"C:\Users\wendy\OneDrive\Desktop\star\10"+"%02d"%day+r"ok\all.json", 'r', encoding='UTF-8').read()
    subfile = json.loads(subpath)
    allFileList = os.listdir(yourPath)

# 逐一查詢檔案清單

    for file in allFileList:
        if ".docx"in file:#read docx for sign language structure
            docx_filename = yourPath+"\\"+file
            d=docx.Document(docx_filename)
            print(docx_filename)
            for text in d.paragraphs:
                print(text.text)
                if (text.text!=""): 
                    if(text.text[0]=="("):
                        testList=text.text
                        break
            hands = re.split('[，。、?？]', testList[1:-1])
            hands = list(filter(None, hands))
            print(hands)
            subs=[]
            print(file[:-5])
            for vid in subfile:
                if Bice(subfile[vid]["name"],file[:-5])>0.8:
                    videoid=vid
                    # print(vid)
                    for sub in subfile[vid]["subtitles"]:
                        subs.append(subfile[vid]["subtitles"][sub]["text"])
                    break
            print(subs)
            #alignment
            if len(subs)==len(hands):
                ans={}
                for i,s in enumerate(subfile[videoid]["subtitles"]):
                    ans[videoid+"_s_"+str(i+1)]={"text":hands[i],"start_time":subfile[videoid]["subtitles"][s]["start_time"],"end_time":subfile[videoid]["subtitles"][s]["end_time"]}
                
                print(ans)
            elif subs==[]:
                continue
            else:
                Matrix = [[0 for x in range(len(subs))]for y in range(len(hands))] 
                bice = [[0 for x in range(len(subs))]for y in range(len(hands))] 
                for x in range(0,len(subs)):
                    for y in range(0,len(hands)):
                        hand = ''.join(re.findall(r'[A-Za-z0-9\u4e00-\u9fa5]', hands[y])) 
                        Matrix[y][x]=lcs(subs[x],hand)
                        bice[y][x]=round(Bice(subs[x],hand), 2)#('%.2f'%)
                        # print(bice)
                # print(numpy.matrix(Matrix))
                # print(numpy.matrix(bice))
                print(len(subs),len(hands))
                Alignment = [[0 for x in range(len(subs))]for y in range(len(hands))] 
                Alignment[0][0]=1
                Alignment[len(hands)-1][len(subs)-1]=1
                s=0
                h=1
                while (h<len(hands)-1)&(s<len(subs)-1):
                    if (Matrix[h][s]==0)&(Matrix[h][s+1]==0):
                        if Matrix[h-1][s+1]>0:
                            Alignment[h-1][s+1]=1
                            h-=1
                            s+=1
                        else:
                            Alignment[h][s+1]=2
                            s+=1
                    elif Matrix[h][s]>=Matrix[h][s+1]:
                        Alignment[h][s]=1
                    else:
                        Alignment[h][s+1]=1
                        s+=1
                    h+=1
                numpyArray = numpy.array(Alignment)
                if((numpyArray[:, -2:-1]==(numpy.array([[0] for x in range(len(hands))]))).all()):
                    print("yessssssss")
                    Alignment = [[0 for x in range(len(subs))]for y in range(len(hands))] 
                    Alignment[0][0]=1
                    Alignment[len(hands)-1][len(subs)-1]=1
                    s=len(subs)-1
                    h=len(hands)-2
                    while (h>0)&(s>0):
                        if (Matrix[h][s]==0)&(Matrix[h][s-1]==0):
                            if Matrix[h+1][s-1]>0:
                                Alignment[h+1][s-1]=1
                                h+=1
                                s-=1
                            else:
                                Alignment[h][s-1]=2
                                s-=1
                        elif Matrix[h][s]>=Matrix[h][s-1]:
                            Alignment[h][s]=1
                        else:
                            Alignment[h][s-1]=1
                            s-=1
                        h-=1
                print(numpy.matrix(Alignment))
                i=0
                match=[-1 for x in range(len(hands))]
                match[0]=0
                for y in range(len(hands)):
                    for x in range(i,len(subs)):
                        if Alignment[y][x]>0:
                            match[y]=x
                            i=x
                            break
                index=[0 for x in range(len(subs))]  
                ans={}
                now=0
                for i,m in enumerate(match):
                    if m==-1:
                        match[i]=match[i-1]
                    index[match[i]]+=1
                print(match)
                # input()
                count=[0 for x in range(len(subs))]  
                for i,s in enumerate(match):
                    start=subfile[videoid]["subtitles"][videoid+"_z_"+str(s+1)]["start_time"]+(subfile[videoid]["subtitles"][videoid+"_z_"+str(s+1)]["end_time"]-subfile[videoid]["subtitles"][videoid+"_z_"+str(s+1)]["start_time"])*(count[s])/index[s]
                    count[s]+=1
                    end=subfile[videoid]["subtitles"][videoid+"_z_"+str(s+1)]["end_time"]
                    ans[videoid+"_s_"+str(i+1)]={"text":hands[i],"start_time":round(start,2),"end_time":end,"breaktext":hands[i].split("/")}

                print(match)

                print(ans)
            subfile[vid]["sign"]=ans
            print (subfile)
            outf = open(r"C:\Users\wendy\OneDrive\Desktop\star\10"+"%02d"%day+r"ok\all2.json", 'w', encoding='UTF-8')
            json.dump(subfile, outf, ensure_ascii=False, indent=1)
            outf.close()
