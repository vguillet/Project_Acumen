# Acumen
The intent of this software is to help students prepare for exams by providing them with an easy to use tool that is able to generate statistics on their study performance/progress and provide recommendation. 
The software would be able to use statistics gathered (via the generation of exams and recording of answers) to generate further practice exams tailored to the user’s performance, using a bank of questions (created by the user). 
This would enable students to acquire insight into their skills and difficulties and allow for them to focus their time on practicing content they struggle most with, thus enabling for a better and more efficient exam preparation.

**Basic features:**
- The user creates subjects and inputs questions with answers into different topics under a certain subject. 
- The user will  be able to generate practice exams based on a selected subject, or specific topics to study from, further tailoring exam generation to their needs. 
- The software would be able to generate exams based on user performance recorded in the different topics.
- The software would be able to keep track of a user’s progress and generate statistics thereby providing greater insight to the user in their journey of learning.

**Advanced features:**

- The software could suggest learning material/resources to further improve knowledge on certain topics were performance is lacking.
- In the future the software could be capable of importing and analyzing documents in different formats (word or pdf formats), detecting and categorizing questions by itself.

## Software structure

The software is made up of 4 main modules, the GUI, the Database, the exam and the statistics generation modules.

## Running the software

Before running the software make sure you have all of the dependencies given in requirements.txt, taking special care to make sure every dependency is up-to-date(program will crash if matplotlib is not 3.0.0, or perhaps more recent). If dependencies were recently installed make sure to restart your computer before running.
Using Pycharm as an example, once the repo is cloned mark the directory Group 12 as the Sources Root.

To run the program use GUI_Integration.py and follow the instructions in the help menu. 


>>>
Acumen is made by 4 Computer Science minor students:

Kevin Bislip 4536908, Project Manager, scrum master, product owner

Xavier Goby 4488822, Database with SQLite developer

Victor Guillet 4488636, GUI with TkInter developer

Luke de Waal 4560000, Exam-gen and statistics generation developer
>>>