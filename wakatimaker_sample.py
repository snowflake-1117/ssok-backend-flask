#!/usr/bin/python3
# -*-coding:utf-8-*-
from wakati_maker import WakatiMaker

#  readme
#  you can use WakatiMaker class by calling do_snowe2vec(category, division, text_file_name, wakati_file_name)
#  it exports sql data to txt, parse it, and make wakati.
#  in server-side, you may need to set this -> http://sssunho.tistory.com/56 for exporting sql data to txt

wm = WakatiMaker()

categories = "취업", "공통"
directories = "data/job/", "data/snowe/"
job_divisions = "공지", "취업", "인턴십", "교육", "멘토", "행사"
snowe_division = "공지", "모집", "학사", "행사", "학생", "장학", "시스템"
all_divisions = job_divisions, snowe_division

snowe_outfile_names = "snowe_gongji", "snowe_mojip", "snowe_haksa", "snowe_haengsa", "snowe_haksaeng", "snowe_janghak", "snowe_system"
job_outfile_names = "job_gongji", "job_chuiup", "job_internship", "job_gyoyuk", "job_mentor", "job_haengsa"
all_outfile_names = job_outfile_names, snowe_outfile_names

txt = ".txt"
wakati = ".wakati"

for i in range(0, len(categories)):
    category = categories[i]
    directory = directories[i]
    print(str(i) + " " + category)
    for j in range(0, len(all_divisions[i])):
        division = all_divisions[i][j]
        outfile_name = all_outfile_names[i][j]
        wm.do_snowe2vec(category, division, directory + outfile_name + txt, directory +
                        outfile_name + wakati)

print("ok")
