from NgramTitle import NgramTitle
from DBManager import DBManager

DBManager

sentence_list = DBManager.select_all_titles()
ngram_title = NgramTitle(sentence_list, 2)
ngram_title.compare_sentence_list()
ngram_title.print_result_upper_50_percent_similarity()
