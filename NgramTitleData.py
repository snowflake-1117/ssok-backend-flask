class NgramTitleData:
    def __init__(self):
        self._two_indexes_set = set([])
        self._similarity_between_two_sentences = 0.0

    @property
    def two_indexes_set(self):
        return self._two_indexes_set

    @property
    def similarity_between_two_sentences(self):
        return self._similarity_between_two_sentences

    @two_indexes_set.setter
    def two_indexes_set(self, indexes_set):
        self._two_indexes_set = indexes_set

    @similarity_between_two_sentences.setter
    def similarity_between_two_sentences(self, similarity):
        self._similarity_between_two_sentences = similarity
