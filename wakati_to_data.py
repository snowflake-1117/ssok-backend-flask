import os, glob, json

from department_convertor import eng_to_idx

category = "snowe"
root_dir = "./data/" + category + "/"
dic_file = root_dir + "/word-dic.json"
train_data = root_dir + "/train_data.json"
test_data = root_dir + "/test_data.json"

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



def count_line_freq(text):
    cnt = [0 for n in range(word_dic["_MAX"])]
    ids = text_to_ids(text)
    for wid in ids:
        cnt[wid] += 1
    return cnt


def get_division_list():
    files = glob.glob(root_dir + "*.wakati", recursive=True)
    division_list = []
    for file in files:
        division = os.path.splitext(file)[0].split('\\')[1]
        division_list.append(division)
    return division_list


def count_freq_train(limit = 0):
    X = []
    Y = []
    files = glob.glob(root_dir + "*.wakati", recursive=True)
    for file in files:
        division = os.path.splitext(file)[0].split('\\')[1]
        if  "_gongji" not in division:
            print("division: ", division)
            division_idx = eng_to_idx[str(division)]
            file = os.path.abspath(file)
            with open(file,encoding="utf8") as f:
                content = f.readlines()
                lines = [line.strip(' ') for line in content]
                capacity = 0
                for line in lines:
                    cnt = count_line_freq(line)
                    X.append(cnt)
                    Y.append(division_idx)
                    if limit > 0:
                        if capacity > limit: break
                        capacity += 1
    print("end of train data creation")
    return X,Y


def count_freq_test(limit = 0):
    X = []
    Y = []
    category_idx = 0
    # read by lines
    file = root_dir + category +"_gongji.wakati"
    # print(file)
    with open(file, encoding="utf8") as f:
        content = f.readlines()
        lines = [line.strip(' ') for line in content]
        capacity = 0
        for line in lines:
            # print(lines.index(line),". ")
            cnt = count_line_freq(line)
            X.append(cnt)
            Y.append(category_idx)
            if limit > 0:
                if capacity > limit: break
                capacity += 1
    print("end of test data creation")
    return X,Y


if not os.path.exists(train_data):
    X, Y = count_freq_train()  # 전체는 void
    json.dump({"X": X, "Y": Y}, open(train_data, "w"))
    X, Y = count_freq_test()  # 전체는 void
    json.dump({"X": X, "Y": Y}, open(test_data, "w"))
