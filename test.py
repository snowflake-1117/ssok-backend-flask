import RelevantContentCommender
from DBManager import DBManager
import random

sentence_list = DBManager.select_all_titles()
random_sentence = random.choice(sentence_list)
print("> ", random_sentence)

RelevantContentCommender.compare_with(random_sentence)
RelevantContentCommender.get_max()