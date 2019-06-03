#test
# def test():
#     print("Hello world!")
#     return

# This database python code allows interaction with text files Completed_tasks and Current_tasks
# It consists of 5 functions:
# 1. Read Current tasks
# 2. Write to current tasks
# 3. Read Completed tasks
# 4. Write to completed tasks
# 5. Delete a task from current tasks
# 6. Change a current task


# 1. Reads files
# Files are opened and put into respective texts
# Everything in these files assume this special character is not used ~
# Subjects text is split by newlines(a newline per subject), it contains in each index a subject
# Subjects can be selected easily by writing the correct index, i.e. first subject is subjects[0].
#
# Topics text is split by newlines(per subject) and then commas(topics in subject).
# Topics are in a list within a list. Topics in the first subject are found using topics[0].
# Second topic of third subject is found using topics[2][1]
#
# Questions text is split by newlines(per subject), commas(per topic) and then @(per question in a topic in a subject).
# Third question of second topic of first subject is then questions[0][1][2]
#
# Questiondetails split: newlines(per subject), commas(per topic), @(per question) and then $(per question detail).
# Question details are as follows:
# Answer(to the question)$Date created$boolean(True correct,False incorrect)$date answered$boolean$dateans$etc
# After date created a lot of

def readfiles():
    subjects = open("Database/Subjects.txt")
    topics = open("Database/Topics.txt")
    questions = open("Database/Questions.txt")
    questiondetails = open("Database/Questiondetails.txt")
    subjectstext= subjects.read()
    topicstext = topics.read()
    questionstext = questions.read()
    questiondetailstext = questiondetails.read()
    subjects.close()
    topics.close()
    questions.close()
    questiondetails.close()

    noemptylines = []
    currentsplit = currentlines.split('\n')
    i = 0
    while i < len(currentsplit):  # prevent empty lines from entering tasks
        if currentsplit[i] != '':
            noemptylines.append(currentsplit[i])
        i = i + 1

    lineswithnumbers = []
    i = 0
    for x in noemptylines:  # adds numbers to tasks
        x = str(i+1) + ". " + x
        lineswithnumbers.append(x)
        i += 1
    return i, lineswithnumbers, noemptylines

# 2. Write to current tasks
def addtask(task):
    current = open("Files/Current_tasks.txt", 'a')
    current.write('\n' + str(task))
    current.close()

# 3. Read Completed tasks
def readcompleted():
    current = open("Files/Completed_tasks.txt")
    currentlines = current.read()
    current.close()
    currentsplit = currentlines.split('\n')
    lineswithnumbers = []
    i = 0
    for x in currentsplit:
        x = str(i+1) + ". " + x
        lineswithnumbers.append(x)
        i += 1
    # I make sure it only prints the last ten at the UI
    return i, lineswithnumbers

# 4. Write to completed tasks
def addcompleted(completedtask):
    completed = open("Files/Completed_tasks.txt", 'a')
    completed.write('\n' + completedtask)
    completed.close()

# 5. Delete a task from current tasks
def deletetask(tasknumber):
    # first read the file
    numberoftasks, tasks, tasksplain = readcurrent()
    i = 0
    updatedtasks = []
    # Add all tasks except task that was asked to be deleted
    while i < numberoftasks:
        if i != tasknumber and tasksplain[i] != '':
            updatedtasks.append(tasksplain[i])
        i = i + 1
    current = open("Files/Current_tasks.txt", 'w')
    for x in updatedtasks:
        current.write(str(x) + '\n')
    current.close()

