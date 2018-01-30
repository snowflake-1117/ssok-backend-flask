class MainPageNotice:
    def __init__(self):
        self._title = ""
        self._content = ""
        self._large_category = ""

    @property
    def title(self):
        return self._title

    @property
    def content(self):
        return self._content

    @property
    def large_category(self):
        return self._large_category

    @title.setter
    def title(self, title):
        self._title = title

    @content.setter
    def content(self, content):
        self._content = content

    @large_category.setter
    def large_category(self, large_category):
        self._large_category = large_category
