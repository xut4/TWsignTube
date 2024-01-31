from pytube import YouTube
import os
import json
import numpy
import aspose.words as aw
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
# end of function lcs
def BICE(x,y):
    return lcs(x,y)*2/(len(x)+len(y))
yourPath = r"C:\Users\wendy\OneDrive\Desktop\news.json"
inf = open(yourPath, 'r', encoding='UTF-8')
doc = inf.read()
inf.close()
vid_url = json.loads(doc)
d=[3,2,4,5,6,9,10,11,12,13]
for date in d:
    out={}
    Path = r"C:\Users\wendy\OneDrive\Desktop\star\10"+"%02d"%date+"ok"
    List = os.listdir(Path)

    list=[]#影片清單
    isin=False
    for file in vid_url["@slnewsptsTaiwan"] :
        if ("202310"+"%02d"%date in file["title"])&("完整版"not in file["title"]):
            isin=True
            list.append(file)
        else:
            if isin:
                break
    rtf=0
    RTF=[]
    for file in List :#rtf清單
        if file.endswith(".rtf"):
            RTF.append(file)
            rtf+=1
    # print(len(List),rtf)
    # input()
    common=[[0 for x in range(rtf)]for y in range(len(list))] #[vid][rtf]
    print(numpy.matrix(common))
    for file in RTF :#rtf清單
        print(file[4:-4])
        x=file[4:-4]
        for l in list:	
            y=l["title"][:-18]
            bice=BICE(x,y)
            if bice>0.1:
                common[list.index(l)][RTF.index(file)]=round(bice,4)
    print(numpy.matrix(common))
    # input() 
    for i,x in enumerate(common):
        print(x)
        print(common[i][x.index(max(x))])
        # input()
        #save srt to docx
        Doc = aw.Document(Path+"\\"+List[x.index(max(x))])
        name=list[i]["title"]
        specialChars = "/\\:*?\"><|"
        for specialChar in specialChars:
            name = name.replace(specialChar, "")
        print(name) 
        Doc.save(Path+"\\"+name+".docx")
        #download video
        yt = YouTube(list[i]['link'])
        print(yt.title)
        progMP4 = yt.streams.filter(progressive=True, file_extension='mp4')
        targetMP4 = progMP4.order_by('resolution').desc().first()
        video_file = targetMP4.download(Path)#下載位置
        out["@slnewsptsTaiwan_2310"+"%02d"%date+"_"+str(i+1)]={"channel": "@slnewsptsTaiwan",
                "name": list[i]['title'],
                "url": list[i]['link'],
                "subtitles": {},
                "sign": {}
                    }
    outf = open(Path+r"\all.json", 'w+', encoding='UTF-8')
    json.dump(out, outf, ensure_ascii=False, indent=1)
    outf.close()