class MainPageNotice:
    def __init__(self, title="", content=""):
        self._title = title
        self._content = content

    @property
    def title(self):
        return self._title

    @property
    def content(self):
        return self._content

    @title.setter
    def title(self, title):
        self._title = title

    @content.setter
    def content(self, content):
        self._content = content
