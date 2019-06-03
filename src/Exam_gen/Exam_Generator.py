"""
This script contains the class Generate_Exam in which is used whenever an exam is generated.
It contains the following methods:
- select_questions
- attempts_gen_dev
- attempts_gen_GUI
- log_attempts
- question_leitner_update
"""


class Generate_Exam:
    def __init__(self, nb_of_q, data_bank):
        """
        Exam generator based on the Leitner system
        Contains functions for:
        - Question selection process
        - Attempt recording
        - Data base updating

        :param nb_of_q: Contains the number requested for this exam
        """
        self.nb_of_q = nb_of_q
        self.data_bank = data_bank
        self.e_questions = []
        self.attempts = []
        self.t = 0

# ___________________________________________________________QUESTION COMPILATION ALGORITHM
    def select_questions(self):  # Select questions for the exam
        from src.Exam_gen.Leitner_Algo import leitner_algo, topup_algo

        from random import shuffle
        import datetime

        e_questions = []                        # Will be used to record questions in the exam generated
        t = datetime.datetime.now().strftime('%Y-%m-%d.%H:%M:%S')
        t = datetime.datetime.strptime(t, '%Y-%m-%d.%H:%M:%S')

        leitner_algo(self.nb_of_q, e_questions, t, self.data_bank)   # Selection questions based on the Leitner algorithm

        # Tops up the exam in case a few questions are missing to reach question count due to selection algorithm
        topup_algo(e_questions, self.nb_of_q, self.data_bank)

        shuffle(e_questions)                    # Shuffle the exam questions

        self.e_questions = e_questions
        self.t = t

# ___________________________________________________________CREATE, COLLECT AND RECORD ATTEMPTS PROCESS
    def attempts_gen_dev(self):                     # Output exam text and collect/record exams attempts results
        from src.Classes_dict import Attempt
        from dbinterface.DBAlgoAPI import KeyCodeTools

        for i in range(len(self.e_questions)):
            q = self.e_questions[i]
            subject = KeyCodeTools().get_all_subject_id_name_pairs()[int(q.q_key.split(".")[0])]
            topic = KeyCodeTools().get_all_topics_id_name_pairs(subject)[int(q.q_key.split(".")[1])]

            print(".....................")
            print("Subject:", subject)
            print("Topic:", topic)
            print("\n")
            print("Q:", i+1)                    # Print question number
            print(q.q_str)                      # Print question text
            print("\n")
            # input("Hit ENTER to display ANSWER")  # TODO uncomment display answer
            print("Answer:", q.q_ans)           # Print question answer
            print("\n")

            # Request user input on attempts for the questions generated
            x = int(input("Did you get the question right? 0- No ; 1- Yes :"))  # Request attempt results

            while not x == 0 and not x == 1:
                print("Wrong entry")
                x = int(input("Enter attempt result again: 0-No ; 1-Yes :"))

            self.attempts.append(Attempt(q.q_key, x))       # Log attempts on Attempts_log

    def attempts_gen_GUI(self, i):                          # Output exam text and collect/record exams attempts results
        from src.Classes_dict import Attempt
        from dbinterface.DBAlgoAPI import KeyCodeTools

        q = self.e_questions[i]
        self.subject = KeyCodeTools().get_all_subject_id_name_pairs()[int(q.q_key.split(".")[0])]
        self.topic = KeyCodeTools().get_all_topics_id_name_pairs(self.subject)[int(q.q_key.split(".")[1])]

    def getsubtop(self, i):
        from dbinterface.DBAlgoAPI import KeyCodeTools
        q = self.e_questions[i]
        self.subject = KeyCodeTools().get_all_subject_id_name_pairs()[int(q.q_key.split(".")[0])]
        self.topic = KeyCodeTools().get_all_topics_id_name_pairs(self.subject)[int(q.q_key.split(".")[1])]

        return self.subject, self.topic

    def attempts_append_GUI(self, question, score):
        from src.Classes_dict import Attempt
        self.attempts.append(Attempt(question.q_key, score))  # Log attempts on Attempts_log

    def log_attempts(self):
            with open('src\Attempts_log.txt', "a") as Attempts_log:
                for a in self.attempts:
                    Attempts_log.write(" ".join([a.q_key, str(a.success), str(a.date_attempted)]) + "\n")
            # Log entry format: "'Question key' 'Success/failure' 'Date of attempt"."Time of attempt'"

# ___________________________________________________________QUESTION LEITNER NUMBER UPDATER
    def question_leitner_update(self):
        from dbinterface.DBAlgoAPI import KeyCodeTools

        def update_nb(attempts_lst, question):
            for attempt in reversed(attempts_lst):  # Go through attempts log backward to locate last attempt
                if attempt.split(" ")[0] == question.q_key:     # Check for attempt question key

                    if int(attempt.split(" ")[1]) == 0:         # Check matching question Leitner number status
                        question.leitner_nb = 1                 # and update accordingly
                        KeyCodeTools().update_leitner_number(question.q_key, question.leitner_nb)
                        return print("Q.Key:", question.q_key, "New Leitner nb:", question.leitner_nb)
                    else:
                        if question.leitner_nb != 3:
                            question.leitner_nb = question.leitner_nb + 1
                            KeyCodeTools().update_leitner_number(question.q_key, question.leitner_nb)
                        return print("Q.Key:", question.q_key, "New Leitner nb:", question.leitner_nb)

        with open('src\Attempts_log.txt', "r") as Attempts_log:
            attempts_lst = Attempts_log.readlines()             # Create a list of attempts
            for question in self.e_questions:
                update_nb(attempts_lst, question)               # the Leitner number is updated

        # Print process overview
        print("\n...................................................................\n")
        print("Attempts logged and Leitner numbers updated")
        with open('src\Attempts_log.txt', "r") as Attempts_log:
            print("Nb. of Logged attempts:", len(Attempts_log.readlines()))
