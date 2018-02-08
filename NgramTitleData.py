class NgramTitleData:
    def __init__(self):
        self._set_of_two_titles = set([])
        self._set_of_two_indices = set([])
        self._similarity_between_two_sentences = 0.0

    @property
    def set_of_two_indices(self):
        return self._set_of_two_indices

    @property
    def similarity_between_two_sentences(self):
        return self._similarity_between_two_sentences

    @property
    def set_of_two_titles(self):
        return self._set_of_two_titles

    @set_of_two_indices.setter
    def set_of_two_indices(self, indices_set):
        self._set_of_two_indices = indices_set

    @similarity_between_two_sentences.setter
    def similarity_between_two_sentences(self, similarity):
        self._similarity_between_two_sentences = similarity

    @set_of_two_titles.setter
    def set_of_two_titles(self, title_set):
        self._set_of_two_titles = title_set

    def print_all(self):
        print("index set: ", self._set_of_two_indices,
              "title set: ", self._set_of_two_titles,
              "similarity: ",self._similarity_between_two_sentences,)