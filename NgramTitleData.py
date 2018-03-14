class NgramTitleData:
    def __init__(self):
        self._list_of_two_titles = []
        self._list_of_two_indices = []
        self._similarity_between_two_sentences = 0.0

    @property
    def list_of_two_indices(self):
        return self._list_of_two_indices

    @property
    def similarity_between_two_sentences(self):
        return self._similarity_between_two_sentences

    @property
    def list_of_two_titles(self):
        return self._list_of_two_titles

    @list_of_two_indices.setter
    def list_of_two_indices(self, indices_list):
        self._list_of_two_indices = indices_list

    @similarity_between_two_sentences.setter
    def similarity_between_two_sentences(self, similarity):
        self._similarity_between_two_sentences = similarity

    @list_of_two_titles.setter
    def list_of_two_titles(self, title_list):
        self._list_of_two_titles = title_list

    def __str__(self):
        return self.list_of_two_titles[1] + "=>" + str(self.similarity_between_two_sentences)