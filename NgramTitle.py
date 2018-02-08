# -*- coding:utf-8 -*-]

from NgramTitleData import NgramTitleData


class NgramTitle:
    def __init__(self, sentence_list, n_number):
        self._sentence_list = sentence_list
        self._n_number = n_number
        self._ngram_data = []
        self._indices_list = []

    def compare_sentence_list(self):
        for object_index, object_sentence in enumerate(self._sentence_list):
            self.compare_sentence(object_index, object_sentence)

    def compare_sentence(self, object_index, object_sentence):
        object_split_list = self.get_spilt_list_of(object_sentence)
        for subject_index, subject_sentence in enumerate(self._sentence_list):
            if subject_index > object_index:
                subject_split_list = self.get_spilt_list_of(subject_sentence)
                count = 0
                for i in object_split_list:
                    for j in subject_split_list:
                        if i == j:
                            count += 1
                ngram_data = NgramTitleData()
                ngram_data.list_of_two_titles = [object_sentence, subject_sentence]
                ngram_data.list_of_two_indices = [object_index, subject_index]
                ngram_data.similarity_between_two_sentences = count / len(object_split_list)
                self._ngram_data.append(ngram_data)
                self._indices_list.append([object_index, subject_index])

    def get_spilt_list_of(self, sentence):
        split_list = []
        sentence_length = len(sentence) - self._n_number + 1
        for i in range(sentence_length):
            split_part = sentence[i:i + self._n_number]
            split_list.append(split_part)
        return split_list

    def print_result_upper_50_percent_similarity(self):
        for i in self._ngram_data:
            if i.similarity_between_two_sentences >= 0.5:
                print("comparing index list: ", i.list_of_two_indices,
                      "\ncomparing title list: ", i.list_of_two_titles,
                      "\nsimilarity: ", i.similarity_between_two_sentences)
