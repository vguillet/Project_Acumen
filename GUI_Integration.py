import tkinter as tk
import numpy as np
from tkinter import ttk
from tkinter import N,S,E,W, NO, YES, END, FIRST, LAST, DISABLED, NORMAL, TOP, BOTTOM, LEFT, RIGHT
import sys
from PIL import Image,ImageTk
import time, datetime
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk, FigureCanvasTk
from matplotlib.figure import Figure
from matplotlib import style
import matplotlib.animation as animation
import matplotlib.dates as mdates
from dbinterface.DBGUIAPI import DBManager
from src.Stats_gen.Data_preprocessing import format_attempts as dataframe
from src.Stats_gen.Stats_Generator import  display_dataframe, error_rate, fail_success
from src.Stats_gen.Stats_Generator import *
from dbinterface.DBAlgoAPI import KeyCodeTools
import pandas as pd

global subjectList, topicList
subjectList = DBManager().get_all_subjects_list()
topicList = DBManager().get_all_subject_topics_dict()


LARGE_FONT = ("Verdana", 12)
MEDIUM_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)
Large_Bold_Font = ("Verdana", 12, 'bold')
Medium_Bold_Font = ("Verdana", 10, 'bold')

F = Figure(figsize=(5, 6), dpi=100)
F.subplots_adjust(left=0.1, right=0.95, bottom=0.15, top=0.92)
Add = F.add_subplot(111)
style.use("ggplot")

def NavButtons(frame, parent, controller, text):
    """
    Function to create the buttons to navigate between pages
    :param frame: Frame in which the buttons are placed
    :param parent: parent frame
    :param controller: tk.Tk defined in base class
    :param text: Header title
    :return: None
    """
    tk.Frame.__init__(frame, parent)
    MainFrame   = tk.Frame(frame)
    HeaderFrame = tk.Frame(MainFrame)
    ButtonFrame = tk.Frame(MainFrame)

    label = ttk.Label(HeaderFrame, text=text, font=LARGE_FONT)
    label.grid(row=0, column=0, padx=10, pady=10, sticky=N+S+E+W)

    home_button = ttk.Button(ButtonFrame, text="Home Page",
                             command=lambda: controller.switch_page(StartPage))
    home_button.grid(row=0, column=0, padx=10, pady=10, sticky=N+S+E+W)

    class_button = ttk.Button(ButtonFrame, text="Class Overview",
                              command=lambda: controller.switch_page(ClassesPage))
    class_button.grid(row=0, column=1, padx=10, pady=10, sticky=N+S+E+W)

    exam_button = ttk.Button(ButtonFrame, text="Exams",
                             command=lambda: controller.switch_page(ExamPage))
    exam_button.grid(row=0, column=2, padx=10, pady=10, sticky=N+S+E+W)

    stats_button = ttk.Button(ButtonFrame, text="Statistics",
                              command=lambda: controller.switch_page(StatsPage))
    stats_button.grid(row=0, column=3, padx=10, pady=10, sticky=N+S+E+W)

    HeaderFrame.grid(row=0, column=0, sticky=N+S+E+W)

    ButtonFrame.grid(row=1, column=0, sticky=N+S+E+W)

    MainFrame.grid(row=0, column=0, sticky=N+S+E+W)


def Input_Parser(string, direction='u2d'):
    """
    Function to change database nomenclature to user interface and vice versa
    :param string: string to convert
    :param direction: 'd2u' --> Database to User ; 'u2d' --> User to Database
    :return: formatted string
    """

    if direction.lower() == 'u2d':
        out = string.replace(" ","_")

    elif direction.lower() == 'd2u':
        out = string.replace("_"," ")

    else:
        raise TypeError

    return out


def TreeView(frame, version='full', **kwargs):
    """
    Function to create subject Treeviews
    :param frame: Frame in which to place the treeview
    :param version: if full, it gets all available items, if not, it gets a certain set of items
    :param kwargs: -
    :return: Treeview and scrollbar objects
    """

    style = ttk.Style()
    style.configure('Treeview', rowheight=30)

    scrollbar = tk.Scrollbar(frame)

    if version.lower() == 'full':

        tree = ttk.Treeview(frame, yscrollcommand=scrollbar.set, height=30)
        scrollbar.config(command=tree.yview_scroll)

        sub_values = []
        top_values = {}

        for i, subject in enumerate(subjectList):
            sub_t_amount = len(topicList[subject])
            sub_q_amount = 0
            sub_q_done = 0

            top_values[subject] = []
            for topic in topicList[subject]:
                df1, df2 = dataframe(KeyCodeTools().get_all_keycodes(topic))
                count_failure, count_success, ratio = basic_stats(df1)

                top_q_amount = KeyCodeTools().get_question_amount(topic)
                top_q_done = count_failure + count_success

                sub_q_amount += top_q_amount
                sub_q_done += top_q_done

                top_values[subject].append((' ', top_q_amount, top_q_done))

            sub_values.append((sub_t_amount, sub_q_amount, sub_q_done))

        namelst     = ["Name", "# Topics", "# Questions", "# Questions Done"]
        widthlst    = [250, 150, 150, 200]

        tree["columns"] = ["#{0}".format(i) for i in range(1, len(namelst))]

        for i in range(len(tree["columns"])+1):
            tree.column(f"#{i}", width=widthlst[i], minwidth=widthlst[i])
            tree.heading(f"#{i}", text=namelst[i])

        Levels = {}

        i = 1
        for idx_1, subject in enumerate(subjectList):
            subject_u = Input_Parser(subject, 'd2u')
            j = 1
            Levels[subject] = tree.insert("", 'end', iid="{0}.{1}".format(i, 0), text=subject_u,
                                          values=sub_values[idx_1])
            for idx_2, topic in enumerate(topicList[subject]):
                topic_u = Input_Parser(topic, 'd2u')
                tree.insert(Levels[subject], 'end', iid="{0}.{1}".format(i, j), text=topic_u, values=top_values[subject][idx_2])
                j += 1
            i += 1

    else:

        tree = ttk.Treeview(frame, yscrollcommand=scrollbar.set, height=14)
        scrollbar.config(command=tree.yview_scroll)

        sub_values = []
        top_values = {}

        for i, subject in enumerate(subjectList):
            sub_q_done = 0

            top_values[subject] = []
            for topic in topicList[subject]:
                df1, df2 = dataframe(KeyCodeTools().get_all_keycodes(topic))
                count_failure, count_success, ratio = basic_stats(df1)

                top_q_done = count_failure + count_success

                sub_q_done += top_q_done

                top_values[subject].append((top_q_done, 0))

            sub_values.append((sub_q_done, 0))

        namelst     = ["Name", "# Questions Done", "Score"]
        widthlst    = [200, 110, 80]

        tree["columns"] = ["#{0}".format(i) for i in range(1, len(namelst))]

        for i in range(len(tree["columns"])+1):
            tree.column(f"#{i}", width=widthlst[i], minwidth=widthlst[i])
            tree.heading(f"#{i}", text=namelst[i])


        Levels = {}

        i = 1
        for idx_1, subject in enumerate(subjectList):
            subject_u = Input_Parser(subject, 'd2u')
            j = 1
            Levels[subject] = tree.insert("", 'end', iid="{0}.{1}".format(i, 0), text=subject_u,
                                          values=sub_values[idx_1])
            for idx_2, topic in enumerate(topicList[subject]):
                topic_u = Input_Parser(topic, 'd2u')
                tree.insert(Levels[subject], 'end', iid="{0}.{1}".format(i, j), text=topic_u,
                            values=top_values[subject][idx_2])
                j += 1
            i += 1

    tree.bind("<Double-1>", lambda event: print(tree.identify_column(event.x)))

    return tree, scrollbar

def treedelete(tree):
    """
    Function to delete all treeview entries
    :param tree: Tree in question
    :return: None
    """
    for i in tree.get_children():
        tree.delete(i)


