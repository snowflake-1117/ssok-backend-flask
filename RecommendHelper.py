from FilteredRecommendItemWithScore import FilteredRecommendItemWithScore
from datetime import datetime


class RecommendHelper:
    selected_recommend_list = []

    @classmethod
    def select_recommend_list_from(cls, filtered_recommend_list, recommend_condition):
        filtered_recommend_list_with_score = []
        for recommend_item in filtered_recommend_list:
            filtered_recommend_list_with_score.append(FilteredRecommendItemWithScore(recommend_item, 0))
        cls.selected_recommend_list = filtered_recommend_list_with_score

        interesting_division = cls.get_interesting_categories_and_divisions(recommend_condition)
        for index, recommend_item in enumerate(cls.selected_recommend_list):
            cls.add_score_which_has_interesting_division(index, recommend_condition, recommend_item,
                                                         interesting_division)
            cls.add_score_which_has_relative_word(index, recommend_item, recommend_condition)
            cls.add_score_close_today(index, recommend_item)
            cls.subtract_score_which_has_unrelated_word(index, recommend_item, recommend_condition)
        result_recommend_list = cls.sort_by_score_desc()
        if result_recommend_list.__len__() < 10:
            return result_recommend_list
        else:
            return result_recommend_list[0:10]

    @classmethod
    def add_date_condition_within_7days(cls, sql):
        return sql + 'DATE(date) >= DATE(subdate(now(), INTERVAL 6 DAY)) AND DATE (date) <= DATE(now())'

    @classmethod
    def add_category_and_division_condition(cls, recommend_condition, sql):
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

        if recommend_condition.interest_event is not 2:
            division_list.append(recommend_condition.INTEREST_EVENT)
        else:
            uninteresting_division_list.append(recommend_condition.INTEREST_EVENT)

    @classmethod
    def filter_by_uninteresting_division(cls, uninteresting_division_list, sql):
        if uninteresting_division_list.__len__() > 0:
            sql += ' AND not division in ('
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
        category_list = recommend_condition.majors.split('-')
        if recommend_condition.interest_career is not 2:
            category_list.extend([recommend_condition.INTEREST_CAREER])
        for index, major in enumerate(category_list):
            sql += "\"" + major + "\""
            if index < category_list.__len__() - 1:
                sql += ", "
            else:
                sql += '))'
        # set major career visibility invisible when user is uninterested in career
        if recommend_condition.interest_career is 2:
            sql += 'AND division not in (\"' + recommend_condition.INTEREST_CAREER + '\")'
        return sql

    @classmethod
    def get_interesting_categories_and_divisions(cls, recommend_condition):
        interesting_majors_and_divisions = []
        if recommend_condition.interest_scholarship is 1:
            interesting_majors_and_divisions.append(recommend_condition.INTEREST_SCHOLARSHIP)
        if recommend_condition.interest_student is 1:
            interesting_majors_and_divisions.append(recommend_condition.INTEREST_STUDENT)
        if recommend_condition.interest_career is 1:
            interesting_majors_and_divisions.append(recommend_condition.INTEREST_CAREER)
        if recommend_condition.interest_system is 1:
            interesting_majors_and_divisions.append(recommend_condition.INTEREST_SYSTEM)
        if recommend_condition.interest_recruit is 1:
            interesting_majors_and_divisions.append(recommend_condition.INTEREST_RECRUIT)
        if recommend_condition.interest_academic is 1:
            interesting_majors_and_divisions.append(recommend_condition.INTEREST_ACADEMIC)
        if recommend_condition.interest_global is 1:
            interesting_majors_and_divisions.append(recommend_condition.INTEREST_GLOBAL)
        if recommend_condition.interest_event is 1:
            interesting_majors_and_divisions.append(recommend_condition.INTEREST_EVENT)
        interesting_majors_and_divisions.extend(recommend_condition.majors.split('-'))
        return interesting_majors_and_divisions

    @classmethod
    def add_score_which_has_interesting_division(cls, index, recommend_condition, recommend_item,
                                                 interesting_majors_and_divisions):
        if recommend_item.record.category not in recommend_condition.majors.split(
                '-') and recommend_item.record.division in interesting_majors_and_divisions:
            cls.selected_recommend_list[index].score += 0.5 * 0.4
        elif recommend_item.record.category in interesting_majors_and_divisions:
            if recommend_item.record.division in ['취업']:
                if '취업' not in interesting_majors_and_divisions:
                    cls.selected_recommend_list[index].score += 0.5 * 0.4
                elif '취업' in interesting_majors_and_divisions:
                    cls.selected_recommend_list[index].score += 1 * 0.4
            else:
                cls.selected_recommend_list[index].score += 0.5 * 0.4

    @classmethod
    def add_score_which_has_relative_word(cls, index, recommend_item, recommend_condition):
        # 학년
        relative_words_with_user = {
            1: ["저학년", "신입생", "새내기", "입학식", "3학기", "1학년"],
            2: ["저학년", " 2학년", "전과", "교환학생", "전공선택", "3학기", "4학기", "학·석사"],
            3: ["고학년", " 3학년", "조기졸업", "전공선택" "5학기", "6학기", "교환학생", "학·석사", "대학원"],
            4: ["고학년", " 4학년", "수료생", "졸업", "학위", "7학기", "8학기", "졸준위", "대학원"]
        }.get(recommend_condition.student_grade)

        # 공통
        relative_words_with_user.extend(["등록"])

        # 전공
        relative_words_with_user.extend(recommend_condition.majors.split('-'))

        # 학번
        relative_words_with_user.extend([str(recommend_condition.student_year) + "학번"])

        # 재/휴학
        if recommend_condition.student_status is recommend_condition.STATUS_IN:
            relative_words_with_user.extend(
                ["재학생", "수강신청", "수강정정", "학사일정", "수업평가", "성적", "학생지도의 날", "계절학기", "소멸과목"])
        else:
            relative_words_with_user.extend(["복학", "휴학", "등록"])

        # 장학
        if recommend_condition.interest_scholarship is 1:
            if recommend_condition.government_scholar:
                relative_words_with_user.extend(["국가장학금"])
            if recommend_condition.school_scholar:
                relative_words_with_user.extend(["자기계발장학", "숙명특별장학", "행정조교", "연구인턴", "고시장학", "숙명장학", "새빛장학", "청파장학"])
            if recommend_condition.external_scholar:
                relative_words_with_user.extend(["장학회", "장학재단", "장학생 선발"])

        if relative_words_with_user is not None:
            count = 0
            for word in relative_words_with_user:
                if word in cls.selected_recommend_list[index].record.title:
                    count += 1
            if count == 0:
                recommend_item.score += 0
            elif count < 2:
                recommend_item.score += 0.5 * 0.2
            else:
                recommend_item.score += 1 * 0.2

    @classmethod
    def sort_by_score_desc(cls):
        return sorted(cls.selected_recommend_list, key=lambda selected_recommend_item: selected_recommend_item.score,
                      reverse=True)

    @classmethod
    def add_score_close_today(cls, index, recommend_item):
        today = datetime.today()
        item_posted_date = datetime.strptime(recommend_item.record.date, "%Y-%m-%d")
        date_distance = today - item_posted_date
        cls.selected_recommend_list[index].score += (1 - (date_distance.days + 1) / 7) * 0.1

    @classmethod
    def subtract_score_which_has_unrelated_word(cls, index, recommend_item, recommend_condition):
        # 학년
        unrelated_words_with_user = {
            1: ["고학년", "수료생", "졸업", "학위복", "학위수여", "학·석사", "신입사원", "졸준위", "대학원"],
            2: ["고학년", "수료생", "졸업", "학위복", "학위수여", "신입생", "새내기", "대학원"],
            3: ["저학년", "수료생", "신입생", "새내기"],
            4: ["저학년", "전과", "신입생", "새내기"]
        }.get(recommend_condition.student_grade)

        if recommend_condition.student_status is recommend_condition.STATUS_IN:
            unrelated_words_with_user.extend(["복학"])
        else:
            unrelated_words_with_user.extend(["학사일정", "수업평가", "성적", "학생지도의 날", "휴학생 제외"])

        if unrelated_words_with_user is not None:
            count = 0
            for word in unrelated_words_with_user:
                if word in recommend_item.record.title:
                    count += 1
            if count == 0:
                cls.selected_recommend_list[index].score += 1 * 0.3
            else:
                cls.selected_recommend_list[index].score += 0
