class RecommendHelper:
    @classmethod
    def add_date_condition_within_10days(cls, sql):
        return sql + 'DATE(date) >= DATE(subdate(now(), INTERVAL 10 DAY)) AND DATE (date) <= DATE(now())'

    @classmethod
    def add_category_condition(cls, recommend_condition, sql):
        division_list = []
        uninteresting_division_list = []
        cls.set_division_two_list_by(recommend_condition, division_list, uninteresting_division_list)
        sql = cls.filter_by_uninteresting_division(uninteresting_division_list, sql)
        sql = cls.find_by_normal_or_interesting_division(division_list, sql)
        sql = cls.find_by_major_category(recommend_condition, sql)
        return sql

    @classmethod
    def set_division_two_list_by(cls, recommend_condition, division_list, uninteresting_division_list):
        if recommend_condition.interest_scholarship is not 2:
            division_list.append(recommend_condition.INTEREST_SCHOLARSHIP)
        else:
            uninteresting_division_list.append(recommend_condition.INTEREST_SCHOLARSHIP)
        if recommend_condition.interest_student is not 2:
            division_list.append(recommend_condition.INTEREST_STUDENT)
        else:
            uninteresting_division_list.append(recommend_condition.INTEREST_STUDENT)
        if recommend_condition.interest_career is not 2:
            division_list.append(recommend_condition.INTEREST_CAREER)
        else:
            uninteresting_division_list.append(recommend_condition.INTEREST_CAREER)
        if recommend_condition.interest_system is not 2:
            division_list.append(recommend_condition.INTEREST_SYSTEM)
        else:
            uninteresting_division_list.append(recommend_condition.INTEREST_SYSTEM)
        if recommend_condition.interest_recruit is not 2:
            division_list.append(recommend_condition.INTEREST_RECRUIT)
        else:
            uninteresting_division_list.append(recommend_condition.INTEREST_RECRUIT)
        if recommend_condition.interest_academic is not 2:
            division_list.append(recommend_condition.INTEREST_ACADEMIC)
        else:
            uninteresting_division_list.append(recommend_condition.INTEREST_ACADEMIC)
        if recommend_condition.interest_global is not 2:
            division_list.append(recommend_condition.INTEREST_GLOBAL)
        else:
            uninteresting_division_list.append(recommend_condition.INTEREST_GLOBAL)
        if recommend_condition.interest_entrance is not 2:
            division_list.append(recommend_condition.INTEREST_ENTRANCE)
        else:
            uninteresting_division_list.append(recommend_condition.INTEREST_ENTRANCE)

    @classmethod
    def filter_by_uninteresting_division(cls, uninteresting_division_list, sql):
        if uninteresting_division_list.__len__() > 0:
            sql += ' AND (not division in ('
            for index, uninteresting_division in enumerate(uninteresting_division_list):
                sql += "\"" + uninteresting_division + "\""
                if index < uninteresting_division_list.__len__() - 1:
                    sql += ', '
                else:
                    sql += ')'
        return sql

    @classmethod
    def find_by_normal_or_interesting_division(cls, division_list, sql):
        sql += ' AND (division in ('
        for index, division in enumerate(division_list):
            sql += "\"" + division + "\""
            if index < division_list.__len__() - 1:
                sql += ', '
            else:
                sql += ')'
        return sql

    @classmethod
    def find_by_major_category(cls, recommend_condition, sql):
        sql += ' OR category in ('
        major_list = [recommend_condition.major1, recommend_condition.major2]
        for index, major in enumerate(major_list):
            sql += "\"" + major + "\""
            if index < major_list.__len__() - 1:
                sql += ", "
            else:
                sql += '))'
        return sql

    @classmethod
    def filter_by_student_status(cls, recommend_condition, sql):
        if recommend_condition.student_status is recommend_condition.STATUS_IN:
            sql += ' OR (title LIKE \"%재학생%\")'
        else:
            sql += ' OR (title LIKE \"%휴학%\" OR title LIKE \"%복학%\")'
        return sql

    @classmethod
    def filter_by_student_grade(cls, recommend_condition, sql):
        if recommend_condition.student_grade is 1:
            sql += ' OR (title LIKE \"%신입생%\" OR title LIKE \"%새내기%\" OR title LIKE \"%GELT%\" OR content LIKE \"% 1학년%\")'
        elif recommend_condition.student_grade is 2:
            sql += ' OR (title LIKE \"% 2학년%\" OR title LIKE \"%전과%\"  OR content LIKE \"%3학기%\" OR content LIKE \"%4학기%\" OR title LIKE \"%복수전공%\" OR title LIKE \"%부전공%\" OR title LIKE \"%교환학생%\")'
        elif recommend_condition.student_grade is 3:
            sql += ' OR (title LIKE \"%3학년%\" OR title LIKE \"%조기졸업%\" OR content LIKE \"%5학기%\" OR content LIKE \"%6학기%\" OR title LIKE \"%교환학생%\")'
        else:
            sql += ' OR (title LIKE \"%수료%\" OR title LIKE \"%졸업%\" OR title LIKE \"%학위수여%\")'
        return sql

    @classmethod
    def add_student_info_condition(cls, recommend_condition, sql):
        sql = cls.filter_by_student_status(recommend_condition, sql)
        sql = cls.filter_by_student_grade(recommend_condition, sql)
        sql += ' OR (content LIKE \"%' + str(recommend_condition.student_year) + '학번%\"))'
        return sql

    @classmethod
    def select_recommend_list_from(cls, filtered_recommend_list, recommend_condition):
        if filtered_recommend_list.__len__() < 10:
            return filtered_recommend_list
        else:
            selected_recommend_list = []
            for recommend_item in filtered_recommend_list:
                selected_recommend_list.append()
            return selected_recommend_list
