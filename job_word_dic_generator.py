#!/usr/bin/python3
# -*-coding:utf-8-*-
import os, glob, json

category = "job"
root_dir = "/var/lib/mysql/data/" + category + "/"
dic_file = root_dir + "word-dic.json"

# 어구를 자르고 ID로 변환하기 ---(※1)
word_dic = {"_MAX": 0}


def text_to_ids(text):
    text = text.strip("")
    words = text.split(" ")
    result = []
    for n in words:
        n = n.strip()
        if n == "": continue
        if not n in word_dic:
            wid = word_dic[n] = word_dic["_MAX"]
            word_dic["_MAX"] += 1
            print(wid, n)
        else:
            wid = word_dic[n]
        result.append(wid)
    return result


# 파일을 읽고 고정 길이의 배열 리턴하기 ---(※2)
def file_to_ids(fname):
    with open(fname, "r", encoding="utf8") as f:
        text = f.read()
        return text_to_ids(text)


# read by line and return array ---(※2)
def line_to_ids(fname):
    with open(fname, "r", encoding="utf8") as f:
        content = f.readlines()
        lines = [line.strip(' ') for line in content]
        for line in lines:
            text_to_ids(line)


# 딕셔너리에 단어 모두 등록하기 --- (※3)
def register_dic():
    files = glob.glob(root_dir + "*.wakati", recursive=True)
    for file in files:
        line_to_ids(file)
        print(file)


# 단어 딕셔너리 만들기 --- (※5)
if os.path.exists(dic_file):
    word_dic = json.load(open(dic_file))
else:
    register_dic()
    json.dump(word_dic, open(dic_file, "w"))
