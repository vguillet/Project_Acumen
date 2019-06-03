import tkinter as tk
from tkinter import N,S,E,W
import sys
#from PIL import Image, ImageTk


subjectList = [ "Maths",
                "Physics"]
topicList   = {"Maths":["Arithmetic","Logarithms"],
               "Physics":["Newtonian Mechanics","Electro-Magnetism"]}

class ListBoxes(tk.Frame):

    def __init__(self, master, subdims, subcoors, topdims, topcoors, subLB=True, topLB=True, topbind=None):
        """
        Listbox Class Initializer
        :param master: main window
        :param subdims: Subject Listbox Dimensions (must be list or tuple with 2 items)
        :param subcoors: Subject Listbox grid coordinates (must be list or tuple with 2 items)
        :param topdims: Topic Listbox Dimensions (must be list or tuple with 2 items)
        :param topcoors: Topic Listbox grid coordinates (must be list or tuple with 2 items)
        :param subLB: Boolean variable, True shows subjects Listbox
        :param topLB: Boolean Variable, True shows topics Listbox
        """
        self.master = master
        self.currentvalue = []

        if subLB == True:

            self.subjects   = tk.Listbox(self.master, width=subdims[0], height=subdims[1])

            for subject in subjectList:
                self.subjects.insert(tk.END, subject)

            self.subjects.bind('<<ListboxSelect>>', self.onselect)
            self.subjects.grid(row=subcoors[0], column=subcoors[1], sticky=N + S + E + W)

        if topLB == True:

            self.topics     = tk.Listbox(self.master, width=topdims[0], height=topdims[1])

            for topic in topicList[subjectList[0]]:
                self.topics.insert(tk.END, topic)

            self.topics.bind('<<ListboxSelect>>', topbind)
            self.topics.grid(row=topcoors[0], column=topcoors[1], sticky=N + S + E + W)

    def getselection(self, event):
        """
        Function to obtain a listbox selection
        :param event:
        :return:
        """
        idx = event.widget.curselection()[0]
        self.currentvalue.append(idx)
        return idx

    def onselect(self, event):
        """
        Function for displaying the correct topics on selected subject in the listboxes
        :param event: Could be any event, but used for <<ListboxSelect>>
        :return: -
        """
        try:
            idx = self.getselection(event)
            for i in range(len(topicList[subjectList[idx]])):
                self.topics.delete(i, tk.END)
            subject = subjectList[idx]
            for topic in topicList[subject]:
                self.topics.insert(tk.END, topic)

        except (IndexError, AttributeError):
            pass


