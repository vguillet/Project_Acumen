"""
Class dictionary, contains the classes required for the src code:
- Question
- Attempt
"""


# ___________________________________________________________QUESTION CLASS
class Question:
    def __init__(self, q_key, q_str, q_ans, leitner_nb):
        """
        Creates a Question object containing all the information relative to the specific question

        :param q_key: Question reference key
        :param q_str: Contains Question text
        :param q_ans: Contains Question answer
        :param leitner_nb: Leitner number of the question
        """
        self.q_key = q_key
        self.q_str = q_str
        self.q_ans = q_ans
        self.leitner_nb = leitner_nb

    def __str__(self):
        return self.q_key


# ___________________________________________________________ATTEMPT CLASS
class Attempt:
    def __init__(self, q_key, success):
        """
        Creates an attempt object containing all the information relative to a specific Question's answer attempt

        :param q_key: Contains the key of the matching Question
        :param success: Contains if the attempts was successful or not (0-Wrong 1-Correct)
        """
        import datetime

        self.q_key = q_key
        self.success = success
        self.date_attempted = datetime.datetime.now().strftime('%Y-%m-%d.%H:%M:%S')
