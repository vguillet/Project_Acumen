"""
Main process followed for exam generation
"""

from dbinterface.DBAlgoAPI import KeyCodeTools
from src.Exam_gen.Exam_Generator import Generate_Exam
from src.Compatibility_script import compile_data_bank


def exam_gen_process():

    # _____________________________________________ SUB-MENU FOR SELECTING EXAM GENERATION PARAMETERS

    # print("\n")
    # print(KeyCodeTools().get_all_subject_id_name_pairs())
    #
    # topic_table_list = []
    # selection = True
    # while selection:
    #     subject = input("Type the name of the subject requested one by one (enter 'Done' when done):\n")
    #     if not subject == "Done":
    #         topic_table_list.append(subject)
    #     else:
    #         selection = False

    topic_table_list = ['CapitalsOfTheAmericas', 'CapitalsOfTheMiddleEast', 'CapitalsOfTheEU']

    # TODO Luke - 29, 43, 45, 51(can't be called, need to be re-writen for GUI), 53, 56
    data_bank = compile_data_bank(topic_table_list)
    print(data_bank)

    print("\n")
    print("How any questions do you want in the exam?")
    print("Max number of questions allowed :", len(data_bank))
    nb_of_q = int(input("Selected number of questions :"))

    while nb_of_q > len(data_bank):
        print("The data bank does not contain enough questions")
        nb_of_q = int(input("Please selected again the number of questions ="))

    # _____________________________________________ EXAM GENERATION PROCESS

    Exam = Generate_Exam(nb_of_q, data_bank)    # Create an exam based on the exam class

    Exam.select_questions()                     # Select Exam based on the Leitner algorithm

    print("\n___________________________________________________________________\n")
    print("Exam date:", Exam.t)                 # Print date and time of exam generated
    print("\n")

    Exam.attempts_gen_dev()                         # Output questions on screen and store results

    Exam.log_attempts()                         # Log attempts to log file
    print("____Exam finished____")

    Exam.question_leitner_update()              # Update Data bank's leitner number

    print("\n Correct Leitner numbers:")
    for q in data_bank:
        print(q.leitner_nb)
