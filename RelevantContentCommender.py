from DBManager import DBManager


class RecommendDatum:
    def __init__(self, sentence, similarity):
        self.subject_line = sentence
        self.similarity = similarity


def compare_with(sentence, sentence_list):
    data_list = []
    object_sentence = sentence
    object_split_list = get_spilt_list_of(object_sentence)

    for subject_index, subject_sentence in enumerate(sentence_list):
        if subject_sentence != object_sentence:
            subject_split_list = get_spilt_list_of(subject_sentence)
            count = 0
            for i in object_split_list:
                for j in subject_split_list:
                    if i == j:
                        count += 1
            datum = RecommendDatum(subject_sentence, count / len(object_split_list))
            data_list.append(datum)

    sorted_list = sorted(data_list, key=lambda item: item.similarity, reverse=True)
    response = filter(sorted_list)
    response_list = DBManager.select_max_list(response)
    print("response>")
    for record in response_list[:2]:
        print(record)
    return response_list


def get_spilt_list_of(sentence):
    split_list = []
    sentence_length = len(sentence) - 2 + 1
    for i in range(sentence_length):
        split_part = sentence[i:i + 2]
        split_list.append(split_part)
    return split_list


def filter(sorted_list):
    max_data = []
    dup = False
    for datum in sorted_list:
        try:
            m = max_data.index(datum)
        except ValueError:
            if max_data.__len__() < 2:
                max_data.append(datum)
    return max_data
