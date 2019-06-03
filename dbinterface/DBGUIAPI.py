import sqlite3
from dbinterface import configuration
from dbinterface.DBAlgoAPI import KeyCodeTools


class DBManager():

    def __init__(self):
        """
        This method initializes the KeyCodeTools class with the parameter db being the str of the
        database's name including its .db extensioni.e. 'testdb.db'
        :param db: str of database's name including its .db extensioni.e. 'testdb.db'
        """
        self.db = configuration.database_path
        self.connection = sqlite3.connect(self.db)
        self.cursor = self.connection.cursor()

    def close(self):
        print("Closing connection with the database")
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

    def __enter__(self):
        # make a database connection and return it
        # self.connect = sqlite3.connect(self.db)
        # self.cursor = self.connection.cursor()
        return self

    def __exit__(self):
        # make sure the dbconnection gets closed
        return self.close()

    def get_question_keycode(self, topic_name, questionid):
        """

        :param topic_name: str of the name of the topic table containing all the questions to be displayed
        :param questionid: an int representing the QuestionID select. I.e. the 1st question has a QuestionID of 1,
        the 2nd question has a QuestionID of 2 etc...
        :return: the super duper uber special unique KeyCode of the question corresponding to the question (QuestionOD)
        select by the user
        """
        get_question_keycode_sql = "SELECT KeyCode FROM {0} WHERE QuestionID = {1}".format(topic_name, questionid)
        self.cursor.execute(get_question_keycode_sql)
        result = self.cursor.fetchone()
        qid = result[0]
        return qid

    def get_table_last_row_id(self, topic_name):
        last_row_id_sql = "SELECT SubjectID, TopicID, QuestionID FROM {0} ORDER BY QuestionID DESC limit 1".format(
            topic_name)
        self.cursor.execute(last_row_id_sql)
        rowids = self.cursor.fetchone()
        qid = str(rowids[2])
        tid = str(rowids[1])
        sid = str(rowids[0])
        delimeter = '.'
        keycode = delimeter.join([sid, tid, qid])
        return keycode

    def get_table_next_row_id(self, topic_name):
        last_row_id_sql = "SELECT SubjectID, TopicID, QuestionID FROM {0} ORDER BY QuestionID DESC limit 1".format(
            topic_name)
        self.cursor.execute(last_row_id_sql)
        rowids = self.cursor.fetchone()
        nextqidint = rowids[2] + 1
        nextqidstr = str(nextqidint)
        nexttidstr = str(rowids[1])
        nextsidstr = str(rowids[0])
        delimeter = '.'
        nextkeycode = delimeter.join([nextsidstr, nexttidstr, nextqidstr])
        return nextkeycode

    def insert_q_keycode(self, topic_name):
        keycode = self.get_table_last_row_id(topic_name)
        # keycodes = keycode.split('.')
        # questionid = int(keycodes[-1])
        q_keycode_insert_sql = "INSERT INTO {0} (KeyCode) VALUES (?) WHERE QuestionID = questionid".format(topic_name)
        self.cursor.execute(q_keycode_insert_sql, (keycode,))
        self.connection.commit()

    def get_all_table_data(self, table_name):
        """
        :param table_name: a str of the name of the table (subject or topic) to get data from
        :return: a list of nested tupels with each tuple containing all the data of one row
        """
        infolist = []
        get_all_table_data_sql = "SELECT * FROM '{0}'".format(table_name)
        self.cursor.execute(get_all_table_data_sql)
        results = self.cursor.fetchall()
        for row in results:
            infolist.append(row)
        return infolist

    def get_all_subjects_list(self):
        subjects_list = []
        get_all_subjects_sql = "SELECT Subject FROM SubjectsDB"
        self.cursor.execute(get_all_subjects_sql)
        results = self.cursor.fetchall()
        for row in results:
            subjects_list.append(row[0])
        return subjects_list

    def get_all_subject_topics_dict(self, table_name = None):
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
        if table_name is None:
            return subject_topics_dict
        else:
            table_name_rows = subject_topics_dict[table_name]
            return table_name_rows

    def get_table_last_row_id(self, topic_name):
        """
        :param topic_name: the name of the topic table
        :return: an str of 3 numbers delimited by 2 dots representing the KeyCode
         of the last (question) row entry in the topic table. I.e. '4,3,18' where:
        1st number) SubjectID i.e. 4
        2nd number) TopicID i.e. 3
        3rd number) QuestionID i.e. 18
        """
        last_row_id_sql = "SELECT SubjectID, TopicID, QuestionID FROM {0} ORDER BY QuestionID DESC limit 1".format(
            topic_name)
        self.cursor.execute(last_row_id_sql)
        rowids = self.cursor.fetchone()
        qid = str(rowids[2])
        tid = str(rowids[1])
        sid = str(rowids[0])
        delimeter = '.'
        keycode = delimeter.join([sid, tid, qid])
        return keycode

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

    def get_table_next_row_id(self, topic_name, subject_name):
        """
        :param topic_name: the name of the topic table
        :return: an str of 3 numbers delimited by 2 dots representing the KeyCode
         of the NEXT last (question) row entry in the topic table. I.e. '4,3,19' where:
        1st number) SubjectID i.e. 4
        2nd number) TopicID i.e. 3
        3rd number) QuestionID i.e. 19
        new_last_row_id: 4,3,19' & last_row_id 4,3,18'
        """
        last_row_id_sql = "SELECT SubjectID, TopicID, QuestionID FROM {0} ORDER BY QuestionID DESC limit 1".format(
            topic_name)
        self.cursor.execute(last_row_id_sql)
        rowids = self.cursor.fetchone()
        if rowids is None:
            nextqidstr = str(1)
            nexttidstr = str(self.get_all_topic_name_id_pairs(subject_name)[topic_name])
            nextsidstr = str(self.get_all_subject_name_id_pairs()[subject_name])
            delimeter = '.'
            nextkeycode = delimeter.join([nextsidstr, nexttidstr, nextqidstr])
            return nextkeycode
        else:
            nextqidint = rowids[2] + 1
            nextqidstr = str(nextqidint)
            nexttidstr = str(rowids[1])
            nextsidstr = str(rowids[0])
            delimeter = '.'
            nextkeycode = delimeter.join([nextsidstr, nexttidstr, nextqidstr])
            return nextkeycode

    def get_subject_name_for_given_topic_name(self, topic_name):
        subject_topics_dict = self.get_all_subject_topics_dict()
        for subject in subject_topics_dict:
            for topic in subject_topics_dict[subject]:
                if topic_name == topic:
                    return subject

    def add_new_subject(self, subject_name):
        """
        :param self:
        :param subject_name: name of the new subject being entered into the database
        :return: None
        """
        create_subject_topics_table_sql = """CREATE TABLE '{0}'(TopicID INTEGER PRIMARY KEY,
                                        Topic TEXT NOT NULL,
                                        NumberOfQuestions INTEGER,
                                        CreationDate TEXT NOT NULL,
                                        SubjectID INTEGER,
                                        FOREIGN KEY (SubjectID) REFERENCES SubjectsDB(SubjectID))""".format(
            subject_name)
        self.cursor.execute(create_subject_topics_table_sql)
        add_new_subject_sql = """INSERT INTO SubjectsDB(Subject,CreationDate,NumberOfTopics) 
                              VALUES (?,date('now'),0)"""
        self.cursor.execute(add_new_subject_sql, (subject_name,))
        self.connection.commit()

    def add_new_topic(self, topic_name, subject_name):
        """

        :param topic_name: not a hard one to guess
        :param subject_name: go figure
        :return: None
        """
        create_topic_questions_table_sql = """CREATE TABLE {0}(QuestionID INTEGER PRIMARY KEY,
                                                          KeyCode TEXT,
                                                          Question TEXT NOT NULL,
                                                          Answer TEXT NOT NULL,
                                                          LeitnerNumber INTEGER,
                                                          CorrectAttempts INTEGER,
                                                          TotalAttempts INTEGER,
                                                          LastAttemptResult INTEGER,
                                                          LastAttemptsDate TEXT,
                                                          CreationDate TEXT NOT NULL,
                                                          TopicID INTEGER,
                                                          SubjectID INTEGER,
                                                          FOREIGN KEY (TopicID) REFERENCES {1}(TopicID));""".format(
            topic_name, subject_name)
        self.cursor.execute(create_topic_questions_table_sql)
        add_new_topic_to_subject_table = """INSERT INTO {0}(Topic,NumberOfQuestions,CreationDate,SubjectID) 
                                          VALUES (?,0,date('now'),(SELECT SubjectID FROM SubjectsDB WHERE Subject = '{0}'))""".format(
            subject_name)
        self.cursor.execute(add_new_topic_to_subject_table, (topic_name,))
        update_number_of_topics_sql = "UPDATE SubjectsDB SET NumberOfTopics = NumberOfTopics + 1 WHERE Subject = ?"
        self.cursor.execute(update_number_of_topics_sql, (subject_name,))
        self.connection.commit()

    def add_new_question(self, topic_name, question, answer, subject_name):
        """
        :param topic_name:  topic name
        :param question: an str of the question
        :param answer:  Aan str of the answer
        :param subject_name:  subject name
        :return:
        """
        # last_q_keycode = self.get_table_last_row_id(topic_name)
        # last_q_keycode = self.get_table_next_row_id(topic_name)
        next_last_q_keycode = self.get_table_next_row_id(topic_name,subject_name)
        add_new_question_sql = """INSERT INTO {0}(Question, Answer, LeitnerNumber, CorrectAttempts,TotalAttempts,
                                                      CreationDate, TopicID,SubjectID,KeyCode)
                                                      VALUES ('{1}','{2}',1,0,0,date('now'),
                                                      (SELECT TopicID FROM {3} WHERE Topic='{0}'),
                                                      (SELECT SubjectID FROM SubjectsDB WHERE Subject = '{3}'),
                                                      '{4}')""".format(topic_name, question, answer, subject_name,
                                                                       next_last_q_keycode)
        self.cursor.execute(add_new_question_sql)
        # q_keycode_serty_sql = "INSERT INTO {0}(KeyCode) VALUES (?)".format(topic_name)
        # self.cursor.execute(q_keycode_serty_sql,(keycode,))
        update_number_of_questions_sql = "UPDATE {0} SET NumberOfQuestions = NumberOfQuestions + 1 WHERE Topic = '{1}'".format(
            subject_name, topic_name)
        self.cursor.execute(update_number_of_questions_sql)
        self.connection.commit()

    def drop_table(self, table_name):
        """
        Utility function - Not meant to be used for interaction with GUI script
        :param table_name:
        :return: None
        """
        drop_table_sql = "DROP TABLE {0}".format(table_name)
        self.cursor.execute(drop_table_sql)
        self.connection.commit()

    def delete_question_entry(self, topic_name, questionid):
        """
        :param topic_name: The name of the topic table which this question belongs to.
        :param questionid: This is the QuestionID of the question which has been selected.
        :return: None
        Instead this function removes the question row entry corresponding with the questionid
        """
        qid = self.get_question_keycode(topic_name, questionid)
        delete_question_sql = "DELETE FROM {0} WHERE KeyCode = '{1}'".format(topic_name, qid)
        self.cursor.execute(delete_question_sql)
        subject_name = self.get_subject_name_for_given_topic_name(topic_name)
        update_number_of_question_in_topic_table_sql = "UPDATE {0} SET NumberOfQuestion = NumberOfQuestions - 1 WHERE Topic = '{1}'".format(subject_name, topic_name)
        self.cursor.execute(update_number_of_question_in_topic_table_sql)
        self.connection.commit()

    def clear_all_topic_questions(self, topic_name):
        """
        :param topic_name: The name of the topics table for which all question row entries are to be deleted/cleared/removed
        :return: None
        Instead this function does as mentioned in "param topic_names:"
        """
        delete_all_topic_question_row_entries_sql = "DELETE FROM {0}".format(topic_name)
        self.cursor.execute(delete_all_topic_question_row_entries_sql)
        subject_name = self.get_subject_name_for_given_topic_name(topic_name)
        update_topic_number_of_questions_sql = "UPDATE {0} SET NumberOfQuestions = 0 WHERE Topic = '{1}'".format(subject_name, topic_name)
        print(subject_name, topic_name)
        self.cursor.execute(update_topic_number_of_questions_sql)
        self.connection.commit()

    def delete_topic_entry(self,subject_name, topic_name):
        """
        Utility function - Not meant to be used for interaction with GUI script
        :param subject_name:
        :param topic_name:
        :return: None
        """
        delete_topic_entry = "DELETE FROM  {0} WHERE Topic = ?".format(subject_name)
        self.cursor.execute(delete_topic_entry,(topic_name,))
        self.connection.commit()

    def delete_subject_entry(self, subject_name):
        """
        Utility function - Not meant to be used for interaction with GUI script
        :param subject_name:
        :return: None
        """
        delete_subject_row_entry_from_SubjectsDB_sql = "DELETE FROM SubjectsDB WHERE Subject = '{0}'".format(subject_name)
        self.cursor.execute(delete_subject_row_entry_from_SubjectsDB_sql)
        self.connection.commit()

    def remove_topic_entirely_from_db(self, topic_name):
        """
        This function is meant for entirely removing a topic (table) from the database!
        :param topic_name:
        :return: None
        """
        self.clear_all_topic_questions(topic_name)
        subject_name = self.get_subject_name_for_given_topic_name(topic_name)
        self.delete_topic_entry(subject_name, topic_name)
        self.drop_table(topic_name)
        update_number_of_topics_for_subject_sql = "UPDATE SubjectsDB SET NumberOfTopics = NumberOfTopics - 1 WHERE Subject = '{0}'".format(subject_name)
        self.cursor.execute(update_number_of_topics_for_subject_sql)
        self.connection.commit()

    def remove_subject_entirely_from_db(self, subject_name):
        """
        Removes a subject entirely from the database! This means that the subject row entry in SubjectsDB
        is removed, all the topics (so topic tables) corresponding with the subject are also removed!
        :param subject_name:
        :return: None
        """
        subject_table_topic_entries = self.get_all_subject_topics_dict(table_name = subject_name)
        for topic_name in subject_table_topic_entries:
            self.remove_topic_entirely_from_db(topic_name)
        self.drop_table(subject_name)
        self.delete_subject_entry(subject_name)

    def edit_table_name(self, current_table_name, new_table_name):
        """
        Utility function - Not meant to be used for interaction with GUI script
        :param current_table_name:
        :param new_table_name:
        :return: None
        """
        edit_table_name_sql = "ALTER TABLE {0} RENAME TO {1}".format(current_table_name, new_table_name)
        self.cursor.execute(edit_table_name_sql)
        self.connection.commit()

    def edit_subject_or_topic_name_attribute(self, new_name,  current_subject_name = None, current_topic_name = None):
        """
        :param new_name: str of the new name to replace the old name of a subject or topic
        :param current_subject_name: str of the current name of the subject (table) in the db
        :param current_topic_name:  str of the current name of the topic (table) in the db
        :return: None
        NOTE!: This function can either change the name of a subject or topic given a new name
        BUT cannot do both simultaneously! You must either provided a new_name and a current_subject_name
        OR a new_name and a current_topic_name BUT NOT a new_name, current_subject_name and a
        current_topic_name
        """
        if current_subject_name is not None and current_topic_name is None:
            old_subject_name = current_subject_name
            new_subject_name = new_name
            self.edit_table_name(old_subject_name, new_subject_name)
            edit_subject_name_in_SubjectsDB_table_sql = "UPDATE SubjectsDB SET Subject = {0} WHERE Subject = {1}".format(old_subject_name, new_subject_name)
            self.cursor.execute(edit_subject_name_in_SubjectsDB_table_sql)
            self.connection.commit()
        elif current_subject_name is None and current_topic_name is not None:
            subject_name = self.get_subject_name_for_given_topic_name(current_topic_name)
            old_topic_name = current_topic_name
            new_topic_name = new_name
            self.edit_table_name(old_topic_name, new_topic_name)
            edit_topic_name_in_parent_subject_table_sql = "UPDATE {0} SET Topic = '{1}' WHERE Topic = '{2}'".format(subject_name, new_topic_name, old_topic_name)
            self.cursor.execute(edit_topic_name_in_parent_subject_table_sql)
            self.connection.commit()

    def edit_question_for_given_keycode(self, keycode, new_question_str):
        """
        Modifies the question string for a given question corresponding with the keycode provided
        :param keycode: keycode of a question i.e. "1.3.4"
        :param new_question_str: the new question string to replace the old question string
        :return: None
        """
        names = KeyCodeTools().get_keycode_to_english_translation(keycode)
        topic_name = names.split('.')[1]
        edit_question_str_sql = """UPDATE {0} SET Question = '{1}' 
        WHERE KeyCode = '{2}'""".format(topic_name, new_question_str, keycode)
        self.cursor.execute(edit_question_str_sql)
        self.connection.commit()

    def edit_answer_for_given_keycode(self, keycode, new_answer_str):
        """
        :param keycode: keycode of a question i.e. "1.3.4"
        :param new_answer_str: the new answer string to replace the old answer string
        :return: None
        """
        names = KeyCodeTools().get_keycode_to_english_translation(keycode)
        topic_name = names.split('.')[1]
        edit_answer_str_sql = """UPDATE {0} SET Answer = '{1}'
        WHERE KeyCode = '{2}'""".format(topic_name, new_answer_str, keycode)
        self.cursor.execute(edit_answer_str_sql)
        self.connection.commit()






