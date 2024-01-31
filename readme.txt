有盡量照順序編號
1. Youtube_crawlURLs.py:
	爬蟲影片網址

有cc字幕(須先自行新增好放資料的資料夾)(單位是秒)
2. haveCC.py:
	若有cc字幕就下載，其他輸出json下一步下載影片
	
3. txt_to_json:
	cc下載之後是txt檔案 將他轉成json

4. endvideos:
	將cc字幕們集合成一個檔案

沒cc字幕
5. dlvideo.py:
	沒有cc字幕的，多一個key判斷下載影片了沒

6. Youtube_crawlVideos.py:
	用5的結果爬蟲下載影片(有些影片有http.client.incompleteread問題無法下載 暫時忽略)

7. NOvideo.py:
	判斷哪些沒辦法下載影片

8. vse.exe.py:(設置 繁體中文 精準模式)
	丟影片偵測字幕
	https://github.com/YaoFANGUK/video-subtitle-extractor

9. same.py:(同時轉成json)
	將字幕進行dice coeffience分析若可能為同一行字幕則合併
#之後人工修正文字內容


有cc的中文字幕
11. breakword.py
	https://github.com/ckiplab/ckiptagger/wiki/Chinese-README
	將中文字幕斷詞

手語字幕
12. find_rtf.py
	將手語新聞的文稿依照標題(srt跟yt標題)猜(用dice去猜)是哪一集的，將rtf輸出成那集名稱的docx檔案，同時整合、下載影片，之後用8偵測字幕

13. srttojson.py
	將srt檔案轉換json(時間單位是毫秒)

14. find_time.py
	將時間與文檔對齊
	將時間單位都改為秒

15. alignment.py
	將文檔中手語結構分段後對齊(手語偵測結果對齊正確句子)主要為了讓原本文檔有時間點

16. result.py
	將所有新聞結果集合成一個檔案

17. new_break2.py:
	(1)讀取"break_2.json"(所有影片資訊，包含字幕)	
	(2)刪去sign的標點符號等
	(3)藉由"BK_compound3.json"進行段詞
	(4)產生"new_break2.json"

18. new_breaktext.py:
	(1)讀取"new_break2.json"
	(2)把sign 的資料，用"/"做分隔
	(3)產生"new_break_updated.json"

19. subs_index.py
	依照相同詞語給與index，並創索引(中文手語分開)

20. random_sub.py
	將索引隨機排列

手語同意詞字典BOOK
1. 都先轉成json
2. 所有json併成一個
3. BK_same_expand.py
	找同義詞群
4. BK_same3 - 複製 (2).py
	找相互之間有相同詞群就加過去
5. BK_same_合併.py
	合併詞群完全相同的
