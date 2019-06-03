"""
Main process followed for stats generation
"""

# from dbinterface.final.GetExamGenData import main_exam_gen_data
import os
from src.Stats_gen.Data_preprocessing import format_attempts
from src.Stats_gen.Stats_Generator import *
from dbinterface.DBAlgoAPI import KeyCodeTools


def stats_gen_process():
    # _____________________________________________ FIRST CHECK IF ATTEMPTS_LOG NOT EMPTY

    if os.stat('./../src/Attempts_log.txt').st_size == 0:
        print("\nGenerate an exam first to be able to see performance statistics")
        print("\n___________________________________________________________________\n")
        return

    # _____________________________________________ SUB-MENU FOR SELECTING STATS GENERATION PARAMETERS

    print("\nSelect topics to generate statistics about:\n")
    print(KeyCodeTools().get_all_subject_id_name_pairs())
    subject = input("Type the name of the subject requested or 'all' if you would like statistics about everything:\n")

    if subject == "all":
        # Generate a list of all keycodes possible
        keylst = []
        for i in range(100):
            for j in range(100):
                key = str(i)+"."+str(j)
                keylst.append(key)
    else:
        print(KeyCodeTools().get_all_topics_id_name_pairs(subject))
        topic = input("Type the topic requested or 'all' if you would like statistics about everything:\n")

        if topic == "all":
            # Generate a list of all topic keycodes possible
            keylst = []
            for j in range(100):
                key = str(KeyCodeTools().get_all_subject_name_id_pairs()[subject]) + "." + str(j)
                keylst.append(key)

        else:
            keylst = str(KeyCodeTools().get_all_subject_name_id_pairs()[subject]) + "." + str(KeyCodeTools().get_all_topic_name_id_pairs(subject)[topic])
    # print("Selected keys:", keylst)
    # _____________________________________________ STATS GENERATION PROCESS

    print("\n_STATISTICS:_______________________________________________________\n")

    df, df2 = format_attempts(keylst)               # Process attempts log according to selection
    dates = plot_pre_processing(df)                 # Process and format dates for plot generation
    display_dataframe(df)                           # Display dataframe

    basic_stats(df)                                 # Display basic statistics

    # ___________________________________________________________PLOT/PRINT CALLS FOR DEV MENU
    # display_df_description(df)                      # Display df description (not yet confirmed as part of stats!!!)
    print_basic_stats(df)
    plot_error_rate(df, dates)                      # Display plot of error rate over time
    plot_fail_success(df, dates)                    # Display plot of failures and successes over time
