sookpam-backend-flask

# MLP - university faculties
#### needed data
    - job
        * gongji.txt : 공지
        * job_chuiup.wakati
        * job_gongji.wakati
        * job_gyoyuk.wakati
        * job_haengsa.wakati
        * job_internship.wakati
        * job_mentor.wakati
    - snowe
        * gongji.txt : 공지
        * snowe_gongji.wakati
        * snowe_haengsa.wakati
        * snowe_haksa.wakati
        * snowe_haksaeng.wakati
        * snowe_janghak.wakati
        * snowe_mojip.wakati
        * snowe_system.wakati

 > please make sure the outputs of word2vec named as exactly as names mentioned above

#### Output
+ word-dic.json : words mapped with numbers( I guess ), this is a output of word_dic_generator.py and will be needed when decoding to classify the data.json
+ data.json : encoded data json file
+ model.h5py : model for keras (since keras classifier did not work out with h5, had to import h5py)