def repopulate(tree, version="full"):
    """
    Repopulates the tree (using treedelete)
    :param tree: Tree in question
    :return: None
    """

    treedelete(tree)

    if version.lower() == 'full':

        sub_values = []
        top_values = {}

        for i, subject in enumerate(subjectList):
            sub_t_amount = len(topicList[subject])
            sub_q_amount = 0
            sub_q_done = 0

            top_values[subject] = []
            for topic in topicList[subject]:
                df1, df2 = dataframe(KeyCodeTools().get_all_keycodes(topic))
                count_failure, count_success, ratio = basic_stats(df1)

                top_q_amount = KeyCodeTools().get_question_amount(topic)
                top_q_done = count_failure + count_success

                sub_q_amount += top_q_amount
                sub_q_done += top_q_done

                top_values[subject].append((' ', top_q_amount, top_q_done))

            sub_values.append((sub_t_amount, sub_q_amount, sub_q_done))

        namelst     = ["Name", "# Topics", "# Questions", "# Questions Done"]
        widthlst    = [250, 150, 150, 200]

        tree["columns"] = ["#{0}".format(i) for i in range(1, len(namelst))]

        for i in range(len(tree["columns"])+1):
            tree.column(f"#{i}", width=widthlst[i], minwidth=widthlst[i])
            tree.heading(f"#{i}", text=namelst[i])

        Levels = {}

        i = 1
        for idx_1, subject in enumerate(subjectList):
            subject_u = Input_Parser(subject, 'd2u')
            j = 1
            Levels[subject] = tree.insert("", 'end', iid="{0}.{1}".format(i, 0), text=subject_u,
                                          values=sub_values[idx_1])
            for idx_2, topic in enumerate(topicList[subject]):
                topic_u = Input_Parser(topic, 'd2u')
                tree.insert(Levels[subject], 'end', iid="{0}.{1}".format(i, j), text=topic_u, values=top_values[subject][idx_2])
                j += 1
            i += 1

    else:
        sub_values = []
        top_values = {}

        for i, subject in enumerate(subjectList):
            sub_q_done = 0

            top_values[subject] = []
            for topic in topicList[subject]:
                df1, df2 = dataframe(KeyCodeTools().get_all_keycodes(topic))
                count_failure, count_success, ratio = basic_stats(df1)

                top_q_done = count_failure + count_success

                sub_q_done += top_q_done

                top_values[subject].append((top_q_done, 0))

            sub_values.append((sub_q_done, 0))

        namelst     = ["Name", "# Questions Done", "Score"]
        widthlst    = [200, 110, 80]

        tree["columns"] = ["#{0}".format(i) for i in range(1, len(namelst))]

        for i in range(len(tree["columns"])+1):
            tree.column(f"#{i}", width=widthlst[i], minwidth=widthlst[i])
            tree.heading(f"#{i}", text=namelst[i])


        Levels = {}

        i = 1
        for idx_1, subject in enumerate(subjectList):
            subject_u = Input_Parser(subject, 'd2u')
            j = 1
            Levels[subject] = tree.insert("", 'end', iid="{0}.{1}".format(i, 0), text=subject_u,
                                          values=sub_values[idx_1])
            for idx_2, topic in enumerate(topicList[subject]):
                topic_u = Input_Parser(topic, 'd2u')
                tree.insert(Levels[subject], 'end', iid="{0}.{1}".format(i, j), text=topic_u,
                            values=top_values[subject][idx_2])
                j += 1
            i += 1


def AboutAcumen(frame):

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



    infoWindow = tk.Toplevel(frame, bg="white")
    infoWindow.resizable(False, False)
    infoWindow.transient(frame)
    infoWindow.title("About Acumen")
    infoWindow.geometry("+500+500")


    tk.Label(infoWindow, text="Version: 0.1", fg="black", bg="white").grid()
    tk.Label(infoWindow, text=infoText, fg="black", bg="white").grid()
    ttk.Button(infoWindow, text="Close", command=infoWindow.withdraw).grid()


def program_exit():
    """
    Exits the program
    """
    sys.exit()


def WarningWindow(frame, text1, text2="", exit=False):

    warning = tk.Toplevel(frame, bg="white")
    warning.resizable(False, False)
    warning.transient(frame)
    warning.title("Warning")
    warning.geometry("+500+500")

    lbFrame = tk.Frame(warning)
    btFrame = tk.Frame(warning)

    tk.Label(lbFrame, text=text1, fg="black", bg="white").grid(row=0, column=0)
    if len(text2) != 0:
        tk.Label(lbFrame, text=text2, fg="black", bg="white").grid(row=1, column=0, sticky=N+E+S+W)

    if exit==False:
        ttk.Button(btFrame, text="Close", command=warning.withdraw).grid(row=0, column=0)

    elif exit==True:
        ttk.Button(btFrame, text="Yes", command=program_exit).grid(row=0, column=0)
        ttk.Button(btFrame, text="No", command=warning.withdraw).grid(row=0, column=1)

    lbFrame.grid(row=0, column=0)
    btFrame.grid(row=1, column=0)


def Update():
    """
    Function used to update frames
    :return: None
    """
    App.after(1000, Update)



class AcumenApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        """
        Initialization of base class, this is where all pages are managed
        :param args: Tkinter-required args
        :param kwargs: Tkinter-required kwargs
        """
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, default='./GUI/icons/main_icon_2.ico')
        tk.Tk.wm_title(self, "Acumen")

        self.resizable(True, True)

        self.width = 900
        self.height = 620
        self.xposition = int(self.winfo_screenwidth() / 2 - self.width / 2)
        self.yposition = int(self.winfo_screenheight() / 2 - self.height / 2)

        self.geometry("{0}x{1}+{2}+{3}".format(self.width, self.height, self.xposition, self.yposition))

        container = tk.Frame(self)
        container.grid(row=0, column=0)

        dropdown = tk.Menu(container)

        filemenu = tk.Menu(dropdown, tearoff=0)
        filemenu.add_command(label="Settings",      command=lambda: WarningWindow(container, "This Feature Has Not Been Implemented Yet", "Our Sincerest Apologies for this,\nIt will be implemented very soon"))
        filemenu.add_command(label="Exit",          command=lambda: WarningWindow(container, "Are you sure you wish to exit?", "Progress is saved automatically.", exit=True))

        helpmenu = tk.Menu(dropdown, tearoff=0)
        helpmenu.add_command(label="About Acumen",  command=lambda: AboutAcumen(container))

        dropdown.add_cascade(label="File", menu=filemenu)
        dropdown.add_cascade(label="Help", menu=helpmenu)
        tk.Tk.config(self, menu=dropdown)

        self.frames     = {}
        self.FrameList  = (StartPage,   ClassesPage,    ExamPage,   StatsPage)
        self.LabelList  = ("Home Page", "Class Overview", "Exams", "Statistics")

        for F in self.FrameList:

            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.switch_page(StartPage)



    def switch_page(self, container):
        """
        Function used to switch pages
        :param container: frame in which to place new page
        :return: None
        """

        frame = self.frames[container]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        """
        Initialization of Start Page, this is the page that is shown first when started up
        :param parent: parent frame
        :param controller: tk.Tk controller
        """
        NavButtons(self, parent, controller, text="Home Page")

        welcomegrid = tk.Frame(self)
        picturegrid = tk.Frame(self)

        photo = Image.open('./GUI/icons/WelcomeImg.png')
        photo = photo.resize((400, 325), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(photo)
        lb = tk.Label(picturegrid, image=photo)
        lb.image = photo
        lb.grid(row=0, column=0)

        photo = Image.open('./GUI/icons/maths_revision.png')
        photo = photo.resize((400, 330), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(photo)
        lb = tk.Label(picturegrid, image=photo)
        lb.image = photo
        lb.grid(row=1, column=0)

        photo = Image.open('./GUI/icons/geography.png')
        photo = photo.resize((460, 330), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(photo)
        lb = tk.Label(welcomegrid, image=photo)
        lb.image = photo
        lb.grid(row=1, column=0)

        text = tk.Text(welcomegrid, height=20, width=58)
        scroll = tk.Scrollbar(welcomegrid, command=text.yview)
        text.configure(yscrollcommand=scroll.set)
        text.tag_configure('bold_italics', font=('Arial', 12, 'bold', 'italic'))
        text.tag_configure('big', font=('Verdana', 20, 'bold'))
        text.tag_configure('color', foreground='#476042',
                            font=('Tempus Sans ITC', 12, 'bold'))
        text.tag_bind('follow', '<1>', lambda e, t=text: t.insert(END, "Not now, maybe later!"))
        text.insert(END, '\n\tAcumen\n', 'big')
        quote = "\n\n\tNoun\n" \
                "\t'The ability to make good judgements \n\tand take quick decisions.'\n" \
                "\tOrigin: Late 16th century: from Latin,\n\t‘sharpness, point’, from acuere ‘sharpen’." \
                ""
        text.insert(END, quote, 'color')
        text.config(state=DISABLED)
        text.grid(row=0, column=0)
        scroll.grid(row=0, column=1, sticky=N+S)

        picturegrid.grid(row=2, column=0)
        welcomegrid.grid(row=2, column=1)
        # welcomegrid.grid_columnconfigure(0, weight=1)
        # welcomegrid.grid_columnconfigure(1, weight=1)
        # welcomegrid.grid_columnconfigure(2, weight=1)
        # welcomegrid.grid_rowconfigure(0, weight=1)


class ClassesPage(tk.Frame):

    def __init__(self, parent, controller):
        """
        Class Page initialization
        :param parent: parent frame
        :param controller: tk.Tk controller
        """

        NavButtons(self, parent, controller, text="Classes")

        self.treeframe = tk.Frame(self, width=740, height=600)
        self.tree, scrollbar = TreeView(self.treeframe)

        btFrame = tk.Frame(self)
        self.tree.bind("<<TreeviewSelect>>", lambda event: self.itemselection(event))

        buttonsx, buttonsy = (10,10)

        global item_selection
        item_selection = []

        global edit_selection
        edit_selection = []

        photo = Image.open('./GUI/icons/abstract/plus_green.png')
        photo = photo.resize((40, 32), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(photo)
        addsub_btn = ttk.Button(btFrame, text="Add", width=buttonsy, image=photo, compound=TOP,
                               command=self.AddWindow)
        addsub_btn.image = photo

        photo = Image.open('./GUI/icons/abstract/minus_red.png')
        photo = photo.resize((40, 32), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(photo)
        delsub_btn = ttk.Button(btFrame, text="Remove", width=buttonsy, image=photo, compound=TOP,
                                command=self.RemoveWindow)
        delsub_btn.image = photo

        photo = Image.open('./GUI/icons/office/pencil_green.png')
        photo = photo.resize((40, 32), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(photo)
        editsub_btn = ttk.Button(btFrame, text="Edit", width=buttonsy, image=photo, compound=TOP,
                               command=self.EditWindow)
        editsub_btn.image = photo

        photo = Image.open('./GUI/icons/actions/repeat_green.png')
        photo = photo.resize((40, 32), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(photo)
        refresh_btn = ttk.Button(btFrame, text="Refresh", width=buttonsy, image=photo, compound=TOP,
                                command= lambda: repopulate(self.tree))
        refresh_btn.image = photo

        addsub_btn.grid(row=0, column=1, sticky=N + W)
        delsub_btn.grid(row=1, column=1, sticky=N + W)
        editsub_btn.grid(row=2, column=1, sticky=N + W)
        refresh_btn.grid(row=3, column=1, sticky=N + W)

        btFrame.grid(row=2, column=2, sticky=N + W)

        self.treeframe.pack_propagate(0)
        self.tree.pack(side='left', fill="both")
        scrollbar.pack(side='right')
        self.treeframe.grid(row=2, column=0, sticky=N + E + W)


    def itemselection(self, event):
        """
        Function to return which items are selected in the treeview
        :param event: <<TreeviewSelect>>
        :return: None
        """
        global item_selection
        item_selection = self.tree.selection()

        for select in item_selection:

            if select[-1] == '0':
                children = self.tree.get_children([select])

                s = set(item_selection)
                to_append = tuple([child for child in children if child not in s])

                item_selection += to_append

        #print(item_selection)

    def EditWindow(self):
        """
        Function creates a window where the user can edit names
        :return: None
        """

        self.editwindow = tk.Toplevel(self, bg='white')
        self.editwindow.transient(self)
        self.editwindow.title("Edit Names of Subjects and Topics")

        global item_selection

        selected = []
        types    = []

        for item in item_selection:

            if item[-1] != '0':
                selected.append(KeyCodeTools().get_keycode_to_english_translation(item).split(".")[-1])
                types.append(0)

            elif item[-1] == '0':
                selected.append(subjectList[int(item.split(".")[0])-1])
                types.append(1)

        headerFrame = tk.Frame(self.editwindow, bg='white')
        entryFrame  = tk.Frame(self.editwindow, bg='white')
        btnFrame    = tk.Frame(self.editwindow, bg='white')

        entryVars   = [tk.StringVar() for i in selected]
        labels      = [tk.Label(entryFrame, text=Input_Parser(selected[i], 'd2u')+":", bg='white') for i in range(len(selected))]
        entries     = [tk.Entry(entryFrame, textvariable=entryVars[i], bg='white') for i in range(len(selected))]

        rows = 8
        cols = int(len(selected)/rows)
        rem  = len(selected)%rows

        if cols < 1:
            cols = 1
            rem  = 0
            rows = len(selected)

        counter = 0
        for i in np.arange(0, cols, 1)*2:
            for j in range(rows):
                labels[counter].grid(row=j, column=i, sticky=N+W)
                entries[counter].grid(row=j, column=i+1, sticky=N+W)

                counter+= 1

        for r in range(rem):
            labels[counter].grid(row=r, column=i+2, sticky=N+W)
            entries[counter].grid(row=r, column=i+3, sticky=N+W)

            counter += 1

        headerLbl = tk.Label(headerFrame, text="Enter New Names and Press Confirm", font=Large_Bold_Font, bg='white')
        emptyLbl_1  = tk.Label(headerFrame, text="\n", bg='white')
        headerLbl.grid(row=0, column=0, sticky=N+W)
        emptyLbl_1.grid(row=1, column=0)

        cancelBtn = ttk.Button(btnFrame, text="Cancel", command=self.editwindow.withdraw)
        confirmBtn = ttk.Button(btnFrame, text='Confirm', command=lambda: self.EditConfirm(entryVars, selected, types))
        emptyLbl_2 = tk.Label(headerFrame, text="\n", bg='white')

        emptyLbl_2.grid(row=0, column=0)
        confirmBtn.grid(row=1, column=0)
        cancelBtn.grid(row=1, column=1)

        headerFrame.grid(row=0, column=0)
        entryFrame.grid(row=1, column=0)
        btnFrame.grid(row=2, column=0)

    def EditConfirm(self, varlst, selectedlst, typelst):
        """
        Once the user has put in all new names, this function can be called
        :param varlst: List of stringvar variables
        :param selectedlst: list of the selected items
        :param typelst: list with 1's or 0's (1 for subjects, 0 for topics)
        :return: None
        """

        for idx, (var, select) in enumerate(zip(varlst, selectedlst)):

            name = var.get()
            type = typelst[idx]

            if type == 0:
                DBManager().edit_subject_or_topic_name_attribute(Input_Parser(name, 'u2d'), current_topic_name=Input_Parser(select, 'u2d'))

            elif type == 1:
                DBManager().edit_subject_or_topic_name_attribute(Input_Parser(name, 'u2d'), current_subject_name=Input_Parser(select, 'u2d'))

        global subjectList, topicList
        subjectList = DBManager().get_all_subjects_list()
        topicList = DBManager().get_all_subject_topics_dict()

        self.editwindow.withdraw()


    def RemoveWindow(self):
        """
        Window that is popped up to warn the user (s)he is about to delete the selected items
        :return: None
        """

        self.removewindow = tk.Toplevel(self, bg="white")
        # self.addwindow.resizable(False, False)
        self.removewindow.transient(self)
        self.removewindow.title("Remove Topics and Subjects")
        self.removewindow.geometry("+500+500")

        global item_selection

        btnFrame = tk.Frame(self.removewindow)

        warninglabel = tk.Label(self.removewindow, text="Are you sure you wish to\ndelete these subjects/topics?", background='white')
        confirmbtn = ttk.Button(btnFrame, text="Yes", command=lambda: self.removeconfirm(item_selection))
        cancelbtn = ttk.Button(btnFrame, text="No", command=None)

        cancelbtn.config(command=self.removewindow.withdraw)

        warninglabel.grid(row=0, column=0)
        confirmbtn.grid(row=0, column=0)
        cancelbtn.grid(row=0, column=1)

        btnFrame.grid(row=1, column=0)


    def removeconfirm(self, selected):
        """
        Function if user confirms (s)he wants to delete all selected items
        :param selected: list of selected items
        :return: none
        """

        global subjectList, topicList

        to_remove_subs = []
        to_remove_topics = []

        for selection in selected:
            lst = selection.split(".")
            subdigit = int(lst[0])
            topdigit = int(lst[1])

            if topdigit == 0:
                to_remove_subs.append(subdigit)

            elif topdigit != 0:
                if subdigit in to_remove_subs:
                    continue

                else:
                    to_remove_topics.append((subdigit, topdigit))

        print(to_remove_subs)

        if not len(to_remove_subs) == 0:
            for sub in to_remove_subs:
                DBManager().remove_subject_entirely_from_db(subjectList[sub-1])

        if not len(to_remove_topics) == 0:
            for sub, top in to_remove_topics:
                topic = topicList[subjectList[sub-1]][top-1]
                DBManager().remove_topic_entirely_from_db(topic)

        subjectList = DBManager().get_all_subjects_list()
        topicList = DBManager().get_all_subject_topics_dict()

        repopulate(self.tree)

        self.removewindow.withdraw()



    def AddWindow(self):
        """
        Window in which the user can add new subjects, topics or questions
        :return: None
        """
        self.addwindow = tk.Toplevel(self, bg="white")
        #self.addwindow.resizable(False, False)
        self.addwindow.transient(self)
        self.addwindow.title("Add Topics and Subjects")
        self.addwindow.geometry("+500+500")

        self.dropdownvar = tk.StringVar()
        self.dropdownvar.trace("r", self.main_comboboxselection)
        dropdown = ttk.Combobox(self.addwindow, textvariable=self.dropdownvar)
        dropdown['values'] = ['Subjects', 'Topics', 'Questions']
        dropdown.bind("<<ComboboxSelected>>", self.main_comboboxselection)
        dropdown.current(0)

        lb1 = tk.Label(self.addwindow, text="Choose what you would like to add: ", bg="white")

        lb1.grid(row=0, column=0, sticky=N+W+S)
        dropdown.grid(row=0, column=1, sticky=N+W+S)


    def main_comboboxselection(self, *args):
        """
        Gets the users type input selection (Subject, Topic or Question)
        :param args: Tkinter-required args
        :return: None
        """
        self.selected = self.dropdownvar.get()

        for i in range(len(self.addwindow.winfo_children())):
            widget = self.addwindow.winfo_children()[i]
            if i in [0, 1]:
                continue
            else:
                widget.grid_forget()
                del self.addwindow.winfo_children()[i]

        self.add_selection(self.addwindow, self.selected)
        return

    def integer_validate(self, var, old):
        """
        Prevents wrong inputs from user when inputting an amount
        :param var: variable linked to user input
        :param old: standard value and/or old value
        :return:
        """
        new_value = var.get()
        old_value = old
        try:
            new_value == '' or int(new_value)
            old_value = new_value

        except:
            var.set(old_value)

    def enterbutton_main(self, frame, btframe, type, *args):
        """
        Enter Button command once the desired amount is given
        :param frame: Topwindow frame
        :param btframe: Frame containing Cancel and Enter buttons
        :param type: Selection made in combobox
        :param args: Amount or names
        :return:
        """
        if not type in ['Subjects', 'Topics', 'Questions']:
            raise TypeError


        if type == 'Subjects':
            print(args)
            val = int(args[0].get())

            if val <= 0:
                val = 1

            variables = [tk.StringVar() for i in range(val)]
            labels    = [tk.Label(frame, text="Subject #{0}".format(i+1), bg='white') for i in range(val)]
            entries   = [ttk.Entry(frame, textvariable=variables[i]) for i in range(val)]

            minrow = 3

            btframe.grid(row=minrow+val)
            self.en1.config(state=DISABLED)
            self.bt1.config(command=lambda: self.sub_enterbutton(variables, self.checkvar))

            for i in range(val):

                labels[i].grid(row=minrow+i, column=0, sticky=N+W)
                entries[i].grid(row=minrow+i, column=1, sticky=N+W)

        elif type == 'Topics':
            subject = args[0].get()
            val = int(args[1].get())

            if val <= 0:
                val = 1

            self.cb1.config(state=DISABLED)
            self.en1.config(state=DISABLED)

            variables = [tk.StringVar() for i in range(val)]
            labels    = [tk.Label(frame, text="Topic #{0}".format(i+1), bg='white') for i in range(val)]
            entries   = [ttk.Entry(frame, textvariable=variables[i]) for i in range(val)]

            minrow = 4

            btframe.grid(row=minrow + val)
            self.bt1.config(command=lambda: self.top_enterbutton(variables, subject))

            for i in range(val):
                labels[i].grid(row=minrow + i, column=0, sticky=N + W)
                entries[i].grid(row=minrow + i, column=1, sticky=N + W)

        elif type == 'Questions':
            subject = args[0].get()
            topic = args[1].get()
            val = int(args[2].get())

            if val <= 0:
                val = 1

            elif val >= 20:
                val = 20

            self.cb1.config(state=DISABLED)
            self.cb2.config(state=DISABLED)
            self.en1.config(state=DISABLED)

            minrow=5

            qframe = tk.Frame(frame)

            Qvariables = [tk.StringVar() for i in range(val)]
            Qlabels    = [tk.Label(qframe, text="Question #{0}".format(i+1), bg='white') for i in range(val)]
            Qentries   = [ttk.Entry(qframe, textvariable=Qvariables[i]) for i in range(val)]

            Avariables = [tk.StringVar() for i in range(val)]
            Alabels    = [tk.Label(qframe, text="Answer #{0}".format(i+1), bg='white') for i in range(val)]
            Aentries   = [ttk.Entry(qframe, textvariable=Avariables[i]) for i in range(val)]

            if val <= 10:
                for i in range(val):
                    Qlabels[i].grid(row=i, column=0)
                    Qentries[i].grid(row=i, column=1)

                    Alabels[i].grid(row=i, column=2)
                    Aentries[i].grid(row=i, column=3)

            elif val > 10:
                mod10 = val%10
                mod2  = mod10%2

                if mod2 == 1:
                    len1 = round(val/2)
                    len2 = int(val/2)

                    for i in range(len1):
                        Qlabels[i].grid(row=i, column=0)
                        Qentries[i].grid(row= i, column=1)

                        Alabels[i].grid(row=i, column=2)
                        Aentries[i].grid(row=i, column=3)

                    i = 0
                    for j in range(len1, len1+len2):
                        Qlabels[j].grid(row=i, column=4)
                        Qentries[j].grid(row=i, column=5)

                        Alabels[j].grid(row=i, column=6)
                        Aentries[j].grid(row=i, column=7)

                        i += 1

                elif mod2 == 0:
                    len1 = round(val/2)
                    len2 = int(val/2)

                    for i in range(len1):
                        Qlabels[i].grid(row=i, column=0)
                        Qentries[i].grid(row= i, column=1)

                        Alabels[i].grid(row=i, column=2)
                        Aentries[i].grid(row=i, column=3)

                    i = 0
                    for j in range(len1, len1+len2):
                        Qlabels[j].grid(row=i, column=4)
                        Qentries[j].grid(row=i, column=5)

                        Alabels[j].grid(row=i, column=6)
                        Aentries[j].grid(row=i, column=7)

                        i += 1

            self.bt1.config(command=lambda: self.Q_enterbutton(Qvariables, Avariables, topic, subject))

            emptylabel = tk.Label(btframe, bg='white')
            emptylabel.grid(row=0, columnspan=3, sticky=N+S+E+W)
            qframe.grid(row=minrow, columnspan=3)
            btframe.grid(row=minrow + 1, sticky=N+W)


    def add_selection(self, frame, selected):
        """
        Once the type of new input is chosen (Sub, Top or Q) this function is fired and allows the user
        to input the next details for the program to add
        :param frame: Frame in which to add the new widgets
        :param selected: Subject, Topic or Question
        :return: None
        """
        if selected == "Subjects":
            amountvar = tk.StringVar()
            amountvar.trace('w', lambda nm, idx, mode, var=amountvar: self.integer_validate(var, ''))

            self.checkvar = tk.BooleanVar()
            self.checkvar.set(False)

            btFrame = tk.Frame(frame)

            lb1      = tk.Label(frame, text="# of Subjects: ", bg='white')
            self.en1 = tk.Entry(frame, textvariable=amountvar)
            self.bt1 = ttk.Button(btFrame, text="Enter", command=lambda: self.enterbutton_main(frame, btFrame, 'Subjects', amountvar))
            self.bt2 = ttk.Button(btFrame, text="Cancel", command=lambda: frame.withdraw())
            self.check = ttk.Checkbutton(frame, text="Add Topics?", variable=self.checkvar, offvalue=0, onvalue=1)


            btFrame.grid(row=3, column=0)
            lb1.grid(row=1, column=0, sticky=N + W)
            self.en1.grid(row=1, column=1, sticky=N + W)
            self.check.grid(row=3, column=1, sticky=N+E+W)
            self.bt1.grid(row=0, column=1, sticky=W)
            self.bt2.grid(row=0, column=0, sticky=E)


        elif selected == "Topics":
            cbvar1 = tk.StringVar()
            self.cb1 = ttk.Combobox(frame, textvariable=cbvar1)
            self.cb1['values'] = [Input_Parser(subjectList[i], 'd2u') for i in range(len(subjectList))]

            amountvar = tk.StringVar()
            amountvar.trace('w', lambda nm, idx, mode, var=amountvar: self.integer_validate(var, ''))

            btFrame = tk.Frame(frame)

            lb1 = tk.Label(frame, text="Choose Subject: ", bg='white')
            lb2 = tk.Label(frame, text="# of Topics: ", bg='white')
            self.en1 = tk.Entry(frame, textvariable=amountvar)
            self.bt1 = ttk.Button(btFrame, text="Enter", command=lambda: self.enterbutton_main(frame, btFrame, 'Topics', cbvar1, amountvar))
            bt2 = ttk.Button(btFrame, text="Cancel", command=frame.withdraw)

            btFrame.grid(row=3, column=0)
            self.cb1.grid(row=1, column=1, sticky=N + W)
            lb1.grid(row=1, column=0, sticky=N + W)
            lb2.grid(row=2, column=0, sticky=N + W)
            self.en1.grid(row=2, column=1, sticky=N + W)
            self.bt1.grid(row=0, column=1, sticky=W)
            bt2.grid(row=0, column=0, sticky=E)


        elif selected == 'Questions':
            self.cbvar1 = tk.StringVar()
            self.cb1 = ttk.Combobox(frame, textvariable=self.cbvar1)
            self.cb1['values'] = [Input_Parser(subjectList[i], 'd2u') for i in range(len(subjectList))]
            self.cbvar1.set(0)
            self.cb1.current(0)


            self.cbvar2 = tk.StringVar()
            self.cb2 = ttk.Combobox(frame, textvariable=self.cbvar2)
            self.cb2['values'] = [Input_Parser(topic, 'd2u') for topic in topicList[self.cbvar1.get()]]
            self.cbvar2.set(Input_Parser(topicList[self.cbvar1.get()][0], 'd2u'))

            self.cb1.bind("<<ComboboxSelected>>", self.Q_comboboxselection)

            amountvar = tk.StringVar(value='20')
            amountvar.trace('w', lambda nm, idx, mode, var=amountvar: self.integer_validate(var, ''))

            btFrame = tk.Frame(frame)

            lb1 = tk.Label(frame, text="Choose Subject: ", bg='white')
            lb2 = tk.Label(frame, text="Choose Topic: ", bg='white')
            lb3 = tk.Label(frame, text="Amount of Questions:\n(Max. 20)", bg='white')
            self.en1 = tk.Entry(frame, textvariable=amountvar)
            self.bt1 = ttk.Button(btFrame, text="Enter",
                                  command=lambda: self.enterbutton_main(frame, btFrame, 'Questions',
                                                                        self.cbvar1, self.cbvar2, amountvar))
            bt2 = ttk.Button(btFrame, text="Cancel", command=frame.withdraw)

            btFrame.grid(row=4, column=0)
            self.cb1.grid(row=1, column=1, sticky=N + W)
            self.cb2.grid(row=2, column=1, sticky=N+W)
            lb1.grid(row=1, column=0, sticky=N + W)
            lb2.grid(row=2, column=0, sticky=N + W)
            lb3.grid(row=3, column=0, sticky=N+W)
            self.en1.grid(row=3, column=1, sticky=N + W)
            self.bt1.grid(row=1, column=1, sticky=W)
            bt2.grid(row=1, column=0, sticky=E)

        Update()

    def Q_comboboxselection(self, *args):
        """
        Lets the user choose what subject to add questions for
        :param args:
        :return:
        """
        self.selected = self.cbvar1.get()

        self.cb2['values'] = topicList[self.selected]

        Update()


    def Q_enterbutton(self, Qvarlist, Avarlist, topic, subject):
        """
        Once everything is filled in for adding new questions, this function ca be fired
        :param varlist: list of stringvars
        :param topic: Topic
        :param subject: Subject
        :return: None
        """
        global subjectList
        global topicList

        for Qvar, Avar in zip(Qvarlist, Avarlist):
            db_q = Input_Parser(Qvar.get(), 'u2d')
            db_a = Input_Parser(Avar.get(), 'u2d')
            DBManager().add_new_question(topic, db_q, db_a, subject)

        self.addwindow.withdraw()

        Update()


    def top_enterbutton(self, varlist, subject):
        """
        Once everything is filled in for adding new topics, this function ca be fired
        :param varlist: list of stringvars
        :param subject: subject
        :return: None
        """
        global subjectList
        global topicList

        olddict = topicList

        for var in varlist:
            db_name = Input_Parser(var.get(), 'u2d')
            DBManager().add_new_topic(db_name, subject)
            topicList[subject].append(db_name)

        self.addwindow.withdraw()

        Update()

    def sub_enterbutton(self, varlist, checkvar):
        """
        Once everything is filled in for adding new subjects, this function ca be fired
        :param varlist: list of stringvars
        :param checkvar: Boolvar for topic adding afterwards
        :return: None
        """
        global subjectList
        global topicList
        oldlist = subjectList

        for var in varlist:
            db_name = Input_Parser(var.get(), 'u2d')
            DBManager().add_new_subject(db_name)

        subjectList = DBManager().get_all_subjects_list()
        s = set(oldlist)
        newkeys = [subject for subject in subjectList if subject not in s]
        for subject in newkeys:
            topicList[subject] = []


        if checkvar.get() == True:

            for i in range(len(varlist)):
                for widget in self.addwindow.winfo_children():
                    print(str(widget))
                    widget.destroy()

                self.add_selection(self.addwindow, 'Topics')

        else:
            self.addwindow.withdraw()

        Update()


class ExamPage(tk.Frame):

    def __init__(self, parent, controller):
        """
        Initialization of the exam page
        :param parent: parent frame
        :param controller: tk.Tk controller
        """

        self.controller = controller

        NavButtons(self, parent, controller, text="Exams")

        buttonstyle = ttk.Style()
        buttonstyle.configure('Exam.TButton', font=('Verdana', 10))

        photo = Image.open('./GUI/icons/examgen.png')
        photo = photo.resize((120, 100), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(photo)
        examgen_btn = ttk.Button(self, text="Generate Exam!", width=40, image=photo, compound=TOP, style='Exam.TButton',
                                 command=self.Examgen_main)
        examgen_btn.image = photo

        infotext = tk.Text(self, height=40, width=65)
        scroll = tk.Scrollbar(self, command=infotext.yview)
        infotext.configure(yscrollcommand=scroll.set)

        #infotext.insert(END, '\n\tAcumen\n', 'big')
        quote = "How to use the Exam Generator:\n" \
                "\n" \
                "1. Make sure you added your subjects and topics.\n" \
                "2. Make sure you have a multitude of questions for \n   every topic.\n" \
                "3. Click the button to the right\n" \
                "4. Select a whole subject or some topics\n" \
                "5. Click confirm when done selecting\n" \
                "6. In the popup window select the amount of questions\n" \
                "7. Click confirm when done selecting\n" \
                "8. When finished with a question click check answer\n" \
                "9. Mark yourself fairly\n" \
                "10. Move on to the next question on the top\n" \
                "11. Click finish, then finish button and yes \n when done with exam\n"

        infotext.insert(END, quote, 'color')
        infotext.config(state=DISABLED)

        infotext.grid(row=1, column=0)
        scroll.grid(row=1, column=1, sticky=N + S)
        examgen_btn.grid(row=1, column=2, sticky=N+S+W)

    def Examgen_main(self):
        """
        Function to pop up a window where the user can select subjects and topics to be examined on
        :return: None
        """

        self.selectwindow = tk.Toplevel(self)
        self.selectwindow.transient(self)
        self.selectwindow.title("Select Your Exam Subjects and Topics")
        tk.Label(self.selectwindow, text="\n", font=LARGE_FONT).grid(row=0, column=0)
        tk.Label(self.selectwindow, text="Make a Selection: ", font=LARGE_FONT).grid(row=1, column=0)
        tk.Label(self.selectwindow, text="\n", font=LARGE_FONT).grid(row=2, column=0)

        self.checkvarsdict_topics   = {}
        self.checkvarsdict_subjects = {}

        i = 0
        j = 3
        for subject in subjectList:
            self.SingleCanvas(self.selectwindow, subject, j, i)

            i += 2

            if i % 6 == 0:
                i = 0
                j += 1
                print(j)


        confirm = ttk.Button(self.selectwindow, text="Confirm", command=self.Exam_db_init)
        cancel  = ttk.Button(self.selectwindow, text='Cancel', command=self.selectwindow.withdraw)

        confirm.grid(row=1, column=2, sticky=E)
        cancel.grid(row=1, column=4, sticky=W)


    def Exam_db_init(self):
        """
        When fired initializes the exam database and creates the appropriate questions with the user's
        selection and past performance; asks the user for the amount of questions.
        :return: None
        """

        from src.Compatibility_script import compile_data_bank

        topics = []

        for key in self.checkvarsdict_topics.keys():
            print(key)
            for idx, check in enumerate(self.checkvarsdict_topics[key]):
                if check.get() == True:
                    topics.append(topicList[key][idx])

        self.selectwindow.withdraw()

        if not len(topics) == 0:

            self.data_bank = compile_data_bank(topics)
            self.amountwindow = tk.Toplevel(self, background='white')
            self.amountwindow.transient(self)
            self.amountwindow.title("Amount of Questions")

            label_1 = tk.Label(self.amountwindow, text="Choose the amount\nof Questions",
                               font=("Verdana", 10, 'bold'), background='white')
            label_2 = tk.Label(self.amountwindow, text="(Available Questions: {0})".format(len(self.data_bank)),
                               font=("Verdana", 8), background='white')
            label_3 = tk.Label(self.amountwindow, text="Amount: ",
                               font=("Verdana", 8), background='white')
            emptylabel = tk.Label(self.amountwindow, text=" ", background='white')

            self.amountvar = tk.StringVar()
            self.amountvar.trace('w', lambda nm, idx, mode, var=self.amountvar: self.integer_validate(var, '', len(self.data_bank)))
            entry_1 = ttk.Entry(self.amountwindow, textvariable=self.amountvar)

            confirm = ttk.Button(self.amountwindow, text="Confirm", command=self.Exam_creation)
            cancel = ttk.Button(self.amountwindow, text='Cancel', command=self.amountwindow.withdraw)

            label_1.grid(row=0, column=0, sticky=N+W)
            label_2.grid(row=1, column=0, sticky=N+W)
            emptylabel.grid(row=2)
            label_3.grid(row=3, column=0, sticky=N+W)
            entry_1.grid(row=3, column=1, sticky=N+W)

            cancel.grid(row=4, column=0, sticky=N+E)
            confirm.grid(row=4, column=1, sticky=N+W)

        return


    def integer_validate(self, var, old, max):
        """
        Prevents wrong inputs from user when inputting an amount
        :param var: variable linked to user input
        :param old: standard value and/or old value
        :return:
        """
        new_value = var.get()
        old_value = old
        try:
            new_value == '' or int(new_value)
            old_value = new_value

            if int(new_value) > max:
                var.set(max)

        except Exception:
            var.set(old_value)

    @staticmethod
    def scoretreeview(frame, nb_q, Exam, progresslst):
        """
        Simple static method to create a treeview with the user's score
        :param frame: frame in which to place it
        :param nb_q: numberof items
        :param Exam: Exam object
        :param progresslst: list with the progress values
        :return: Tree Object, Scrollbar Object
        """

        style = ttk.Style()
        style.configure('Treeview', rowheight=25)

        scrollbar = tk.Scrollbar(frame)
        tree = ttk.Treeview(frame, yscrollcommand=scrollbar.set, height=12)
        scrollbar.config(command=tree.yview_scroll)

        #Qnumber ; Subject ; Topic ; Score
        tree["columns"] = ["#{0}".format(i) for i in range(1, 4)]

        tree.column("#0", width=75, stretch=NO)
        tree.column("#1", width=100, stretch=NO)
        tree.column("#2", width=135, stretch=NO)
        tree.column("#3", width=90, stretch=NO)
        tree.heading("#0", text="Question")
        tree.heading("#1", text="Subject")
        tree.heading("#2", text="Topic")
        tree.heading("#3", text="Score")

        subjects = []
        topics = []
        for i in range(nb_q):
            subject, topic = Exam.getsubtop(i)
            subjects.append(subject)
            topics.append(topic)

        progress = [0]*nb_q

        i = 0
        for score in progresslst:
            if score == None:
                progress[i] = 'Uncompleted'

            elif score == 0.0 and type(score) == float:
                progress[i] = 'Given Up'

            elif score == 0 and type(score) == int:
                progress[i] = 'Incorrect!'

            elif score == 1:
                progress[i] = 'Correct!'

            i += 1

        Levels = {}

        i = 1
        j = 0
        for subject in subjects:
            Levels[subject] = tree.insert("", END, text=f"Q-{i}",
                                          values=(Input_Parser(subject,'d2u'), Input_Parser(topics[j], 'd2u'), progress[j]))

            i += 1
            j += 1

        return tree, scrollbar

    def closewarning(self):
        """
        Popup message warning the user he cannot exit the exam unless he uses the finish button
        :return: None
        """

        popupwindow = tk.Toplevel(self.questionwindow)
        txtvar = tk.StringVar()
        warning = tk.Message(popupwindow, textvariable=txtvar)

        txtvar.set("You cannot exit at this time, please finish the exam or proceed to the finish button.")
        warning.pack()

    def Exam_creation(self):
        """
        Main function for exam creation
        :return: None
        """


        from src.Exam_gen.Exam_Generator import Generate_Exam

        nb_q = int(self.amountvar.get())

        Exam = Generate_Exam(nb_q, self.data_bank)
        Exam.select_questions()

        self.amountwindow.withdraw()
        self.questionwindow = tk.Toplevel()
        self.questionwindow.resizable(False, False)

        self.questionwindow.protocol('WM_DELETE_WINDOW', self.closewarning)

        q_note = ttk.Notebook(self.questionwindow)

        tab_frame_lst      = [tk.Frame(q_note) for _ in range(nb_q+1)]
        q_strings   = [f"Q-{i+1}" for i in range(nb_q)]
        answer_variables = [tk.StringVar() for _ in range(nb_q)]
        Q_n_A = Exam.e_questions

        progress = [None for _ in range(nb_q)]
        user_answers = [0 for _ in range(nb_q)]

        for i in range(nb_q):
            q_note.add(tab_frame_lst[i], text=q_strings[i])
            answer_variables[i].set("Type An Answer\n And Click Button To Display Answer")

        q_note.add(tab_frame_lst[-1], text="Finish")

        tab_list = q_note.tabs()

        def surrender(var, idx, txt, ans, *args):
            """
            Function for when the user surrenders
            :param var: Answer Label Stringvar
            :param idx: question index
            :param txt: user input box
            :param ans: correct answer
            :param args: buttons
            :return: None
            """

            progress[idx] = 0.0

            q = Q_n_A[idx]
            Exam.attempts_append_GUI(q, 0)

            correct_answer = ans
            print(f"DEBUG SURRENDER: {correct_answer}")

            txt.delete("1.0", END)
            txt.insert(END, "You gave up")
            txt.config(state=DISABLED)
            var.set(correct_answer)

            for btn in args:
                btn.config(state=DISABLED)


        def submit_answer(var, idx, txt, ans, *args):
            """
            Function for when the user submits an answer
            :param var: Answer Label Stringvar
            :param idx: question index
            :param txt: user input box
            :param ans: correct answer
            :param args: buttons
            :return: None
            """

            progress[idx] = 'submitted'

            user_answer = txt.get("1.0", END)
            user_answers[idx] = user_answer

            correct_answer = ans
            print(f"DEBUG SUBMIT: {correct_answer}")

            txt.config(state=DISABLED)
            var.set(correct_answer)

            for btn in args:
                #print(f"DEBUG BTN: {btn, btn['state']}")
                if str(btn['state']) == 'disabled':
                    btn.config(state=NORMAL)

                else:
                    btn.config(state=DISABLED)

        def correctsubmission(idx, *args):
            """
            Function for when the user marks himself correct
            :param idx: question index
            :param args: buttons
            :return: None
            """

            progress[idx] = 1

            q = Q_n_A[idx]
            Exam.attempts_append_GUI(q, 1)

            for btn in args:
                btn.config(state=DISABLED)

        def wrongsubmission(idx, *args):
            """
            Function for when the user marks himself wrong
            :param idx: question index
            :param args: buttons
            :return: None
            """

            progress[idx] = 0

            q = Q_n_A[idx]
            Exam.attempts_append_GUI(q, 0)

            for btn in args:
                btn.config(state=DISABLED)

        def TabChange(event):
            """
            Function for changing to another question
            :param event: <<NotebookTabChange>>
            :return: None
            """

            try:
                idx = q_note.index(q_note.select())

            except Exception:
                idx = 0

            tab = tab_frame_lst[idx]

            if not idx == len(tab_list) - 1:

                Exam.attempts_gen_GUI(idx)

                question = Q_n_A[idx].q_str
                answer = Q_n_A[idx].q_ans


                maxwidth = 40
                minwidth = 10

                if len(question) > maxwidth:

                    words = question.split(" ")

                    new_question = ''

                    for idx, word in enumerate(words):
                        nq_lst = new_question.split("\n")

                        if not len(nq_lst[-1] + word + " ") > maxwidth:
                            new_question += (word + " ")

                        else:
                            new_question += ("\n" + word + " ")

                    question = new_question


                else:
                    pass

                labelFrame = tk.Frame(tab)
                textFrame = tk.Frame(tab)
                btnFrame = tk.Frame(tab)

                sublabel = tk.Label(labelFrame, text=str(Exam.subject), font=Large_Bold_Font)
                toplabel = tk.Label(labelFrame, text=str(Exam.topic), font=Medium_Bold_Font)


                #answer_variables[idx].trace('r', lambda nm, i, mode, var=answer_variables[idx]: print(f"DEBUG AVAR: {answer_variables[idx].get()}"))

                Q_label = tk.Label(labelFrame, text=Input_Parser(question, 'd2u'), font=MEDIUM_FONT, width=maxwidth)
                A_label = tk.Label(labelFrame, textvariable=answer_variables[idx], font=MEDIUM_FONT, width=maxwidth)

                emptylabels_1 = [tk.Label(labelFrame, text="\n").grid(row=i + 2, column=0) for i in range(2)]
                emptylabels_2 = [tk.Label(labelFrame, text="\n").grid(row=i + 5, column=0) for i in range(2)]
                emptylabels_3 = [tk.Label(labelFrame, text="\n").grid(row=i + 8, column=0) for i in range(2)]
                emptylabels_4 = [tk.Label(labelFrame, text="\n").grid(row=i, column=1) for i in range(2)]

                sublabel.grid(row=0, column=0, sticky=N + W)
                toplabel.grid(row=1, column=0, sticky=N + W)
                Q_label.grid(row=4, column=0, sticky=N + W)
                A_label.grid(row=7, column=0, sticky=N + W)

                Answer_Entry = tk.Text(textFrame, height=10)

                Answer_Entry.insert(END, "Type you answer here...")

                Answer_Entry.grid(row=0, sticky=N + W)

                photo = Image.open('./GUI/icons/abstract/yes.png')
                photo = photo.resize((40, 32), Image.ANTIALIAS)
                photo = ImageTk.PhotoImage(photo)
                correctbutton = ttk.Button(btnFrame, text='Correct!', image=photo, compound=TOP, width=15,
                                             command=None)
                correctbutton.image = photo

                photo = Image.open('./GUI/icons/abstract/no.png')
                photo = photo.resize((40, 32), Image.ANTIALIAS)
                photo = ImageTk.PhotoImage(photo)
                wrongbutton = ttk.Button(btnFrame, text='Wrong', image=photo, compound=TOP, width=15,
                                             command=None)
                wrongbutton.image = photo

                photo = Image.open('./GUI/icons/objects/padlock_open.png')
                photo = photo.resize((40, 32), Image.ANTIALIAS)
                photo = ImageTk.PhotoImage(photo)
                answerbutton = ttk.Button(btnFrame, text='Check Answer', image=photo, compound=TOP, width=15)
                answerbutton.image = photo

                photo = Image.open('./GUI/icons/abstract/surrender.png')
                photo = photo.resize((40, 32), Image.ANTIALIAS)
                photo = ImageTk.PhotoImage(photo)
                surrenderbutton = ttk.Button(btnFrame, text='Give Up', image=photo, compound=TOP, width=15)
                surrenderbutton.image = photo

                surrenderbutton.config(command=lambda: surrender(answer_variables[idx], idx, Answer_Entry, answer, surrenderbutton, answerbutton, correctbutton, wrongbutton))
                answerbutton.config(command=lambda: submit_answer(answer_variables[idx], idx, Answer_Entry, answer, answerbutton, surrenderbutton, correctbutton, wrongbutton))

                correctbutton.config(command=lambda: correctsubmission(idx, wrongbutton), state=DISABLED)
                wrongbutton.config(command=lambda: wrongsubmission(idx, correctbutton), state=DISABLED)

                if progress[idx] != None:

                    Answer_Entry.delete("1.0", END)
                    Answer_Entry.insert(END, user_answers[idx])
                    answer_variables[idx].set(answer)

                    answerbutton.config(state=DISABLED)
                    surrenderbutton.config(state=DISABLED)


                answerbutton.grid(row=2, column=0, ipadx = 35, ipady=10, sticky=N + E)
                surrenderbutton.grid(row=3, column=0, ipadx=35, ipady=10, sticky=N + E)
                correctbutton.grid(row=4, column=0, ipadx=35, ipady=10, sticky=N + E)
                wrongbutton.grid(row=5, column=0, ipadx=35, ipady=10, sticky=N + E)

                tab.columnconfigure((0,1), weight=1)
                tab.rowconfigure((0,1), weight=1)

                labelFrame.grid(row=0, column=0, sticky=N + W)
                btnFrame.grid(row=0, column=1, sticky=N + W)
                textFrame.grid(row=1, column=0, columnspan=2, sticky=N + W)

            else:

                headerFrame = tk.Frame(tab)
                scoreFrame  = tk.Frame(tab)

                tk.Label(headerFrame, text="Overview", font=Large_Bold_Font).grid(row=0, column=0, sticky=N+W)
                emptylabels_1 = [tk.Label(headerFrame, text="\n").grid(row=i + 1, column=0) for i in range(2)]

                tree, scroll = self.scoretreeview(scoreFrame, nb_q, Exam, progress)
                tree.grid(row=0, column=0, sticky=N+W)
                scroll.grid(row=0, column=1, sticky=N+W+S)

                photo = Image.open('./GUI/icons/actions/flag.png')
                photo = photo.resize((40, 32), Image.ANTIALIAS)
                photo = ImageTk.PhotoImage(photo)
                finishbtn = ttk.Button(scoreFrame, text="Finish", image=photo, compound=TOP, width=40,
                                       command=lambda: self.finishexam(Exam, Q_n_A, progress))
                finishbtn.image = photo
                finishbtn.grid(row=0, column=2, sticky=N+W)

                headerFrame.grid(row=0, column=0)
                scoreFrame.grid(row=3, column=0)


        q_note.bind("<<NotebookTabChanged>>", TabChange)
        q_note.event_generate("<<NotebookTabChanged>>")
        q_note.grid()

    def finishexam(self, exam, questions, progress):
        """
        Function for when the user finishes an exam
        :param exam: Exam object
        :param questions: Questions given to user
        :param progress: progress list
        :return: None
        """

        self.finishwindow = tk.Toplevel(self.questionwindow)
        self.finishwindow.resizable(False, False)

        label = tk.Label(self.finishwindow, text="Are you sure you want to quit?\nUnfinished Questions will be marked as incorrect!")

        btnFrame = tk.Frame(self.finishwindow)

        confirmbtn = ttk.Button(btnFrame, text="Yes", command=lambda: self.finishconfirm(exam, questions, progress))
        cancelbtn  = ttk.Button(btnFrame, text="No", command=self.finishwindow.withdraw)

        confirmbtn.grid(row=0, column=0)
        cancelbtn.grid(row=0, column=1)

        label.grid(row=0, column=0)
        btnFrame.grid(row=1, column=0)

    def finishconfirm(self, exam, questions, progress):
        """
        Function for when the user for sure wants to quit
        :param exam: Exam object
        :param questions: Questions given to user
        :param progress: progress list
        :return: None
        """

        for q, p in zip(questions, progress):
            if p == None:
                exam.attempts_append_GUI(q, 0)


        exam.log_attempts()
        exam.question_leitner_update()

        self.finishwindow.withdraw()
        self.questionwindow.withdraw()


    def populate(self, frame, subject):
        """
        Function to populate the topic and subject selection canvas
        :param frame: frame in which to place the widgets
        :param subject: subject name
        :return: None
        """
        subject_font = ("Verdana", 10, 'bold')
        topic_font = ("Verdana", 8)

        checkvarslst = []
        subvar = tk.BooleanVar()
        subvar.set(False)
        self.checkvarsdict_subjects[subject] = subvar

        tk.Checkbutton(frame, variable=subvar, bg='white', command=lambda: self.parentselect(subvar)).grid(row=0, column=0, sticky=N+W)
        tk.Label(frame, text=Input_Parser(subject, 'd2u')+":", bg='white', font=subject_font).grid(row=0, column=1, sticky=N+W)

        for i, topic in enumerate(topicList[subject]):
            checkvarslst.append(tk.BooleanVar())
            checkvarslst[i].set(False)
            tk.Label(frame, text=Input_Parser(topic, 'd2u'), bg='white', font=topic_font).grid(row=i+1, column=1, sticky=N+W)
            tk.Checkbutton(frame, variable=checkvarslst[i], bg='white').grid(row=i+1, column=0)

        self.checkvarsdict_topics[subject] = checkvarslst

    def onFrameConfigure(self, event, canvas):
        '''Reset the scroll region to encompass the inner frame'''
        canvas.configure(scrollregion=canvas.bbox("all"))


    def SingleCanvas(self, parent, subject, row, col):
        """
        Function to create a single subject canvas on the subject and topic selection page
        :param parent: parent frame
        :param subject: subject name
        :param row: row coordinate wrt other canvasses
        :param col: column coordinate wrt other canvasses
        :return: None
        """

        canvas = tk.Canvas(parent, borderwidth=10, background="#ffffff", width=250, height=200)
        frame = tk.Frame(canvas, borderwidth=10, background="#ffffff")
        vsb = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)

        vsb.grid(row=row, column=col+1, sticky=N+S+W)
        canvas.grid(row=row, column=col)
        canvas.create_window(10, 10, window=frame, anchor="nw",
                                  tags="self.frame1")

        frame.bind("<Configure>", lambda event: self.onFrameConfigure(event, canvas))

        self.populate(frame, subject)

    def parentselect(self, var):
        """
        Function to set all children to the same value as the parent if the parent changes
        :param var: subject boolean
        :return: None
        """
        for key, val in self.checkvarsdict_subjects.items():
            if val == var:
                break

        if var.get() == True:

            for check in self.checkvarsdict_topics[key]:
                check.set(True)

        elif var.get() == False:

            for check in self.checkvarsdict_topics[key]:
                check.set(False)


class StatsPage(tk.Frame):


    def __init__(self, parent, controller):
        """
        Initialization of the statistics page
        :param parent: parent frame
        :param controller: tk.Tk controller
        """

        NavButtons(self, parent, controller, text="Statistics")

        plotFrame = tk.Frame(self)
        toolFrame = tk.Frame(self)
        treeFrame = tk.Frame(toolFrame, width=400, height=14*30)
        btFrame   = tk.Frame(toolFrame)
        self.stFrame   = tk.Frame(toolFrame)

        self.tree, scrollbar = TreeView(treeFrame, version='basic')
        self.tree.bind("<<TreeviewSelect>>", self.plotselections)
        #self.tree.bind("<ButtonRelease-1>", self.plotselections)

        global plot_selection
        plot_selection = ('1.1',)

        global plotdata
        plotdata = ['E']

        self.plotting(plotFrame)

        buttonsx, buttonsy = (14,10)

        photo = Image.open('./GUI/icons/actions/repeat_green.png')
        photo = photo.resize((40, 32), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(photo)
        refresh_btn = ttk.Button(btFrame, text="Refresh", width=buttonsx, image=photo, compound=TOP,
                                command=lambda: repopulate(self.tree, version='basic'))
        refresh_btn.image = photo


        photo = Image.open('./GUI/icons/geometry/loss.png')
        photo = photo.resize((40, 32), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(photo)
        errorrate_btn = ttk.Button(btFrame, text="Plot Error-Rate", width=buttonsx, image=photo, compound=TOP,
                              command=lambda: plotdata.append('E'))
        errorrate_btn.image = photo

        photo = Image.open('./GUI/icons/geometry/gain.png')
        photo = photo.resize((40, 32), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(photo)
        success_btn = ttk.Button(btFrame, text="Plot Trials", width=buttonsx, image=photo, compound=TOP,
                              command=lambda: plotdata.append('S'))
        success_btn.image = photo

        global statStringVars, text
        statStringVars = [tk.StringVar() for _ in range(3)]
        text = tk.Text(self.stFrame, height=8, width=48)


        refresh_btn.grid(row=0, column=0)
        errorrate_btn.grid(row=0, column=2)
        success_btn.grid(row=0, column=1)
        treeFrame.pack_propagate(0)
        self.tree.pack(side='left')

        plotFrame.grid(row=2, column=1, sticky=N + W)
        toolFrame.grid(row=2, column=0, sticky=N+W)
        btFrame.grid(row=0, column=0, sticky=N+W)
        treeFrame.grid(row=1, column=0, sticky=N+W)
        self.stFrame.grid(row=2, column=0, sticky=N+W)


    def plotselections(self, event):

        """
        Function to return what subjects/topics need to be plotted
        :param event:
        :return:
        """

        global plot_selection
        plot_selection = self.tree.selection()

        for select in plot_selection:

            if select[-1] == '0':
                children = self.tree.get_children([select])

                s = set(plot_selection)
                to_append = tuple([child for child in children if child not in s])

                plot_selection += to_append


    def animate(self):
        """
        Function to animate the graph and refresh every defined interval
        :return: None
        """

        df1, df2 = dataframe(plot_selection)

        dates = df1['Date']

        Add.clear()

        if plotdata[-1] == 'E':
            error = error_rate(df1)

            if len(error) == 0:

                now = str(datetime.datetime.now())
                now = now.split(" ")
                hours = now[1].split(".")[0]
                now[1] = hours
                now = " ".join(now)
                error = [0]
                dates = [pd.Timestamp((datetime.datetime.strptime(now.replace("\n", ""),
                                                                  '%Y-%m-%d %H:%M:%S')))]

            Add.plot(dates, error, 'r-x', label='Error Rate')
            Add.set_ylabel('Error rate')
            Add.set_title('Error Rate Over Time')

        elif plotdata[-1] == 'S':
            fail, succes = fail_success(df1)

            if len(fail) == 0:

                now = str(datetime.datetime.now())
                now = now.split(" ")
                hours = now[1].split(".")[0]
                now[1] = hours
                now = " ".join(now)
                fail = [0]
                dates = [pd.Timestamp((datetime.datetime.strptime(now.replace("\n", ""),
                                                                  '%Y-%m-%d %H:%M:%S')))]

            if len(succes) == 0:

                now = str(datetime.datetime.now())
                now = now.split(" ")
                hours = now[1].split(".")[0]
                now[1] = hours
                now = " ".join(now)
                succes = [0]
                dates = [pd.Timestamp((datetime.datetime.strptime(now.replace("\n", ""),
                                                                  '%Y-%m-%d %H:%M:%S')))]

            Add.plot(dates, fail, 'r-o', label="Fails")
            Add.plot(dates, succes, 'g-o', label="Successes")
            Add.set_ylabel('Attempts')
            Add.set_title('Attempts Over Time')

        Add.legend()
        Add.set_xlabel('Date')

        for tick in Add.get_xticklabels():
            tick.set_rotation(30)

        # global text
        df1, df2 = dataframe(plot_selection)
        global success, failures, ratios
        success, failures, ratios = basic_stats(df1)

        for idx, var in enumerate(statStringVars):
            var.set(str(basic_stats(df1)[idx]))

        text.delete(1.0, END)
        text.config(borderwidth=2)
        text.insert(END, "Basic Statistics:\n\n")
        text.insert(END, "Amount of Successes:  {0}\n".format(statStringVars[0].get()))
        text.insert(END, "Amount of Failures:   {0}\n".format(statStringVars[1].get()))
        text.insert(END, "Succes-Failure Ratio: {0}\n".format(statStringVars[2].get()))
        text.grid(row=0, column=0, sticky=N + W)


    def plotting(self, frame):
        """
        Canvas creation for the plot
        :param frame: frame in which to place the canvas
        :return: None
        """

        canvas = FigureCanvasTkAgg(F, frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

        toolbar = NavigationToolbar2Tk(canvas, frame)
        toolbar.update()
        canvas.get_tk_widget().pack()


if __name__ == "__main__":

    App = AcumenApp()
    App.geometry("900x750")
    ani = animation.FuncAnimation(F, StatsPage.animate, interval=250)
    App.mainloop()