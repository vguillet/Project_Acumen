"""
Pre-processing of the Attempts log and formatting to Pandas dataframe
"""


def format_attempts(keylst):
    # ___________________________________________________________INITIALISATION OF STATS GENERATOR
    import datetime
    import pandas as pd

    # Creating storage lists for first dataframe
    attempts_results = []
    attempts_datetime = []
    attempts_keys = []

    # Creating storage lists for second dataframe
    attempts_dates = []
    attempts_date_count = []
    nb_attempts_per_question = []

    success = []
    success_dates = []
    success_date_count = []

    failure = []
    failure_dates = []
    failure_date_count = []

    # ___________________________________________________________INITIAL PROCESSING OF ATTEMPTS_LOG

    selected_keys = []

    for i in keylst:
        word = i
        if len(word.split(".")) != 2:
            word = ".".join(word.split(".")[:-1])
        if not word.split(".")[1] == '0':
            selected_keys.append(word)

    #print("selected_keys:", selected_keys)

    with open('src\Attempts_log.txt', "r") as Attempts_log:
        attempts_lst = Attempts_log.readlines()    # Pre-processing of text file

        for attempt in attempts_lst:
            for key in selected_keys:
                if str(attempt.split(" ")[0].split(".")[0])+"."+str(attempt.split(" ")[0].split(".")[1]) == key:
                    # Compare subject.topic keys selected with attempts'

                    # Append attempts keys to list attempts_keys
                    attempts_keys.append(attempt.split(" ")[0])

                    # Append attempts results to list attempts_results
                    attempts_results.append(int(attempt.split(" ")[1]))

                    # Append attempts dates to list attempts_dates and time to list attempts_time
                    attempts_datetime.append(pd.Timestamp((datetime.datetime.strptime(
                        attempt.split(" ")[2].replace(".", " ").replace("\n", ""), '%Y-%m-%d %H:%M:%S'))))

            # ___________________________________________________________DETAILED PROCESSING OF ATTEMPTS_LOG

                    # Append attempts dates to list attempts_dates
                    attempts_dates.append(pd.Timestamp(datetime.datetime.strptime(
                        attempt.split(" ")[2].split(".")[0], '%Y-%m-%d')))

                    # If success, append attempt to success and success date to success_date
                    if int(attempt.split(" ")[1]) == 1:
                        success.append(attempt)
                        success_dates.append(datetime.datetime.strptime(attempt.split(" ")[2].split(".")[0], '%Y-%m-%d'))

                    # If failure, append attempt to failure and failure date to failure_date
                    elif int(attempt.split(" ")[1]) == 0:
                        failure.append(attempt)
                        failure_dates.append(datetime.datetime.strptime(attempt.split(" ")[2].split(".")[0], '%Y-%m-%d'))

                    break

        # ---------------------------List number of attempts per date
        for date in attempts_dates:
            count = 0
            for date_check in attempts_dates:
                if date == date_check:
                    count += 1
            attempts_date_count.append(count)

        # ---------------------------List number of success per date
        for date in attempts_dates:
            count = 0
            for date_check in success_dates:
                if date == date_check:
                    count += 1
            success_date_count.append(count)

        # ---------------------------List number of failure per date
        for date in attempts_dates:
            count = 0
            for date_check in failure_dates:
                if date == date_check:
                    count += 1
            failure_date_count.append(count)

        # ---------------------------List number of times a question was taken

        for i in range(len(attempts_keys)):
            key_count = 0
            for key in attempts_keys:
                if attempts_keys[i] == key:
                    key_count += 1
            nb_attempts_per_question.append(key_count)

    # ___________________________________________________________CREATION OF PANDAS DATAFRAMES

        data = {"Key": attempts_keys,
                "Result": attempts_results,
                "Date and time": attempts_datetime}
        df1 = pd.DataFrame(data)

        data = {"Date": attempts_dates,
                "Total nb Attempts": attempts_date_count,
                "Successes": success_date_count,
                "Failures": failure_date_count}
        df2 = pd.DataFrame(data)

        df = df2

        df = df.drop_duplicates(subset='Date', keep="last")     # Remove repeated dates
        df = df.reset_index(drop=True)                          # Reset index

        return df, df1
