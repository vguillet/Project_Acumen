"""
Test file, contains the test functions for testing Exam_gen
"""
import pytest


@pytest.fixture     # Define an exam class instance to be used in the tests
def Exam():
    from src.Exam_gen.Exam_Generator import Generate_Exam
    from src.Compatibility_script import compile_data_bank
    topic_table_list = ['CapitalsOfTheAmericas']
    data_bank = compile_data_bank(topic_table_list)
    nb_of_q = len(data_bank)
    Exam = Generate_Exam(nb_of_q, data_bank)
    Exam.select_questions()
    return Exam


def test_leitner_algo(Exam):
    from src.Exam_gen.Leitner_Algo import leitner_algo
    import datetime
    t = datetime.datetime.now().strftime('%Y-%m-%d.%H:%M:%S')
    t = datetime.datetime.strptime(t, '%Y-%m-%d.%H:%M:%S')
    leitner_algo(Exam.nb_of_q, Exam.e_questions, t, Exam.data_bank)
    assert len(Exam.nb_of_q) == len(Exam.e_questions)


def test_topup_algo(Exam):     # Check if the right number of question is selected
    from src.Exam_gen.Leitner_Algo import topup_algo
    e_questions = [1, 2, 3]
    topup_algo(e_questions, Exam.nb_of_q, Exam.data_bank)
    topup_algo(e_questions, Exam.nb_of_q, Exam.data_bank)
    assert len(e_questions) == Exam.nb_of_q


def test_select_questions(Exam):    # Check if the selection process is successful
    assert len(Exam.e_questions) == len(Exam.data_bank)
