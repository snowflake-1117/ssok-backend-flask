from datetime import datetime


class Record:
    def __init__(self):
        self._id = 0
        self._category = ""
        self._division = ""
        self._title = ""
        self._content = ""
        self._view = 0
        self._date = datetime.strptime("1900.01.01", "%Y.%m.%d").date()

    @property
    def id(self):
        return self._id

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

    @id.setter
    def id(self, record_id):
        self._id = record_id

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
