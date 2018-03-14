from DBManager import DBManager
import random
import heapq

sentence_list = DBManager.select_all_titles()
random_sentence = random.choice(sentence_list)
print("> ", random_sentence)
# random_datum = DBManager.selectDatumBy(random_sentence)

n_number = 2
data_list = []


class RecommendDatum():
    def __init__(cls, sentence, similarity):
        cls.subject_line = sentence
        cls.similarity = similarity


def compare_with(object_sentence):
    object_split_list = get_spilt_list_of(object_sentence)
    for subject_index, subject_sentence in enumerate(sentence_list):
        if subject_sentence != object_sentence :
            subject_split_list = get_spilt_list_of(subject_sentence)
            count = 0
            for i in object_split_list:
                for j in subject_split_list:
                    if i == j:
                        count += 1
            datum = RecommendDatum(subject_sentence, count / len(object_split_list))
            data_list.append(datum)


def get_spilt_list_of(sentence):
    split_list = []
    sentence_length = len(sentence) - n_number + 1
    for i in range(sentence_length):
        split_part = sentence[i:i + n_number]
        split_list.append(split_part)
    return split_list


def print_all_subject_data():
    for record in data_list:
        if record.similarity >= 0.5:
            print("comparing title list: ", record.subject_line,
                  "\nsimilarity: ", record.similarity)


def get_max():
    response = heapq.nlargest(n_number, data_list, lambda item: item.similarity)
    for record in response:
        print("comparing title list: ", record.subject_line,
              "\nsimilarity: ", record.similarity)



compare_with(random_sentence)
print("ALL")
print_all_subject_data()
print("MAX")
get_max()