class DropdownMenu(ListBoxes):

    def __init__(self, master):
        self.master = master

        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        fileMenu = tk.Menu(menubar, tearoff=0)
        fileMenu.add_command(label="Settings", command=None)
        fileMenu.add_command(label="Exit", command=self.programExit)  # Should be at the bottom
        menubar.add_cascade(label="File", menu=fileMenu)

        editMenu = tk.Menu(menubar, tearoff=0)
        editMenu.add_command(label="Modify Topics", command=self.topicEdit)
        editMenu.add_command(label="Modify Subjects", command=self.subjectEdit)
        menubar.add_cascade(label="Edit", menu=editMenu)

        toolMenu = tk.Menu(menubar, tearoff=0)
        toolMenu.add_command(label="Show Statistics")
        menubar.add_cascade(label="Tools", menu=toolMenu)

        helpMenu = tk.Menu(menubar, tearoff=0)
        helpMenu.add_command(label="About Acumen", command=self.infoWindow)
        menubar.add_cascade(label="Help", menu=helpMenu)

        self.currentValue = [0]


    def subjectEdit(self):
        """
        Helper function for the edit menu in the dropdown.
        Allows editing of subjects enrolled for
        :return: -
        """
        self.editSub = tk.Toplevel(self.master)
        self.editSub.transient(self.master)
        self.editSub.title('Subject Modification')

        lbFrame = tk.Frame(self.editSub)
        btFrame = tk.Frame(self.editSub)



        self.subLabel = tk.Label(lbFrame, text="Enrolled\nSubjects:"
                                 ).grid(row=0, column=0, sticky=N + E + W)

        self.addButton = tk.Button(btFrame, text="Add\nTopic", height=2, command=self.addSub
                                   ).grid(row=1, column=0, sticky=N + E + W)
        self.delButton = tk.Button(btFrame, text="Delete", height=2, command=None
                                   ).grid(row=2, column=0, sticky=N + E + W)
        self.renameButton = tk.Button(btFrame, text="Rename", height=2, command=None
                                      ).grid(row=3, column=0, sticky=N + E + W)

        self.emptyLabel = tk.Label(btFrame, text='', height=2
                                   ).grid(row=0, column=0, sticky=N + E + S + W)

        self.ListBoxClass = ListBoxes(lbFrame, (15, 7), (1, 0), (0, 0), (0, 0), topLB=False, topbind=None)

        lbFrame.grid(row=0, column=0, sticky=W + N)
        btFrame.grid(row=0, column=1, sticky=N)

    def addSub(self):
        """
        Helper function for adding subjects in the edit menu
        :return:
        """

        addNew = tk.Toplevel(self.editSub)
        addNew.transient(self.editSub)
        addNew.title("Add Subjects")

        def repopulateLB(nameVar):
            name = nameVar.get()
            subjectList.append(name)
            topicList[name] = []
            for i in range(len(subjectList)):
                self.ListBoxClass.subjects.delete(i, tk.END)

            for i in range(len(subjectList)):
                self.ListBoxClass.subjects.insert(tk.END, subjectList[i])

            tk.Tk.update(self.master)
            tk.Tk.update_idletasks(self.master)

            addNew.withdraw()

        subjectName = tk.StringVar()
        subLabel = tk.Label(addNew, text="Subject Name: "
                            ).grid(row=0, column=0)
        entryBox = tk.Entry(addNew, textvariable=subjectName
                            ).grid(row=0, column=1)
        enterButton = tk.Button(addNew, text="Enter", command=lambda: repopulateLB(subjectName)
                                ).grid(row=0, column=2)


    def topicEdit(self):
        """
        Helper function for the edit menu in the dropdown.
        Allows editing of topics enrolled for
        :return: -
        """

        self.editTop = tk.Toplevel(self.master)
        self.editTop.transient(self.master)
        self.editTop.title('Topic Modification')

        lbFrame = tk.Frame(self.editTop)
        cbFrame = tk.Frame(self.editTop)
        btFrame = tk.Frame(self.editTop)

        self.ListBoxClass = ListBoxes(lbFrame, (0, 0), (0,0),(20, 7), (1,1), subLB=False, topbind=self.topicReturn)

        self.radioButtonDict       = {}

        self.subLabel  = tk.Label(cbFrame, text="Enrolled\nSubjects:"
                                  ).grid(row=0, column=0, sticky=N+E+W)
        self.topLabel  = tk.Label(lbFrame, text="Enrolled\nTopics:"
                                  ).grid(row=0, column=1, sticky=N+S+E+W)
        self.addButton = tk.Button(btFrame, text="Add\nTopic", height=2, command=self.AddTopic
                                   ).grid(row=1, column=0, sticky=N+E+W)
        self.delButton = tk.Button(btFrame, text="Delete", height=2, command=self.DelTopic
                                   ).grid(row=2, column=0, sticky=N+E+W)
        self.renameButton = tk.Button(btFrame, text="Rename", height=2, command=self.renameTopic
                                      ).grid(row=3, column=0, sticky=N+E+W)
        self.emptyLabel = tk.Label(btFrame, text='', height=2
                                   ).grid(row=0, column=0, sticky=N+E+S+W)

        self.subjectsRadioButtons(cbFrame)

        cbFrame.grid(row=0, column=0, sticky=W+N)
        lbFrame.grid(row=0, column=1, sticky=N)
        btFrame.grid(row=0, column=2, sticky=N)

    def subjectsRadioButtons(self, frame):
        """
        Helper function to create radiobuttons for the topic edit window
        :param frame: frame in which the radiobuttons need to be displayed
        :return: -
        """

        def radioButtonControl(variable):
            """
            Function to display topics in the listbox corresponding
            to the radiobutton subject selection
            :param variable: IntVar of the radiobutton list
            :return: -
            """
            idx = variable.get()
            subname     = subjectList[idx]
            topnamelst  = topicList[subname]

            self.ListBoxClass.subject = subjectList[idx]

            for i in range(len(topicList[subjectList[idx]])):
                self.ListBoxClass.topics.delete(i, tk.END)

            for topic in topicList[self.ListBoxClass.subject]:
                self.ListBoxClass.topics.insert(tk.END, topic)

        self.radioButtonDict = {}
        self.radioButtonVar = tk.IntVar()

        for i in range(len(subjectList)):
            self.radioButtonDict['Button_{0}'.format(i + 1)] = tk.Radiobutton(frame, text=subjectList[i],
                                                                              variable=self.radioButtonVar, value=i,
                                                                              command=lambda: radioButtonControl(
                                                                                  self.radioButtonVar), indicatoron=1
                                                                              ).grid(row=i + 1, column=0, sticky=N + W)

    def renameTopic(self):
        """
        Function to rename a selected topic
        :return:
        """
        renameWin = tk.Toplevel(self.editTop)
        renameWin.transient(self.editTop)
        renameWin.title("Rename Topic")

        subidx = self.radioButtonVar.get()
        subname = subjectList[subidx]
        topicidx = self.currentValue[-1]

        def enterCommand(topic):

            new = self.nameVar.get()
            old = topicList[subname][topic]

            topicList[subname][topic] = new

            for i in range(len(topicList[subname])):
                self.ListBoxClass.topics.delete(i, tk.END)
            for j in topicList[subname]:
                self.ListBoxClass.topics.insert(tk.END, j)

            renameWin.withdraw()


        self.nameVar = tk.StringVar()
        oldNameIndicator    = tk.Label(renameWin, text="Old Name:  "
                                       ).grid(row=0, column=0, sticky=E)
        oldName             = tk.Label(renameWin, text=topicList[subname][topicidx]
                                       ).grid(row=0, column=1,sticky=W)
        newNameIndicator    = tk.Label(renameWin, text="New Name:  "
                                       ).grid(row=1, column=0, sticky=E)
        newName             = tk.Entry(renameWin, textvariable=self.nameVar
                                        ).grid(row=1, column=1, sticky=W)
        enterButton         = tk.Button(renameWin, text='Enter', command=lambda: enterCommand(topicidx)
                                        ).grid(row=2, column=1)

    def topicReturn(self, event):

        idx = event.widget.curselection()
        idx = idx[0]
        self.currentValue.append(idx)

    def DelTopic(self):
        """
        Function to delete a topic from a subject
        :return:
        """
        delWin = tk.Toplevel(self.editTop)
        delWin.transient(self.editTop)
        delWin.title("Delete Topics")
        lbFrame = tk.Frame(delWin)
        btFrame = tk.Frame(delWin)

        subidx = self.radioButtonVar.get()
        subname = subjectList[subidx]



        def yesCommand():
            topic = self.currentValue[-1]
            del topicList[subname][topic]
            delWin.withdraw()
            for i in range(len(topicList[subjectList[topic]])):
                self.ListBoxClass.topics.delete(i, tk.END)
            subject = subjectList[topic]
            for topic in topicList[subject]:
                self.ListBoxClass.topics.insert(tk.END, topic)



        def noCommand():
            delWin.withdraw()


        warningLabel = tk.Label(lbFrame, text="Are you sure you want to delete this topic?\nIt can be added again at any time."
                                ).grid(row=0, column=0)
        yesButton = tk.Button(btFrame, text="Yes", command=yesCommand
                              ).grid(row=0, column=1)
        noButton  = tk.Button(btFrame, text="No", command=noCommand
                              ).grid(row=0, column=0)

        lbFrame.grid(row=0, column=0)
        btFrame.grid(row=1, column=0)

    def AddTopic(self):
        """
        Function to add topics in the edit menu
        :return:
        """
        addNew = tk.Toplevel(self.editTop)
        addNew.transient(self.editTop)
        addNew.title("Add Topics")

        subidx = self.radioButtonVar.get()

        def addToListBox(idx, txtvar):
            subname = subjectList[idx]
            topicList[subname].append(txtvar.get())
            self.ListBoxClass.topics.insert(tk.END, txtvar.get())
            addNew.withdraw()

        topicName   = tk.StringVar()
        topLabel    = tk.Label(addNew, text="Topic Name: "
                               ).grid(row=0, column=0)
        entryBox    = tk.Entry(addNew, textvariable=topicName
                               ).grid(row=0, column=1)
        enterButton = tk.Button(addNew, text="Enter", command=lambda: addToListBox(subidx, topicName)
                                ).grid(row=0, column=2)

    def programExit(self):
        """
        Exits the program
        """
        self.DataBase.close_cb()
        sys.exit()

    def infoWindow(self):
        """
        Upon clicking the button, another window will pop up,
        showing version, credits, and other general information
        """

        infoText = "Created by:\n " \
                   "Kevin Bislip\n " \
                   "Luke de Waal\n " \
                   "Victor Guillet\n " \
                   "and Xavier O'Rourke Goby\n" \
                   "\n" \
                   "Insipred by Maurício Aniche\n" \
                   "and Felienne Hermans"

        infoWindow = tk.Toplevel(self.master, bg="white")
        infoWindow.resizable(False, False)
        infoWindow.transient(self.master)
        infoWindow.title("About Acumen")
        tk.Label(infoWindow, text="Version: 0.1", fg="black", bg="white").grid()
        tk.Label(infoWindow, text=infoText, fg="black", bg="white").grid()
        tk.Button(infoWindow, text="Close", command=infoWindow.withdraw).grid()


