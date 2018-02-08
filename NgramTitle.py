from NgramTitleData import NgramTitleData


class NgramTitle:
    def __init__(self, sentence_list, n_number):
        self._sentence_list = sentence_list
        self._n_number = n_number
        self._ngram_data = []

    def compare_sentence_list(self):
        for object_index, object_sentence in self._sentence_list:
            self.compare_sentence(object_index, object_sentence)
        self.print_result()

    def compare_sentence(self, object_index, object_sentence):
        object_split_list = self.get_spilt_list_of(object_sentence)
        for subject_index, subject_sentence in self._sentence_list:
            if ([object_index, subject_index]) in self._ngram_data[:][0].two_indices_set:
                break
            else:
                subject_split_list = self.get_spilt_list_of(subject_sentence)
                count = 0
                for i in object_split_list:
                    for j in subject_split_list:
                        if i == j:
                            count += 1
            ngram_data = NgramTitleData()
            ngram_data.set_of_two_titles = ([object_sentence, subject_sentence])
            ngram_data.set_of_two_indices = ([object_index, subject_index])
            ngram_data.similarity_between_two_sentences = count / len(object_split_list)
            self._ngram_data.append(ngram_data)

    def get_spilt_list_of(self, sentence):
        split_list = []
        sentence_length = len(sentence) - self._n_number + 1
        for i in range(sentence_length):
            split_part = sentence[i:i + self._n_number]
            split_list.append(split_part)
        return split_list

    def print_result(self):
        for i in self._ngram_data:
            print(i.print_all)
