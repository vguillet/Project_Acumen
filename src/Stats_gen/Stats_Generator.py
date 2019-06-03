"""
List of stats obtainable by the user:
-Total nb. of correct attempts /
-Total number of failed attempts /
-Ratio of correct/failed attempts /
-Graph of rate of error /
-Graph of success and failed attempts vs time /

"""


def display_dataframe(df):  # Display Pandas dataframe
    print(df, "\n")


def basic_stats(df):    # Count and output total number of answer correct/ wrong and ratio
    count_success = 0
    count_failure = 0

    for index, row in df.iterrows():
        count_success += row["Successes"]
        count_failure += row["Failures"]

    return count_success, count_failure, count_success/(count_failure or 1)


# TODO Luke - The function bellow display the dataframe contained in the variable df
def display_df_description(df):
    print("\n", df.describe())


# TODO Luke - The function bellow returns the dates formated in pyplot, so you might not want to use this one
def plot_pre_processing(df):       # Format dates for proper displaying on plot
    """
    :param df: dataframe from data_preprocessing
    :return: x - dates formatted for clean plotting with Pyplot
    """

    import numpy as np

    dates = []
    for index, row in df.iterrows():
        dates.append(row["Date"])

    dates = np.array(dates, dtype='datetime64[D]')

    return dates


# TODO Luke - The two functions bellow return y values to be used for plotting, they are always plotted against dates
def error_rate(df):        # Plot the rate of error
    """
    :param df: dataframe from data_preprocessing
    :return: y - Rate of error
    """
    ratios = []
    for index, row in df.iterrows():
        ratios.append(100*(row["Failures"]/(row["Total nb Attempts"] or 1)))

    return ratios


def fail_success(df):      # Plot the number of failed attempts and successes over time
    """
    :param df: dataframe from data_preprocessing
    :return: two ys - Failure and Successes
    """
    failures = []
    successes = []
    for index, row in df.iterrows():
        failures.append(row["Failures"])
        successes.append(row["Successes"])

    return failures, successes


# ___________________________________________________________PLOT/PRINT FUNCTIONS FOR DEV MENU

def print_basic_stats(df):
    count_failure, count_success, ratio = basic_stats(df)
    print("Number of tears shed answering questions:", count_failure+count_success)
    print("Number of questions answered successfully:", count_success)
    print("Number of questions answered wrong:", count_failure)
    print("Ratio of right to wrong:", ratio)


def plot_fail_success(df, dates):  # Plot the number of failed attempts and successes over time

    import matplotlib.pyplot as plt

    failures, successes = fail_success(df)

    plt.plot(dates, failures)
    plt.plot(dates, successes)
    plt.gcf().autofmt_xdate()
    plt.title("Number of successes and failures over time")
    plt.grid()
    plt.xlabel("Dates of attempts")
    plt.ylabel("Number of successful and failed attempts")
    plt.show()


def plot_error_rate(df, dates):  # Plot the rate of error

    import matplotlib.pyplot as plt

    ratios = error_rate(df)

    plt.plot(dates, ratios)
    plt.gcf().autofmt_xdate()
    plt.title("% Error rate")
    plt.grid()
    plt.xlabel("Dates of attempts")
    plt.ylabel("% of questions correct")
    plt.show()
