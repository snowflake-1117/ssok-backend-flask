class DepartmentUrlData:
    def __init__(self):
        self._college = ""
        self._department = ""
        self._domain_name = ""
        self._home_id = ""
        self._menu_seq = 0
        self._handle = 0
        self._board_id = 0
        self._category_id = 0
        self._page = 0
        self._site_id = ""

    @property
    def college(self):
        return self._college

    @property
    def department(self):
        return self._department

    @property
    def domain_name(self):
        return self._domain_name

    @property
    def home_id(self):
        return self._home_id

    @property
    def menu_seq(self):
        return self._menu_seq

    @property
    def handle(self):
        return self._handle

    @property
    def board_id(self):
        return self._board_id

    @property
    def category_id(self):
        return self._category_id

    @property
    def page(self):
        return self._page

    @property
    def site_id(self):
        return self._site_id

    @college.setter
    def college(self, college):
        self._college = college

    @department.setter
    def department(self, department):
        self._department = department

    @domain_name.setter
    def domain_name(self, domain_name):
        self._domain_name = domain_name

    @home_id.setter
    def home_id(self, home_id):
        self._home_id = home_id

    @menu_seq.setter
    def menu_seq(self, menu_seq):
        self._menu_seq = menu_seq

    @handle.setter
    def handle(self, handle):
        self._handle = handle

    @board_id.setter
    def board_id(self, board_id):
        self._board_id = board_id

    @category_id.setter
    def category_id(self, category_id):
        self._category_id = category_id

    @page.setter
    def page(self, page):
        self._page = page

    @site_id.setter
    def site_id(self, site_id):
        self._site_id = site_id
