class RecommendCondition:
    STATUS_IN = True
    STATUS_OUT = False

    CATEGORY_NORMAL = 0
    CATEGORY_INTERESTING = 1
    CATEGORY_UNINTERESTING = 2

    INTEREST_SCHOLARSHIP = "장학"
    INTEREST_ACADEMIC = "학사"
    INTEREST_EVENT = "행사"
    INTEREST_RECRUIT = "모집"
    INTEREST_SYSTEM = "시스템"
    INTEREST_GLOBAL = "국제"
    INTEREST_CAREER = "취업"
    INTEREST_STUDENT = "학생"

    def __init__(self, student_grade=0, student_year=0,
                 major1="", major2="", school_scholar=False,
                 government_scholar=False, external_scholar=False, student_status=STATUS_IN,
                 interest_scholarship=CATEGORY_NORMAL, interest_academic=CATEGORY_NORMAL,
                 interest_event=CATEGORY_NORMAL, interest_recruit=CATEGORY_NORMAL,
                 interest_system=CATEGORY_NORMAL, interest_global=CATEGORY_NORMAL,
                 interest_career=CATEGORY_NORMAL, interest_student=CATEGORY_NORMAL):
        self._student_year = int(student_year)
        self._student_grade = int(student_grade)
        self._major1 = major1
        self._major2 = major2
        self._school_scholar = school_scholar in ['True', 'true']
        self._government_scholar = government_scholar in ['True', 'true']
        self._external_scholar = external_scholar in ['True', 'true']
        self._student_status = student_status in ['True', 'true']
        self._interest_scholarship = int(interest_scholarship)
        self._interest_academic = int(interest_academic)
        self._interest_event = int(interest_event)
        self._interest_recruit = int(interest_recruit)
        self._interest_system = int(interest_system)
        self._interest_global = int(interest_global)
        self._interest_career = int(interest_career)
        self._interest_student = int(interest_student)

    @property
    def student_year(self):
        return self._student_year

    @property
    def student_grade(self):
        return self._student_grade

    @property
    def major1(self):
        return self._major1

    @property
    def major2(self):
        return self._major2

    @property
    def school_scholar(self):
        return self._school_scholar

    @property
    def government_scholar(self):
        return self._government_scholar

    @property
    def external_scholar(self):
        return self._external_scholar

    @property
    def student_status(self):
        return self._student_status

    @property
    def interest_scholarship(self):
        return self._interest_scholarship

    @property
    def interest_academic(self):
        return self._interest_academic

    @property
    def interest_event(self):
        return self._interest_event

    @property
    def interest_recruit(self):
        return self._interest_recruit

    @property
    def interest_global(self):
        return self._interest_global

    @property
    def interest_career(self):
        return self._interest_career

    @property
    def interest_student(self):
        return self._interest_student

    @property
    def interest_system(self):
        return self._interest_system

    @student_year.setter
    def student_year(self, student_year):
        self._student_year = student_year

    @student_grade.setter
    def student_grade(self, student_grade):
        self._student_grade = student_grade

    @student_status.setter
    def student_status(self, student_status):
        self._student_status = student_status

    @major1.setter
    def major1(self, major1):
        self._major1 = major1

    @major2.setter
    def major2(self, major2):
        self._major2 = major2

    @school_scholar.setter
    def school_scholar(self, school_scholar):
        self._school_scholar = school_scholar

    @government_scholar.setter
    def government_scholar(self, government_scholar):
        self._government_scholar = government_scholar

    @external_scholar.setter
    def external_scholar(self, external_scholar):
        self._external_scholar = external_scholar

    @interest_scholarship.setter
    def interest_scholarship(self, interest_scholarship):
        self._interest_scholarship = interest_scholarship

    @interest_academic.setter
    def interest_academic(self, interest_academic):
        self._interest_academic = interest_academic

    @interest_event.setter
    def interest_event(self, interest_event):
        self._interest_event = interest_event

    @interest_recruit.setter
    def interest_recruit(self, interest_recruit):
        self._interest_recruit = interest_recruit

    @interest_global.setter
    def interest_global(self, interest_global):
        self._interest_global = interest_global

    @interest_system.setter
    def interest_system(self, interest_system):
        self._interest_system = interest_system

    @interest_student.setter
    def interest_student(self, interest_student):
        self._interest_student = interest_student

    @interest_career.setter
    def interest_career(self, interest_career):
        self._interest_career = interest_career
