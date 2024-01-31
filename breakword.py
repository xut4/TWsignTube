import os
import copy
from ckiptagger import data_utils, construct_dictionary, WS, POS, NER
import json
    # Download data
# data_utils.download_data(r"C:\Users\91032\Desktop\data")

# Load model without GPU
ws = WS(r"C:\Users\91032\Desktop\data\data")#"./data")
pos = POS(r"C:\Users\91032\Desktop\data\data")#"./data")
ner = NER(r"C:\Users\91032\Desktop\data\data")#"./data")

result="C:/Users/91032/Desktop/data/ckiptagger-master/tttttttt.json"
inf = open(r"C:\Users\91032\Desktop\TWsignTube\test\links_mix.json", 'r', encoding='UTF-8')
doc = inf.read()
inf.close()
srts = json.loads(doc)
# 建立一個詞典，詞典中的每個詞都有一個對應的權重
word_to_weight = {
    "7-11": 1,
    # "\n": 1,
    "聾視聞": 1,
    "FoodPanda": 1,
    "Uber Eates": 1,
    "Uber Eats": 1,
}
recommend = {
    "-": 1,
    "聾人": 2,
    "聾": 1,
    "聽人": 1,
    "學":1
}
segment_delimiter_set = {"，",",","。",".","\n",'/',"　"," ","：","~",":","；",";","","…","？","?",'"','\"',"'","~","！","!","《","》","「","」","、","『","』",'(',")"}

# 使用 construct_dictionary 函數來將上述的詞與權重建立成詞典
coerce_dictionary = construct_dictionary(word_to_weight)
dictionary = construct_dictionary(recommend)
for video in srts:
    sentence_list = []# 結果整理成list
    for sen in srts[video]["subtitles"]:
        sentence_list.append(srts[video]["subtitles"][sen]["text"])

    word_sentence_list = ws(sentence_list,sentence_segmentation = True,
                segment_delimiter_set = segment_delimiter_set, 
                recommend_dictionary=dictionary, coerce_dictionary=coerce_dictionary)
    pos_sentence_list = pos(word_sentence_list)
    i=0
    for sen in srts[video]["subtitles"]:
        w=copy.copy(word_sentence_list[i])
        for word in w:
            if word in segment_delimiter_set:
                del word_sentence_list[i][word_sentence_list[i].index(word)]
        srts[video]["subtitles"][sen]["breaktext"]=word_sentence_list[i]
        i+=1



outf = open(result, 'w+', encoding='UTF-8')
json.dump(srts, outf, ensure_ascii=False, indent=2)
outf.close()
#     # Release model
del ws
del pos
del ner

# Show results
# def print_word_pos_sentence(word_sentence, pos_sentence):
#     assert len(word_sentence) == len(pos_sentence)
#     for word, pos in zip(word_sentence, pos_sentence):
#         print(f"{word}({pos})", end="\u3000")
#     print()
#     return

# for i, sentence in enumerate(sentence_list):
#     print()
#     print(f"'{sentence}'")
#     a=word_sentence_list[i]
    # print_word_pos_sentence(word_sentence_list[i],  pos_sentence_list[i])
    # for entity in sorted(entity_sentence_list[i]):
    #     print(entity)
# return

