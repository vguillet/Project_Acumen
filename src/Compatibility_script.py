from src.Classes_dict import Question
# from dbinterface import GetExamGenData
# from dbinterface.DBAlgoAPI import KeyCodeTools
# import Group12.dbinterface.final.ScratchKeyCodeUtils.KeyCodeTools as keycodetools
from dbinterface.DBAlgoAPI import KeyCodeTools

# topic_table_name = 'CapitalsOfTheAmericas'


def compile_questions(topic_table_name):
    data = KeyCodeTools().combine_exam_gen_data(topic_table_name)

    keys = data['keycodes']
    q_str = data['questions']
    q_ans = data['answers']
    q_leitner = data['leitnernums']

    new_questions = [Question(keys[i], q_str[i], q_ans[i], q_leitner[i]) for i in range(len(q_str))]
    return new_questions


def compile_data_bank(topic_table_list):
    data_bank = []
    for topic_table_name in topic_table_list:
        data_bank += compile_questions(topic_table_name)
    return data_bank

# # ___________________________________________TEMPORARY DATABASE FOR THE EXAM GEN TO TRAIN
#
# # Enter question text
# str1 = "How are you?"
# str2 = "What's your name?"
# str3 = "Where are you from?"
# str4 = "What do you study?"
# str5 = "How's everything going?"
# str6 = "What are your hobbies?"
#
# # Reformat the data from the databank to question instances
# q1 = Question("1.1.1", str1, "I am alright", 1)
# q2 = Question("1.2.2", str2, "My name is Victor", 1)
# q3 = Question("2.1.3", str3, "I am from France", 2)
# q4 = Question("2.2.4", str4, "I study aerospace engineering", 1)
# q5 = Question("3.1.5", str5, "Everything is going well", 2)
# q6 = Question("3.2.6", str6, "I enjoy sports and music", 3)
#
# # Create question list according to the user's demand
# data_bank = [q1, q2, q3, q4, q5, q6]
#
