import os, glob, json

root_dir = "./data/"
dic_file = root_dir + "/word-dic.json"
data_file = root_dir + "/data.json"

# load word_dic from word_dic
word_dic = json.load(open(dic_file))
max_words = word_dic["_MAX"]

def text_to_ids(text):
    text = text.strip()
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


# 파일 내부의 단어 세기 --- (※4)
def count_file_freq(fname):
    print("word_dic[_MAX]",word_dic["_MAX"])
    cnt = [0 for n in range(word_dic["_MAX"])]
    with open(fname,"r",encoding="utf8") as f:
        text = f.read().strip()
        ids = text_to_ids(text)
        for wid in ids:
            cnt[wid] += 1
        print(cnt)
    return cnt


# 카테고리마다 파일 읽어 들이기 --- (※5)
def count_freq(limit = 0):
    X = []
    Y = []

    category_names = ["affair", "event", "recruit", "scholorship", "student", "notice"]
    files = glob.glob(root_dir + "*.wakati", recursive=True)
    for file in files:
        category = os.path.splitext(file)[0].split('\\')[1]
        print(category)
        category_idx = category_names.index(str( category ))
        cnt = count_file_freq(file)
        X.append(cnt)
        Y.append(category_idx)
    return X,Y


# 벡터를 파일로 출력하기 --- (※6)
# 전체 데이터를 기반으로 데이터 만들기
X, Y = count_freq() # 전체는 void
json.dump({"X": X, "Y": Y}, open(data_file, "w"))
print("ok")