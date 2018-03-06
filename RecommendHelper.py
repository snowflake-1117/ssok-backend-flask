from FilteredRecommendItemWithScore import FilteredRecommendItemWithScore
from datetime import datetime


class RecommendHelper:
    @classmethod
    def add_date_condition_within_10days(cls, sql):
        return sql + 'DATE(date) >= DATE(subdate(now(), INTERVAL 10 DAY)) AND DATE (date) <= DATE(now())'

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
        if recommend_condition.interest_entrance is not 2:
            division_list.append(recommend_condition.INTEREST_ENTRANCE)
        else:
            uninteresting_division_list.append(recommend_condition.INTEREST_ENTRANCE)

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
        category_list = [recommend_condition.major1, recommend_condition.major2]
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
    def select_recommend_list_from(cls, filtered_recommend_list, recommend_condition):
        if filtered_recommend_list.__len__() < 10:
            return filtered_recommend_list
        else:
            selected_recommend_list = []
            for recommend_item in filtered_recommend_list:
                filtered_recommend_item_with_score = FilteredRecommendItemWithScore(recommend_item, 0)
                selected_recommend_list.append(filtered_recommend_item_with_score)

            interesting_division = cls.get_interesting_categories_and_divisions(recommend_condition)
            for recommend_item in selected_recommend_list:
                cls.add_score_which_has_interesting_division(recommend_item, interesting_division)
                cls.add_score_which_has_relative_word(recommend_item, recommend_condition)
                cls.add_score_close_today(recommend_item)
            result_recommend_list = cls.sort_by_score_desc(selected_recommend_list)
            return result_recommend_list

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
        if recommend_condition.interest_entrance is 1:
            interesting_majors_and_divisions.append(recommend_condition.INTEREST_ENTRANCE)
        interesting_majors_and_divisions.append(recommend_condition.major1)
        interesting_majors_and_divisions.append(recommend_condition.major2)
        return interesting_majors_and_divisions

    @classmethod
    def add_score_which_has_interesting_division(cls, recommend_item, interesting_majors_and_divisions):
        if recommend_item.record.division in interesting_majors_and_divisions:
            recommend_item.score += 1
        elif recommend_item.record.category in interesting_majors_and_divisions:
            recommend_item.score += 1

    @classmethod
    def add_score_which_has_relative_word(cls, recommend_item, recommend_condition):
        relative_words_with_user = {
            1: ["신입", "새내기", "GELT", " 1학년", "학사일정", "수강신청", "수강 신청", "오리엔테이션"],
            2: [" 2학년", "전과", "교환학생", "복수전공", "부전공", "3학기", "4학기"],
            3: [" 3학년", "조기졸업", "복수전공", "부전공" "5학기", "6학기", "교환학생"],
            4: [" 4학년", "수료생", "졸업", "학위복", "학위수여", "7학기", "8학기", "학·석사"]
        }.get(recommend_condition.student_grade)

        relative_words_with_user.extend([str(recommend_condition.student_year) + "학번"])

        if recommend_condition.student_status is recommend_condition.STATUS_IN:
            relative_words_with_user.extend(["재학생"])
        else:
            relative_words_with_user.extend(["휴학", "복학"])

        if recommend_condition.interest_scholarship is not 2:
            if recommend_condition.government_scholar:
                relative_words_with_user.extend(["국가장학금"])
            if recommend_condition.school_scholar:
                relative_words_with_user.extend(["자기계발장학", "숙명특별장학", "행정조교", "연구인턴", "고시장학", "숙명장학", "새빛장학", "청파장학"])
            if recommend_condition.external_scholar:
                relative_words_with_user.extend(["장학회", "장학재단", "장학생 선발"])

        if relative_words_with_user is not None:
            for word in relative_words_with_user:
                if word in recommend_item.record.title:
                    recommend_item.score += 2
                elif word in recommend_item.record.content:
                    recommend_item.score += 1

    @classmethod
    def sort_by_score_desc(cls, selected_recommend_list):
        return sorted(selected_recommend_list, key=lambda selected_recommend_item: selected_recommend_item.score,
                      reverse=True)

    @classmethod
    def add_score_close_today(cls, recommend_item):
        today = datetime.today()
        item_posted_date = datetime.strptime(recommend_item.record.date, "%Y-%m-%d")
        date_distance = today - item_posted_date
        recommend_item.score += 1 / (date_distance.days + 1)
