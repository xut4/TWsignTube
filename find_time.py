import docx
import json
import os

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
date=[2,4,5,6,9,10,11,12,13]
for day in date:
    yourPath=r"C:\Users\wendy\OneDrive\Desktop\star\10"+"%02d"%day+"ok"
    allFileList = os.listdir(yourPath)
    inf = open(yourPath+r"\all.json", 'r', encoding='UTF-8')
    doc = inf.read()
    inf.close()
    alldata = json.loads(doc)
    for file in allFileList:
        path="0"
        # print(file)
        if (file.endswith(".json"))&( "all"not in file):#有all代表是完整版(無對應檔案)
            # print(file)
            videoid=""
            for video in alldata:
                print(Bice(alldata[video]["name"][:-18],file[:-22]))
                if Bice(alldata[video]["name"][:-18],file[:-22])>0.8:
                    videoid=video
                    break
            path=yourPath+"\\"+file[:-5]+'.docx'#find correspond docx
            # print(file)

            #open json
            inf = open(yourPath+"\\"+file, 'r', encoding='UTF-8')
            doc = inf.read()
            inf.close()
            js = json.loads(doc)

            #open docx
            if(os.path.exists(path)):
                sub=[]
                d=docx.Document(path)
                print(path)
                testList = []
                for text in d.paragraphs: #read all
                    testList.append(text)
                w=0
                test=[]
                for pg in testList: #take needed from all
                    if pg.text[0:2]=="-1":#因觀察docx是-1開頭是手語台詞
                        w+=1
                        test.append(pg.text[2:])
                    elif w>0:
                        break
                print(test)
                for i in range(len(test)-1):
                    sub.append({'content':test[i]})
                index=0
                if sub==[]:#means docx has problem
                    continue
                for i in js:
                    x=i['content']
                    y=test[index]
                    bice=Bice(x,y)
                    while bice<=0.3:
                        index+=1
                        if(index>=len(test)):
                            break
                        y=test[index]
                        bice=Bice(x,y)
                    if(index>=len(test)):
                        break
                    if "start_time"in sub[index]:
                        sub[index]["end_time"]=i["end"]/1000#原本是毫秒
                    else:
                        sub[index]["start_time"]=i["start"]/1000
                        sub[index]["end_time"]=i["end"]/1000
                # print(output)
            print(sub)
            # input()
            # for o in sub:
            n=0
            for s in sub:
                # print(o,s)
                # print(sub[s])
                if "start_time"not in s:
                    n+=1
            if n!=len(sub):
                for i,s in enumerate(sub):
                    if "start_time"not in s:
                        try:
                            sub[i]["start_time"]=sub[i-1]["end_time"]
                        except:
                            sub[i]["start_time"]=0
                        try:
                            sub[i]["end_time"]=sub[i+1]["start_time"]
                        except:
                            sub[i]["end_time"]=sub[i]["start_time"]+2
                    print(videoid)
                    alldata[videoid]["subtitles"][videoid+"_z_"+str(i+1)]={"text":sub[i]["content"],
                                                                "start_time":sub[i]["start_time"],
                                                                "end_time": sub[i]["end_time"]}
    outf = open(r"C:\Users\wendy\OneDrive\Desktop\star\10"+"%02d"%day+r"ok\all.json", 'w', encoding='UTF-8')
    json.dump(alldata, outf, ensure_ascii=False, indent=1)
    outf.close()
        
                                
                            
                                
                                

                        
