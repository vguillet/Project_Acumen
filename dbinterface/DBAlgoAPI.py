import sqlite3
from dbinterface import configuration


class KeyCodeTools():

    def __init__(self):
        """
        This method initializes the KeyCodeTools class with the parameter db being the str of the
        database's name including its .db extensioni.e. 'testdb.db'
        :param db: str of database's name including its .db extensioni.e. 'testdb.db'
        """
        self.db = configuration.database_path
        self.connect = sqlite3.connect(self.db)
        self.cursor = self.connect.cursor()

    def close(self):
        print("Closing connection with the database")
        self.connect.commit()
        self.cursor.close()
        self.connect.close()

    def __enter__(self):
        # make a database connection and return it
        # self.connect = sqlite3.connect(self.db)
        # self.cursor = self.connection.cursor()
        return self

    def __exit__(self):
        # make sure the dbconnection gets closed
        return self.close()

    def get_all_subject_id_name_pairs(self):
        subject_id_pairs_pairs_dict = {}
        get_all_subjectids_sql = "SELECT SubjectID FROM SubjectsDB "
        self.cursor.execute(get_all_subjectids_sql)
        subjectids = self.cursor.fetchall()
        return subjectids

    def get_table_last_row_id(self, topic_name):
        """
        :param topic_name: the name of the topic table
        :return: an str of 3 numbers delimited by 2 dots representing the KeyCode
         of the last (question) row entry in the topic table. I.e. '4,3,18' where:
        1st number) SubjectID i.e. 4
        2nd number) TopicID i.e. 3
        3rd number) QuestionID i.e. 18
        """
        last_row_id_sql = "SELECT SubjectID, TopicID, QuestionID FROM {0} ORDER BY QuestionID DESC limit 1".format(topic_name)
        self.cursor.execute(last_row_id_sql)
        rowids = self.cursor.fetchone()
        qid = str(rowids[2])
        tid = str(rowids[1])
        sid = str(rowids[0])
        delimeter = '.'
        keycode = delimeter.join([sid, tid, qid])
        return keycode

    def get_all_subject_id_name_pairs(self):
        """
        :return: a dict of all SubjectID:Subject pairs present in the SubjectsDB table (all the subjects in the db)
        """
        subject_id_name_pairs_dict = {}
        get_all_subject_ids_names_sql = "SELECT SubjectID,Subject FROM SubjectsDB "
        self.cursor.execute(get_all_subject_ids_names_sql)
        results = self.cursor.fetchall()
        for row in results:
            subject_id = row[0]
            subject_name = row[1]
            subject_id_name_pairs_dict[subject_id] = subject_name
        return subject_id_name_pairs_dict

    def get_all_topics_id_name_pairs(self,subject_name):
        """
        :return: a dict of all SubjectID:Subject pairs present in the SubjectsDB table (all the subjects in the db)
        """
        topics_id_name_pairs_dict = {}
        get_all_topics_ids_names_sql = "SELECT TopicID,Topic FROM {0} ".format(subject_name)
        self.cursor.execute(get_all_topics_ids_names_sql)
        results = self.cursor.fetchall()
        for row in results:
            topics_id = row[0]
            topics_name = row[1]
            topics_id_name_pairs_dict[topics_id] = topics_name
        return topics_id_name_pairs_dict

    def get_all_subject_name_id_pairs(self):
        """
        :return: a dict of all Subject:SubjectID pairs present in the SubjectsDB table (all the subjects in the db)
        """
        subject_name_id_pairs_dict = {}
        get_all_subject_ids_names_sql = "SELECT SubjectID,Subject FROM SubjectsDB "
        self.cursor.execute(get_all_subject_ids_names_sql)
        results = self.cursor.fetchall()
        for row in results:
            subject_id = row[0]
            subject_name = row[1]
            subject_name_id_pairs_dict[subject_name] = subject_id
        return subject_name_id_pairs_dict

    def get_all_topic_name_id_pairs(self, subject_name):
        """
        :return: a dict of all Subject:SubjectID pairs present in the SubjectsDB table (all the subjects in the db)
        """
        topic_name_id_pairs_dict = {}
        get_all_topics_ids_names_sql = "SELECT TopicID,Topic FROM {0}".format(subject_name)
        self.cursor.execute(get_all_topics_ids_names_sql)
        results = self.cursor.fetchall()
        for row in results:
            topic_id = row[0]
            topic_name = row[1]
            topic_name_id_pairs_dict[topic_name] = topic_id
        return topic_name_id_pairs_dict

    def get_all_keycodes(self, topic_table_name):
        get_all_table_data_sql = "SELECT * FROM '{0}'".format(topic_table_name)
        self.cursor.execute(get_all_table_data_sql)
        results = self.cursor.fetchall()
        keycodes = []
        for row in results:
            qid = str(row[0])
            tid = str(row[10])
            sid = str(row[11])
            delimeter = '.'
            keycode = delimeter.join([sid, tid, qid])
            keycodes.append(keycode)
        return keycodes

    def get_question_amount(self, topic_table_name):
        get_all_table_data_sql = "SELECT * FROM '{0}'".format(topic_table_name)
        self.cursor.execute(get_all_table_data_sql)
        results = self.cursor.fetchall()
        question_amount = 0
        for row in results:
            question_amount += 1
        return question_amount


    def get_all_questions(self, topic_table_name):
        get_all_table_data_sql = "SELECT * FROM '{0}'".format(topic_table_name)
        self.cursor.execute(get_all_table_data_sql)
        results = self.cursor.fetchall()
        questions = []
        for row in results:
            questions.append(row[2])
        return questions

    def get_all_answers(self, topic_table_name):
        get_all_table_data_sql = "SELECT * FROM '{0}'".format(topic_table_name)
        self.cursor.execute(get_all_table_data_sql)
        results = self.cursor.fetchall()
        answers = []
        for row in results:
            answers.append(row[3])
        return answers

    def get_all_leitnernums(self, topic_table_name):
        get_all_table_data_sql = "SELECT * FROM '{0}'".format(topic_table_name)
        self.cursor.execute(get_all_table_data_sql)
        results = self.cursor.fetchall()
        leitnernums = []
        for row in results:
            leitnernums.append(row[4])
        return leitnernums

    def get_keycode_to_english_translation(self, keycode):
        """
        :param keycode: str of the keycode of a question
        :return: provides a translation of the first(subject) and second(topic) part of the keycode provided
        in order to determine what they represent
        """
        sid = keycode.split('.')[0]
        tid = keycode.split('.')[1]
        get_subjectname_for_subjectid_sql = "SELECT Subject FROM SubjectsDB WHERE SubjectID = '{0}'".format(sid)
        self.cursor.execute(get_subjectname_for_subjectid_sql)
        subject_name = self.cursor.fetchone()[0]
        get_topicname_for_topicid_name_sql = "SELECT Topic from {0} WHERE TopicID = '{1}'".format(subject_name, tid)
        self.cursor.execute(get_topicname_for_topicid_name_sql)
        topic_name = self.cursor.fetchone()[0]
        # print(type(topic_name)) type <str>
        names = subject_name + '.' + topic_name
        return names

    def get_english_to_keycode_translation(self,subject_name = None, topic_name = None):
        """
        :param subject_name: the str name of the subject for which you wish to get the keycode of. None by default
        :param topic_name: the str name of the topic for which you wish to get the keycode of. None by default
        :return: the
        """
        get_subjectid_for_subjectname_sql = "SELECT SubjectID FROM SubjectsDB WHERE Subject = '{0}'".format(subject_name)
        get_topicid_for_topicname_sql = "SELECT TopicID FROM {0} WHERE Topic = '{1}'".format(subject_name, topic_name)
        if subject_name and topic_name is not None:
            self.cursor.execute(get_subjectid_for_subjectname_sql)
            subjectid = str(self.cursor.fetchone()[0])
            self.cursor.execute(get_topicid_for_topicname_sql)
            topicid = str(self.cursor.fetchone()[0])
            subject_topic_keycode = subjectid + '.' + topicid
            return subject_topic_keycode
        elif subject_name is not None and topic_name is None:
            self.cursor.execute(get_subjectid_for_subjectname_sql)
            subjectid = str(self.cursor.fetchone()[0])
            return subjectid
        elif subject_name is None and topic_name is not None:
            all_subjects_list = KeyCodeTools().get_all_subjects_list()
            for subject in all_subjects_list:
                all_subject_topics_list = KeyCodeTools().get_all_subject_topics_dict(subject)
                if topic_name in all_subject_topics_list:
                    subject_name = subject
                    get_topicid_for_topicname_sql = "SELECT TopicID FROM {0} WHERE Topic = '{1}'".format(subject_name,topic_name)
                    self.cursor.execute(get_topicid_for_topicname_sql)
                    topicid = str(self.cursor.fetchone()[0])
                    return topicid

    def get_all_subjects_list(self):
        """
        :return: A list of all the subjects contained within the database (so in the SubjectsDB table)
        """
        subjects_list = []
        get_all_subjects_sql = "SELECT Subject FROM SubjectsDB"
        self.cursor.execute(get_all_subjects_sql)
        results = self.cursor.fetchall()
        for row in results:
            subjects_list.append(row[0])
        return subjects_list

    def get_all_subject_topics_dict(self, subject_name = None):
        """
        :param subject_name: The name of the specific subject for which you want the topics of, None
        by default.
        :return: If subject_name is left as it is (so None) then a dictionary consisting of
        the key:value pairs subject:list of topics is returned. IF however the name of a subject is passed
        in as an argument for subject_name then only the topics belonging to this subject are returned, again
        in tjhe form of a dictionary (so a dictionary with only one key with that being the name of the
        subject and the corresponding value being the list of topics part of this subject)
        """
        subject_topics_dict = {}
        subjects_list = self.get_all_subjects_list()
        for sbj in subjects_list:
            topics_list = []
            get_subject_topics_sql = "SELECT Topic FROM {0}".format(sbj)
            self.cursor.execute(get_subject_topics_sql)
            results = self.cursor.fetchall()
            for row in results:
                topics_list.append(row[0])
            subject_topics_dict[sbj] = topics_list
        if subject_name is None:
            return subject_topics_dict
        else:
            table_name_rows = subject_topics_dict[subject_name]
            return table_name_rows

    def update_leitner_number(self, keycode,newleitnernumber):
        """
        :param keycode: This is the str of the keycode of a question i.e. 1.1.7
        :param newleitnernumber: int representing the new leitner number
        :return: Simply updates the leitner number of the question associated with the keycode provided
        """
        keycodes = keycode.split('.')
        sid = int(keycodes[0])
        tid = int(keycodes[1])
        subject_id_name_pairs = self.get_all_subject_id_name_pairs()
        subject_name = subject_id_name_pairs[sid]
        topic_id_name_pairs = self.get_all_topics_id_name_pairs(subject_name)
        topic_name = topic_id_name_pairs[tid]
        sql = """UPDATE {0} SET LeitnerNumber = {1} 
                  WHERE KeyCode = '{2}'""".format(topic_name, newleitnernumber, keycode)
        self.cursor.execute(sql)
        self.connect.commit()

    def update_correct_attempts(self, keycode):
        """
        :param keycode: This is the str of the keycode of a question i.e. 1.1.7
        :return: Adds 1 to the CorrectAttempts column of the question row entry corresonponding with the
        keycode provided
        """
        sid = int(keycode.split('.')[0])
        tid = int(keycode.split('.')[1])
        subject_id_name_pairs = self.get_all_subject_id_name_pairs()
        subject_name = subject_id_name_pairs[sid]
        topic_id_name_pairs = self.get_all_topics_id_name_pairs(subject_name)
        topic_name = topic_id_name_pairs[tid]
        sql = """UPDATE {0} SET CorrectAttempts = CorrectAttempts + 1 
                  WHERE KeyCode = '{1}'""".format(topic_name, keycode)
        self.cursor.execute(sql)
        self.connect.commit()

    def update_total_attempts(self, keycode):
        """
        :param keycode: This is the str of the keycode of a question i.e. 1.1.7
        :return: Simply adds 1 to the TotalAttempts column for the row corresponding with the
        keycode provided
        """
        sid = int(keycode.split('.')[0])
        tid = int(keycode.split('.')[1])
        subject_id_name_pairs = self.get_all_subject_id_name_pairs()
        subject_name = subject_id_name_pairs[sid]
        topic_id_name_pairs = self.get_all_topics_id_name_pairs(subject_name)
        topic_name = topic_id_name_pairs[tid]
        sql = """UPDATE {0} SET TotalAttempts = TotalAttempts + 1 
                  WHERE KeyCode = '{1}'""".format(topic_name, keycode)
        self.cursor.execute(sql)
        self.connect.commit()

    def update_last_attempt_result(self, keycode,result):
        """
        :param keycode: This is the str of the keycode of a question i.e. 1.1.7
        :param result: 1 if correct and 0 if wrong
        :return:
        """
        sid = int(keycode.split('.')[0])
        tid = int(keycode.split('.')[1])
        subject_id_name_pairs = self.get_all_subject_id_name_pairs()
        subject_name = subject_id_name_pairs[sid]
        topic_id_name_pairs = self.get_all_topics_id_name_pairs(subject_name)
        topic_name = topic_id_name_pairs[tid]
        sql = """UPDATE {0} SET LastAttemptResult = {1} 
                  WHERE KeyCode = '{2}'""".format(topic_name,result, keycode)
        self.cursor.execute(sql)
        self.connect.commit()

    def update_last_attempt_date(self, keycode):
        """
        :param keycode: This is the str of the keycode of a question i.e. 1.1.7
        :return: Updates the LastAttemptsDate column of the row corresponding with the
        keycode provided for a question by updating the date to that of the current date
        """
        sid = int(keycode.split('.')[0])
        tid = int(keycode.split('.')[1])
        subject_id_name_pairs = self.get_all_subject_id_name_pairs()
        subject_name = subject_id_name_pairs[sid]
        topic_id_name_pairs = self.get_all_topics_id_name_pairs(subject_name)
        topic_name = topic_id_name_pairs[tid]
        sql = """UPDATE {0} SET LastAttemptsDate = date('now') 
                  WHERE KeyCode = '{1}'""".format(topic_name, keycode)
        self.cursor.execute(sql)
        self.connect.commit()

    def combine_exam_gen_data(self, topic_table_name):
        dictdata = {}
        keycode_translations = []
        dictdata['keycodes'] = self.get_all_keycodes(topic_table_name)
        for i in dictdata['keycodes']:
            keycode_translation = self.get_keycode_to_english_translation(i)
            keycode_translations.append(keycode_translation)
        dictdata['keycodes_translation'] = list(keycode_translations)
        dictdata['questions'] = self.get_all_questions(topic_table_name)
        dictdata['answers'] = self.get_all_answers(topic_table_name)
        dictdata['leitnernums'] = self.get_all_leitnernums(topic_table_name)
        return dictdata

    def get_subject_name_for_given_topic_name(self, topic_name):
        subject_topics_dict = self.get_all_subject_topics_dict()
        for subject in subject_topics_dict:
            for topic in subject_topics_dict[subject]:
                if topic_name == topic:
                    return subject











