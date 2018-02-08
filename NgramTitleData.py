class NgramTitleData:
    def __init__(self):
        self._two_indices_set = set([])
        self._similarity_between_two_sentences = 0.0

    @property
    def two_indices_set(self):
        return self._two_indices_set

    @property
    def similarity_between_two_sentences(self):
        return self._similarity_between_two_sentences

    @two_indices_set.setter
    def two_indices_set(self, indices_set):
        self._two_indices_set = indices_set

    @similarity_between_two_sentences.setter
    def similarity_between_two_sentences(self, similarity):
        self._similarity_between_two_sentences = similarity
