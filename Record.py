class Record:
    def __init__(self):
        self._record_id = 0
        self._category = ""
        self._division = ""
        self._title = ""
        self._content = ""
        self._view = 0
        self._date = None

    @property
    def record_id(self):
        return self._record_id

    @property
    def category(self):
        return self._category

    @property
    def division(self):
        return self._division

    @property
    def title(self):
        return self._title

    @property
    def content(self):
        return self._content

    @property
    def view(self):
        return self._view

    @property
    def date(self):
        return self._date

    @record_id.setter
    def record_id(self, record_id):
        self._record_id = record_id

    @category.setter
    def category(self, category):
        self._category = category

    @division.setter
    def division(self, division):
        self._division = division

    @title.setter
    def title(self, title):
        self._title = title

    @content.setter
    def content(self, content):
        self._content = content

    @view.setter
    def view(self, view):
        self._view = view

    @date.setter
    def date(self, date):
        self._date = date
