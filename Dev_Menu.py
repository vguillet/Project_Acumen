"""
Mainframe for development purpose
Basic decision tree interface for the developer
"""
# ___________________________________________________________INITIALISATION OF GENERATOR SETTINGS
from src.Exam_gen.Exam_Gen_process import exam_gen_process
from src.Stats_gen.Stats_Gen_process import stats_gen_process

run = True

# ___________________________________________________________PROGRAM DECISION TREE
while run:
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~MAIN MENU~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
    choice = int(input("What would you like to do? "
                       "\n 1) Generate exam "
                       "\n 2) Generate stats "
                       "\n 3) Clear log file" 
                       "\n 4) Exit program"
                       "\n Selection:"))

    # ---------------------------Generate exam
    if choice == 1:
        exam_gen_process()
        # This function call on the exam generation process function which handle exam generation.
        # It contains a number of print statements along with a few input requirement from the user
        # such as hit enter to display answer (something which could be replaced by a button i believe)

    # ---------------------------Generate statistics
    elif choice == 2:
        stats_gen_process()
        # This function call on the stats generation process function which handles stats generation
        # It contains a number of print statements along with a few input requirement from the user
        # such as what topic is wanted in the stats etc...

    # ---------------------------Other
    elif choice == 3:                                   # Clear Attempts_log file
        delete = int(input("\nAre you sure? This operation is irreversible\nYes - 0 , Cancel - 1: "))
        if delete == 0:
            open('src\Attempts_log.txt', 'w').close()
            print("\nAttempts_log cleared!")

        elif delete == 1:
            break

    elif choice == 4:                                   # Exit program
        run = False
