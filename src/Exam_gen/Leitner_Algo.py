"""
Leitner algorithm, used to select questions based on previous attempts etc...
"""


# ___________________________________________________________LEITNER ALGORITHM
def leitner_algo(nb_of_q, e_questions, t, data_bank):

    from datetime import datetime
    from datetime import timedelta

    # ---------------------------Leitner times spans
    # Define the time-span between each question attempt required based on the Leitner nb. and principle
    def req_timelapse(leitner_nb):

        if leitner_nb == 1:
            return timedelta(days=0)
        elif leitner_nb == 2:
            return timedelta(days=1)
        elif leitner_nb == 3:
            return timedelta(days=2)

    # ---------------------------Question selection logic
    # Select questions based on the previous attempts log
    def select_q(attempts_lst, question_checked):

        attempts_rec = []  # Create soft attempt record list
        for attempt in attempts_lst:
            if attempt.split(" ")[0] == question_checked.q_key: # Compare keys for every attempt logged
                attempts_rec.append(attempt)                    # a record attempts matching

        if len(attempts_rec) == 0:                              # If q has no attempts logged, select q
            e_questions.append(question_checked)
            return

        else:
            last_time = datetime.strptime(attempts_rec[-1].split(" ")[2].strip("\n"), '%Y-%m-%d.%H:%M:%S')
            if t - last_time >= req_timelapse(question_checked.leitner_nb):
                                                                    # If date of last attempt and q leitner number
                e_questions.append(question_checked)                # difference not in range, select question
                return

    # ____________________________________________________________
    # ---------------------------Question selection main algorithm
    # Select the questions based on the Leitner number and the other questions in the exam

    for i in range(len(data_bank)):
        question_checked = data_bank[i]

        if question_checked not in e_questions:             # Checking if the question is already in the exam
            with open('src\Attempts_log.txt', "r") as Attempts_log:
                attempts_lst = Attempts_log.readlines()     # Create a list of attempts
                select_q(attempts_lst, question_checked)

        if len(e_questions) == nb_of_q:
            break                                           # Break loop if number of questions selected = nb_of_q


# ___________________________________________________________TOP-UP ALGORITHM
# Tops up question selections with random questions to reach req. question count if not enough select by Leitner algo
def topup_algo(e_questions, nb_of_q, data_bank):
    from random import shuffle

    if not len(e_questions) == nb_of_q:
        extra_q = []

        for i in range(len(data_bank)):                         # List questions not selected
            if data_bank[i] not in e_questions:
                extra_q.append(data_bank[i])

        shuffle(extra_q)                                        # Shuffle resulting list

        for i in range(nb_of_q - len(e_questions)):
            e_questions.append(extra_q[i])                      # Select a random set of questions to reach q. count
    return
