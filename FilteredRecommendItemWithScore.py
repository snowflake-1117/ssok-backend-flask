class FilteredRecommendItemWithScore:
    def __init__(self, record, score=0):
        self._record = record
        self._score = score

    @property
    def record(self):
        return self._record

    @property
    def score(self):
        return self._score

    @record.setter
    def record(self, record):
        self._record = record

    @score.setter
    def score(self, score):
        self._score = score
