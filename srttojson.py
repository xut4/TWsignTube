import re
import json
from sys import argv
import os



def parse_time(time_string):
    hours = int(re.findall(r'(\d+):\d+:\d+,\d+', time_string)[0])
    minutes = int(re.findall(r'\d+:(\d+):\d+,\d+', time_string)[0])
    seconds = int(re.findall(r'\d+:\d+:(\d+),\d+', time_string)[0])
    milliseconds = int(re.findall(r'\d+:\d+:\d+,(\d+)', time_string)[0])

    return (hours * 3600 + minutes * 60 + seconds) * 1000 + milliseconds


def parse_srt(srt_string):
    srt_list = []

    for line in srt_string.split('\n\n'):
        if line != '':
            index = int(re.match(r'\d+', line).group())

            pos = re.search(r'\d+:\d+:\d+,\d+ --> \d+:\d+:\d+,\d+',
                            line).end() + 1
            content = line[pos:]
            start_time_string = re.findall(
                r'(\d+:\d+:\d+,\d+) --> \d+:\d+:\d+,\d+', line)[0]
            end_time_string = re.findall(
                r'\d+:\d+:\d+,\d+ --> (\d+:\d+:\d+,\d+)', line)[0]
            start_time = parse_time(start_time_string)
            end_time = parse_time(end_time_string)

            srt_list.append({
                'index': index,
                'content': content,
                'start': start_time,
                'end': end_time
            })

    return srt_list


# if len(argv) == 3:
date=[2,4,5,6,9,10,11,12,13]
for day in date:
    yourPath = r"C:\Users\wendy\OneDrive\Desktop\star\10"+"%02d"%day+"ok"

    # 列出指定路徑底下所有檔案(包含資料夾)

    allFileList = os.listdir(yourPath)

    # 逐一查詢檔案清單

    for file in allFileList:
        if ".srt"in file:
            srt_filename = yourPath+"\\"+file
            out_filename = yourPath+"\\"+file[:-3]+"json"
            srt = open(srt_filename, 'r', encoding="utf-8").read()
            print(srt)
            parsed_srt = parse_srt(srt)
            outf = open(out_filename, 'w', encoding='UTF-8')
            json.dump(parsed_srt, outf, ensure_ascii=False, indent=1)
            outf.close()
        # open(out_filename, 'w', encoding="utf-8").write(
        #     json.dumps(parsed_srt, indent=2, sort_keys=True))
    # elif len(argv) == 1:
    #     print('Type \'srttojson.py filename.srt filename.json\'')
    # else:
    #     print('Wrong command.')
