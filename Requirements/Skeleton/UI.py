# This is the main file for interacting with the user and it imports functions from the Database code
# to run the backend and the Exam generator code to handle the that part.

from Database import *
from Examgen import *

#\\TODO: Add a first run explanation of the program
#\\TODO: Create subjects and topics and questions
#\\TODO: Add more options for making exam based on a specific topic and one or more topics or just the whole subject
#\\TODO: Add more options for seeing statistics, one question, one specific exam, topic statistics, subject statistics.

print("Greetings to Acumen! Increasing your exam grades since 2018!")
print("This program allows you to do this and that and the other.")

# Part of this main menu is always seen in the GUI as opposed to being asked all the time in console UI.
# This function simply asks the user which option he would like to do and returns the option selected.
#
def main_menu():
    print("""\n Please select an option and input its corresponding option
Press 1 to view your subjects, topics and questions
Press 2 to add a new subject 
Press 3 to add a new topic
Press 4 to add a new question
Press 5 to make an exam
Press 6 to view your statistics
Press 7 to delete subjects, topics or questions
Press 8 to quit the program
""")
    option = input("What would you like to do?\n")
    return option

# Function: Subjects, Topics and Questions (stq). Happens if you choose option 2 or further down option 5 or 6
# My implementation of this hierarchy is as follows:
# I have a list [ ] which contains subjects as indexes [Subject1, Subject2, etc]
# I have a second list which contains topics within a list [[Topic1, Topic2, etc], [Topic1, Topic2, etc], [etc]]
# I have a third list which contains questions within two lists [[[Question1, Question2, etc]], [[ditto]], [[etc]]]
# A fourth list which contains question details within three lists:
# [[[[Answer, Date created, boolean(True correct,False incorrect), date answered, boolean, date ans, etc ]]], [[[etc]]]]
#
def stq(Subjects):
    print('wip')
    #return ''

# This will implement what SRC(exam generation and statistics) has made
# It is considered done when it can make an exam based on a specific topic
# and one or more topics or the whole subject entirely.

def exam():
    print("wip")

# This function is used in certain sensitive places such as deletion.
# This is to make sure the user doesn't make any accidental mistakes.
def certain(action, object):
    certainty = input("\nAre you sure you want to {} {}".format(action, object))
    return certainty

# Function: Continue(cont) Basically asks the user if he or she wants to go back to the main menu or quit the program.
#
def cont():
    decision = input("\nPress any key to return to main menu, or 'n' to quit ")
    return decision


running = False
while running:
    # Welcome
    numberoftasks, tasks, tasksplain = readcurrent()
    Welcome = "Hello you have %s tasks pending!" % (str(numberoftasks))
    print(Welcome)
    Action = actions()

    # Press 1 to view your subjects, topics and questions
    if Action == '1':
        print("\nYour current Subjects are:")
        for x in tasks:
            print(x)
        decision = cont()
        if decision == 'n':
            running = False

    # Press 2 to add a new subject
    elif Action == '2':
        task = input("What would you like your subject to be?\n")
        addtask(task)
        print('Subject added succesfully!')
        print('These are your current Subjects now:\n')
        numberoftasks, tasks, tasksplain = readcurrent()
        for x in tasks:
            print(x)
        decision = cont()
        if decision == 'n':
            running = False

    # Press 3 to add a new topic
    elif Action == '3':
        task = input("What would you like the task to be?\n")
        addtask(task)
        print('task added succesfully!')
        print('These are your current tasks now:\n')
        numberoftasks, tasks, tasksplain = readcurrent()
        for x in tasks:
            print(x)
        decision = cont()
        if decision == 'n':
            running = False
    # Press 4 to add a new question
    elif Action == '4':
        task = input("What would you like the task to be?\n")
        addtask(task)
        print('task added succesfully!')
        print('These are your current tasks now:\n')
        numberoftasks, tasks, tasksplain = readcurrent()
        for x in tasks:
            print(x)
        decision = cont()
        if decision == 'n':
            running = False
    # Press 5 to make an exam
    # Press 6 to view your statistics
    # Press 7 to delete subjects, topics or questions
    # Press 8 to quit the program

    # Press 5 to change an already made task
    elif Action == '5':
        print("wip")

    # Press 6 to delete a task
    elif Action == '6':
        print("\nYour current tasks are:")
        numberoftasks, tasks, tasksplain = readcurrent()
        for x in tasks:
            print(x)
        tasknumber = int(input("Which task number would you like to delete?\n")) - 1
        if tasknumber >= 0 and tasknumber <= numberoftasks:
            task = tasks[tasknumber]
            deletetask(tasknumber)
            print("Task deleted successfully")
        else:
            print("That was not a valid number, please try again later")

    else:
        print("Please enter a number between 1 and 4 ")

# Base path is the user looks at tasks pending
# Alternate path is the user looks at tasks completed in the past

print("Thanks for using me!")
