import tkinter as tk
import numpy as np
from tkinter import ttk
from tkinter import N,S,E,W, NO, YES, END, FIRST, LAST, DISABLED, NORMAL, TOP, BOTTOM, LEFT, RIGHT
import sys
from PIL import Image,ImageTk
import time
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure as Graph



subjectList = [ "Maths",
                "Physics",
                "Chemistry"]
topicList   = {"Maths":["Arithmetic","Logarithms","Quadratic Equations","Matrices"],
               "Physics":["Newtonian Mechanics","Electro-Magnetism","Circuits","Waves","Nuclear Physics"],
               "Chemistry":["ReDox","Acids and Bases","Organic Chemistry"]}

openwindows = []


LARGE_FONT= ("Verdana", 12)


def NavButtons(frame, parent, controller, text):
    """
    Function to create the buttons to navigate between pages
    :param frame:
    :param parent:
    :param controller:
    :param text:
    :return:
    """
    tk.Frame.__init__(frame, parent)

    HeaderFrame = tk.Frame(frame)
    ButtonFrame = tk.Frame(frame)

    label = ttk.Label(HeaderFrame, text=text, font=LARGE_FONT)
    label.grid(row=0, column=2, padx=10, pady=10, sticky=N+S+E+W)

    home_button = ttk.Button(ButtonFrame, text="Home Page",
                             command=lambda: controller.switch_page(StartPage))
    home_button.grid(row=1, column=0, padx=10, pady=10, sticky=N+S+E+W)

    class_button = ttk.Button(ButtonFrame, text="Class Overview",
                              command=lambda: controller.switch_page(ClassesPage))
    class_button.grid(row=1, column=1, padx=10, pady=10, sticky=N+S+E+W)

    exam_button = ttk.Button(ButtonFrame, text="Exams",
                             command=lambda: controller.switch_page(ExamPage))
    exam_button.grid(row=1, column=2, padx=10, pady=10, sticky=N+S+E+W)

    stats_button = ttk.Button(ButtonFrame, text="Statistics",
                              command=lambda: controller.switch_page(StatsPage))
    stats_button.grid(row=1, column=3, padx=10, pady=10, sticky=N+S+E+W)

    HeaderFrame.grid(row=0, column=0, sticky=N+S+E+W)
    ButtonFrame.grid(row=1, column=0, sticky=N+S+E+W)


def TreeView(frame, row=0, col=0, version='full'):

    #treeFrame = tk.Frame(frame)

    style = ttk.Style()
    style.configure('Treeview', rowheight=25)

    scrollbar = tk.Scrollbar(frame)
    tree = ttk.Treeview(frame, yscrollcommand=scrollbar.set, height=12)
    scrollbar.config(command=tree.yview_scroll)

    if version.lower() == 'full':
        tree["columns"] = ["#{0}".format(i) for i in range(1,5)]
    else:
        tree["columns"] = ["#{0}".format(i) for i in range(1, 3)]

    tree.column("#0", width=200, stretch=NO)
    tree.column("#1", width=100, stretch=NO)
    tree.column("#2", width=100, stretch=NO)
    tree.heading("#0", text="Name")
    tree.heading("#1", text="# Topics")
    tree.heading("#2", text="Score")

    if version.lower() == 'full':
        tree.column("#3", width=100, stretch=NO)
        tree.column("#4", width=100, stretch=NO)
        tree.heading("#3", text="Time Spent")
        tree.heading("#4", text="Tears Shed")

    Levels = {}

    i = 0
    for subject in subjectList:
        Levels[subject] = tree.insert("".format(i), 'end', text=subject, values=(len(topicList[subject]), 0, 0, 100))
        i += 1
        for topic in topicList[subject]:
            tree.insert(Levels[subject], 'end', text=topic, values=("", 0, 0, 40))


    tree.grid(row=row, column=col, sticky=N+E+W)
    scrollbar.grid(row=row, column=col+1, sticky=N+S+W)

    #treeFrame.grid(row=row, column=col, sticky=N+E+W)



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


def testevent(event):
    print("Testing")
    return


def motion(event):
    print("Mouse position: (%s %s)" % (event.x, event.y))
    time.sleep(0.05)
    return


class AcumenApp(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, default='./icons/main_icon_2.ico')
        tk.Tk.wm_title(self, "Acumen")

        self.resizable(True, True)

        self.width = 900
        self.height = 620
        self.xposition = int(self.winfo_screenwidth() / 2 - self.width / 2)
        self.yposition = int(self.winfo_screenheight() / 2 - self.height / 2)

        self.geometry("{0}x{1}+{2}+{3}".format(self.width, self.height, self.xposition, self.yposition))


        self.bind("<Configure>", self.windowresize)
        #self.bind("<Motion>", motion)

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
        self.winsizes   = {'startpage': (865, 420),  "classespage": (685, 400), 'exampage': (500, 500), 'statspage':(925, 625)}
        self.FrameList  = (StartPage,   ClassesPage,    ExamPage,   StatsPage)
        self.LabelList  = ("Home Page", "Class Overview", "Exams", "Statistics")

        for F in self.FrameList:

            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.switch_page(StartPage)


    def windowresize(self, event):
        self.width = self.winfo_width()
        self.height = self.winfo_height()
        print("Size: ({0}, {1})".format(self.width, self.height))
        #time.sleep(0.05)
        return

    def setwindowsize(self, page):
        self.width = self.winsizes[page][0]
        self.height = self.winsizes[page][1]
        self.geometry("{0}x{1}+{2}+{3}".format(self.width, self.height, 300, 300))

    def switch_page(self, container):

        frame = self.frames[container]
        frame.tkraise()
        print(frame)
        name = str(frame)[9:]
        self.setwindowsize(name)



