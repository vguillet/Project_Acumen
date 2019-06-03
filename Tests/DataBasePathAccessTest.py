from Group12.dbinterface.DBGUIAPI import DBManager

def test_add_new_subject():
    # make a subject name called "mcboatface"
    # check if the subject exists
    # Due to the fact we are dealing with the real database we don't want to save any data we are creating
    # this also checks if the remove subject function works as intended if the test is repeated multiple times

    subject_name = "mcboatface4"
    DBManager().add_new_subject(subject_name)
    subject_list = DBManager().get_all_subjects_list()
    assert subject_name in subject_list
    print('New subject was created, success. Now we are going to delete the subject')
    DBManager().remove_subject_entirely_from_db(subject_name)
    print("test subject deleted successfully")

def test_add_new_topic():
    # make a subject name called "hitest" under subject "History"
    # check if the topic exists
    # Due to the fact we are dealing with the real database we don't want to save any data we are creating
    # this also checks if the remove topic function works as intended if the test is repeated multiple times

    topic_name = "hitest"
    subject_name = "History"
    DBManager().add_new_topic(topic_name, subject_name)
    topicList = DBManager().get_all_subject_topics_dict()
    assert topic_name in topicList.get(subject_name)
    print('New topic was created, success. Now we are going to delete the topic')
    DBManager().remove_topic_entirely_from_db(topic_name)
    print("test topic deleted successfully")

if __name__ == '__main__':
    #run all tests look at subjects and topics before and after
    # print(DBManager().get_all_subjects_list())
    # print(DBManager().get_all_subject_topics_dict())
    test_add_new_subject()
    test_add_new_topic()
    # print(DBManager().get_all_subjects_list())
    # print(DBManager().get_all_subject_topics_dict())