class Toolbar(ListBoxes):

    def __init__(self, master):

        self.master = master
        self.refresh     = tk.Button(self.master, text="Refresh",    width=15, command=None
                                     ).grid(row=0, column=2, sticky=N + S + E + W)
        self.generate    = tk.Button(self.master, text="Generate",   width=15, command=None
                                     ).grid(row=0, column=1, sticky=N + S + E + W)
        self.addnew      = tk.Button(self.master, text="Enroll in\nSubject", width=15, command=self.AddNewSubject
                                     ).grid(row=0, column=0, sticky=N+S+E+W)
        # self.delsub      = tk.Button(self.master, text="Unenroll from\nSelected Subject", width=15, command=self.DeleteSubject
        #                              ).grid(row=0, column=1, sticky=N+E+S+W)


    def AddNewSubject(self):
        """
        Parent function used for inserting new subjects and topics from scratch
        :return: -
        """

        addNew = tk.Toplevel(self.master)
        #addNew.resizable(False, False)
        addNew.transient(self.master)
        addNew.title("Enroll In New Subject")

        def TopicInsertion(window, topiclist, topicadddict, subject, amount):
            """
            Function for inserting topics into a subject, used in SubjectInsertion
            :param window: the new popup window
            :param topiclist: base variable, now defined at top of script, later in separate file
            :param topicadddict: dictionary containing topics to be added
            :param subject: variable taken from the user input containing subject name
            :param amount: amount of topics to be added to the defined subject
            :return: -
            """
            for i in range(amount):
                topiclist[subject].append(topicadddict['txtVar_{0}'.format(i+1)].get())
            window.withdraw()

        def SubjectInsertion(nameVar):
            """
            Function for inserting subjects, makes use of TopicInsertion
            :return: -
            """
            name = nameVar.get()
            subjectList.append(name)
            topicList[name] = []

            topicInsertWindow = tk.Toplevel(self.master)
            topicInsertWindow.transient(self.master)
            topicInsertWindow.title("Insert Topics")
            topicAmount = topicNumVar.get()

            topicAdditionDict = {}
            for i in range(topicAmount):
                topicAdditionDict['txtVar_{0}'.format(i+1)] = tk.StringVar()
                tk.Label(topicInsertWindow, text="Topic #{0}".format(i+1)
                         ).grid(column=0, row=i)
                tk.Entry(topicInsertWindow, textvariable=topicAdditionDict['txtVar_{0}'.format(i+1)]
                         ).grid(column=1, row=i)


            tk.Button(topicInsertWindow, text="Enter", command=lambda: TopicInsertion(topicInsertWindow, topicList, topicAdditionDict, name, topicAmount)
                      ).grid(column=1, row=i+1)


            L = ListBoxes(self.master, (15, 8), (2,0), (15, 10) , (4,0))
            addNew.withdraw()

        nameVar         = tk.StringVar()
        topicNumVar     = tk.IntVar()
        subjectName     = tk.Entry(addNew, textvariable=nameVar
                                   ).grid(column=1, row=0, ipady=0)
        topicNum        = tk.Entry(addNew, textvariable=topicNumVar
                                   ).grid(column=1, row=1)
        subinfoLabel    = tk.Label(addNew, text="Name of Subject: "
                                   ).grid(column=0, row=0)
        topinfoLabel    = tk.Label(addNew, text="Amount of topics: "
                                   ).grid(column=0,row=1)
        enterButton     = tk.Button(addNew, text="Enter", command=lambda: SubjectInsertion(nameVar)
                                    ).grid(column=1, row=2, padx=5)



class MainView(tk.Frame):
    pass



class MainApplication(tk.Frame):

    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.master     = master
        self.dropdown   = DropdownMenu(self.master)
        self.listboxes  = ListBoxes(self.master, (20, 8), (2,0), (20, 10) , (4,0))
        self.toolbar    = Toolbar(self.master)
        self.mainview   = MainView(self.master)



if __name__ == "__main__":
    root = tk.Tk()
    root.title("Acumen")
    App = MainApplication(root)
    root.mainloop()