class StartPage(tk.Frame):

    def __init__(self, parent, controller):

        NavButtons(self, parent, controller, text="Home Page")

        welcomegrid = tk.Frame(self)

        photo = Image.open('./icons/WelcomeImg.png')
        photo = photo.resize((400, 325), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(photo)
        lb = tk.Label(welcomegrid, image=photo)
        lb.image = photo
        lb.grid(row=0, column=0)

        text = tk.Text(welcomegrid, height=20, width=55)
        scroll = tk.Scrollbar(welcomegrid, command=text.yview)
        text.configure(yscrollcommand=scroll.set)
        text.tag_configure('bold_italics', font=('Arial', 12, 'bold', 'italic'))
        text.tag_configure('big', font=('Verdana', 20, 'bold'))
        text.tag_configure('color', foreground='#476042',
                            font=('Tempus Sans ITC', 12, 'bold'))
        text.tag_bind('follow', '<1>', lambda e, t=text: t.insert(END, "Not now, maybe later!"))
        text.insert(END, '\n\tAcumen\n', 'big')
        quote = """
        \tTo be, or not to be that is the question:
        \tWhether 'tis Nobler in the mind to suffer
        \tThe Slings and Arrows of outrageous Fortune,
        \tOr to take Arms against a Sea of troubles.
        \n
        \t\t- William Shakespeare
        """
        text.insert(END, quote, 'color')
        text.config(state=DISABLED)
        text.grid(row=0, column=1)
        scroll.grid(row=0, column=2, sticky=N+S)

        welcomegrid.grid(row=2, column=0)

class ClassesPage(tk.Frame):

    def __init__(self, parent, controller):

        NavButtons(self, parent, controller, text="Classes")
        TreeView(self, row=2)

        btFrame = tk.Frame(self)

        buttonsx, buttonsy = (50,50)

        photo = Image.open('./icons/abstract/plus_green.png')
        photo = photo.resize((40, 32), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(photo)
        addsub_btn = tk.Button(btFrame, text="Enroll", height=buttonsx, width=buttonsy, image=photo, compound=TOP,
                               command=lambda: WarningWindow(self, "This Feature Has Not Been Implemented Yet",
                                                             "Our Sincerest Apologies for this,\nIt will be implemented very soon"))
        addsub_btn.image = photo

        photo = Image.open('./icons/abstract/minus_red.png')
        photo = photo.resize((40, 32), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(photo)
        delsub_btn = tk.Button(btFrame, text="Unenroll", height=buttonsx, width=buttonsy, image=photo, compound=TOP,
                               command=lambda: WarningWindow(self, "This Feature Has Not Been Implemented Yet",
                                                             "Our Sincerest Apologies for this,\nIt will be implemented very soon"))
        delsub_btn.image = photo

        photo = Image.open('./icons/office/pencil_green.png')
        photo = photo.resize((40, 32), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(photo)
        editsub_btn = tk.Button(btFrame, text="Edit", height=buttonsx, width=buttonsy, image=photo, compound=TOP,
                               command=lambda: WarningWindow(self, "This Feature Has Not Been Implemented Yet",
                                                             "Our Sincerest Apologies for this,\nIt will be implemented very soon"))
        editsub_btn.image = photo

        photo = Image.open('./icons/actions/repeat_green.png')
        photo = photo.resize((40, 32), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(photo)
        refresh_btn = tk.Button(btFrame, text="Refresh", height=buttonsx, width=buttonsy, image=photo, compound=TOP,
                                command=lambda: WarningWindow(self, "This Feature Has Not Been Implemented Yet",
                                                              "Our Sincerest Apologies for this,\nIt will be implemented very soon"))
        refresh_btn.image = photo

        addsub_btn.grid(row=0, column=1, sticky=N + W)
        delsub_btn.grid(row=1, column=1, sticky=N + W)
        editsub_btn.grid(row=2, column=1, sticky=N + W)
        refresh_btn.grid(row=3, column=1, sticky=N + W)

        btFrame.grid(row=2, column=2, sticky=N + W)

class ExamPage(tk.Frame):

    def __init__(self, parent, controller):

        NavButtons(self, parent, controller, text="Exams")

class StatsPage(tk.Frame):

    def __init__(self, parent, controller):

        NavButtons(self, parent, controller, text="Statistics")
        TreeView(self, version='basic', row=2, col=0)

        plotFrame = tk.Frame(self)

        figure = Graph(figsize=(5,5), dpi=100)
        add = figure.add_subplot(111)
        xdat = np.arange(0,10)
        ydat = np.random.randint(0,10,10)

        add.plot(xdat, ydat)

        canvas = FigureCanvasTkAgg(figure, plotFrame)
        canvas.draw()
        canvas.get_tk_widget().pack()

        toolbar = NavigationToolbar2Tk(canvas, plotFrame)
        toolbar.update()
        canvas._tkcanvas.pack()

        plotFrame.grid(row=2, column=1)


if __name__ == "__main__":

    App = AcumenApp()
    App.mainloop()