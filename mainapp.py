# importing libraries for GUI, GUI file upload, GUI message pop up
from tkinter import *
from tkinter.filedialog import askopenfile
from tkinter import messagebox
import pandas as pd
from IPython.display import display
from csv import DictReader
from LFparser import parser
from LFparser import projectFileParser


def student_search(event):
    # enter the student's name in the entry and hit enter, filter out other students' names with only relevant students
    #   listed
    student_filter = []
    filter = event.widget.get().lower()
    for obj in studentlist[1:]:
        if filter in obj.lastName.lower() or filter in obj.firstName.lower():
            student_filter.append(obj.firstName + ' ' + obj.lastName)
    # listbox.insert(END, *student_filter)
    print(student_filter)


studentFileOpenCount = 0
projectFileOpenCount = 0

# Setting up the GUI window and size of the initial window. The window can be dragged and altered to fit the desired
# size on the screen.
root = Tk()
root.title("The Learning Factory")
root.geometry('850x700')

#################################################  MAIN FRAME  #################################################
mainFrame = Frame(root)
mainFrame.pack(side=TOP)
mainFrameLabel = Label(mainFrame, text="Learning Factory Dashboard", font=("Courier", 35))
mainFrameLabel.pack()
subTitle = Label(mainFrame, text="Please upload the proper CSV files to start", font=("Courier", 20))
subTitle.pack()

#################################################  STUDENT FRAME  #################################################
studentFrame = Frame(root)
studentFrame.pack(side=LEFT, expand=TRUE, fill=BOTH)

studentFrameLabel = Label(studentFrame, text="Student Search", font=("Courier", 20))
studentFrameLabel.pack(side=TOP)

studentSearchLabel = Label(studentFrame, text="Student Name:", font=("Courier", 10))
studentSearchLabel.pack(side=TOP)

studentSearch = Entry(studentFrame)
studentSearch.bind('<Return>', student_search)
studentSearch.pack(side=TOP)

#################################################  PROJECT FRAME  #################################################
projectFrame = Frame(root)
projectFrame.pack(side=RIGHT, expand=TRUE, fill=BOTH)

projectFrameLabel = Label(projectFrame, text="Project Search", font=("Courier", 20))
projectFrameLabel.pack(side=TOP)

projectSearchLabel = Label(projectFrame, text="Project name:", font=("Courier", 10))
projectSearchLabel.pack(side=TOP)

projectSearch = Entry(projectFrame)
projectSearch.pack(side=TOP)


# student and project list buttons allow the user to go to the list of students and projects in the future. For now
# it checks if the proper CSV file has been uploaded and shows content of CSV file by setting offset at 0 and reading
# the file, if the file is missing an error will pop up
def students_list():
    global studentFile
    global studentFileOpenCount
    global studentlst
    global studentlist

    studentFile = askopenfile(mode='r+', filetypes=[('CSV Files', '*.csv')])

    if studentFile is not None:
        # calls in parser to create a list of objects from CSV
        studentlist = parser(studentFile)

        # if a previous CSV is open then the list will be deleted
        if studentFileOpenCount != 0:
            scrollbar.delete("1.0", tk.END)

        # the scrollbar is implemented and filled with content
        scrollbar = Scrollbar(studentFrame)
        scrollbar.pack(side=RIGHT, expand=TRUE, fill=BOTH)
        studentlst = Listbox(studentFrame, yscrollcommand=scrollbar.set)
        for obj in studentlist[1:]:
            # avoid the first row in the csv that just has titles
            # add the student's first and last name to the listbox
            studentlst.insert(END, obj.firstName + " " + obj.lastName)
        studentlst.pack(side=LEFT, expand=TRUE, fill=BOTH)
        scrollbar.config(command=studentlst.yview)
        studentFileOpenCount += 1
        studentlst.bind('<Double-1>', student_select)
    # studentFile.seek(0)
    else:
        messagebox.showerror("Error", "No student CSV file detected")


def project_list():
    global projectFile
    global projectFileOpenCount
    global projlst
    global projectlist

    projectFile = askopenfile(mode='r+', filetypes=[('CSV Files', '*.csv')])

    if projectFile is not None:
        # calls in parser to create a list of objects from CSV
        projectlist = projectFileParser(projectFile)

        # if a prevous CSV is open then the list will be deleted
        if projectFileOpenCount != 0:
            scrollbar.delete("1.0", tk.END)

        # the scrollbar is implemented and filled with content
        scrollbar = Scrollbar(projectFrame)
        scrollbar.pack(side=RIGHT, expand=TRUE, fill=BOTH)
        projlst = Listbox(projectFrame, yscrollcommand=scrollbar.set)
        for obj in projectlist[1:]:
            # avoid the first row in the csv that just has titles
            projlst.insert(END, obj.projectTitle)
        projlst.pack(side=LEFT, expand=TRUE, fill=BOTH)
        scrollbar.config(command=projlst.yview)
        projectFileOpenCount += 1
        projlst.bind('<Double-1>', project_select)
    # projectFile.seek(0)
    else:
        messagebox.showerror("Error", "No project CSV file detected")


def student_select(event):
    # Create a new window with the student attributes and 2 buttons to swap projects with another student
    # or move to a different project. Once this is completed, create a new CSV file and return to the user
    newWindow = Toplevel(root)
    newWindow.title("Student")
    newWindow.geometry("400x400")
    Label(newWindow, text="Student window").pack()

    # studentPicked = studentlst.curselection()
    studentPicked = studentlst.curselection()[0]
    name = Label(newWindow,
                 text=studentlist[studentPicked + 1].firstName + " " + studentlist[studentPicked + 1].lastName)
    major = Label(newWindow, text="Major : " + studentlist[studentPicked + 1].major)
    projid = Label(newWindow, text="Project ID : " + studentlist[studentPicked + 1].projectID)
    studentIP = Label(newWindow, text="Student IP : " + studentlist[studentPicked + 1].studentIP)
    onCampus = Label(newWindow, text="On Campus? " + studentlist[studentPicked + 1].onCampus)
    campusID = Label(newWindow, text="Campus ID : " + studentlist[studentPicked + 1].campusID)
    nda = Label(newWindow, text="NDA? " + studentlist[studentPicked + 1].studentNDA)

    btn1 = Button(newWindow, text='Swap teams with another student', command=swapStudents)
    btn2 = Button(newWindow, text='Move to a different team')
    name.pack(pady=10)
    major.pack(pady=10)
    projid.pack(pady=10)
    studentIP.pack(pady=10)
    onCampus.pack(pady=10)
    campusID.pack(pady=10)
    nda.pack(pady=10)
    btn1.pack(pady=10)
    btn2.pack(pady=10)


def project_select(event):
    # Create a new window with the student attributes and 2 buttons to swap projects with another student
    # or move to a different project. Once this is completed, create a new CSV file and return to the user
    newWindow = Toplevel(root)
    newWindow.title("Project")
    newWindow.geometry("800x800")

    projectPicked = projlst.curselection()
    projectPicked = projectPicked[0]

    name = Label(newWindow, text=projectlist[projectPicked + 1].projectTitle)
    company = Label(newWindow, text="Company : " + projectlist[projectPicked + 1].companyName)
    projid = Label(newWindow, text="Project ID : " + projectlist[projectPicked + 1].projectID)
    confid = Label(newWindow, text="Confidentiality? " + projectlist[projectPicked + 1].confidentiality)
    ip = Label(newWindow, text="IP : " + projectlist[projectPicked + 1].ip)
    courseName = Label(newWindow, text="Course Name: " + projectlist[projectPicked + 1].courseName)
    courseTime = Label(newWindow, text="Course Time: " + projectlist[projectPicked + 1].courseTime)
    physPrototype = Label(newWindow, text="Physical Prototype? " + projectlist[projectPicked + 1].physicalPrototype)
    bme = Label(newWindow, text="BME : " + projectlist[projectPicked + 1].bme)
    cmpen = Label(newWindow, text="CMPEN : " + projectlist[projectPicked + 1].cmpen)
    cmpsc = Label(newWindow, text="CMPSC : " + projectlist[projectPicked + 1].cmpsc)
    ds = Label(newWindow, text="DS : " + projectlist[projectPicked + 1].ds)
    ed = Label(newWindow, text="ED : " + projectlist[projectPicked + 1].ed)
    ee = Label(newWindow, text="EE : " + projectlist[projectPicked + 1].ee)
    egee = Label(newWindow, text="EGEE : " + projectlist[projectPicked + 1].egee)
    esc = Label(newWindow, text="ESC : " + projectlist[projectPicked + 1].esc)
    ie = Label(newWindow, text="IE : " + projectlist[projectPicked + 1].ie)
    matse = Label(newWindow, text="MATSE : " + projectlist[projectPicked + 1].matse)
    me = Label(newWindow, text="ME : " + projectlist[projectPicked + 1].me)

    btn1 = Button(newWindow, text='Swap teams with another student', command=swapStudents)
    btn2 = Button(newWindow, text='Move to a different team')
    name.pack(pady=10)
    company.pack(pady=10)
    projid.pack(pady=10)
    confid.pack(pady=10)
    ip.pack(pady=10)
    courseName.pack(pady=10)
    courseTime.pack(pady=10)
    physPrototype.pack(pady=10)
    bme.pack(pady=10)
    cmpen.pack(pady=10)
    cmpsc.pack(pady=10)
    ds.pack(pady=10)
    ed.pack(pady=10)
    ee.pack(pady=10)
    egee.pack(pady=10)
    esc.pack(pady=10)
    ie.pack(pady=10)
    matse.pack(pady=10)
    me.pack(pady=10)
    btn1.pack(pady=10)
    btn2.pack(pady=10)


def swapStudents():
    print("hi")


# 1) Open another listbox with students to choose from and have the ability to double click and display that students
# 		attributes.
# 2) Have a confirmation button that when clicked, the swap will be made that will change the two students project IDs
# 3) As the confirmation button is displayed, show possible project/student disagreements by using the two project's
# 		attributes

def moveStudent():
    print("hi")


# 1) Open a listbox that will have project names and the project IDs with the ability to double click
# 2) Have a confirmation button that when clicked, the student project ID will be updated to the new ID
# 3) As the confirmation button is displayed, show any possible project/student disagreements by using the project
# 		attributes


def team_irregularity():
    # Search through the team file and find teams that are too big, too small, or don't have all of the
    # correct majors assigned for the team by cross checking with the student file.
    print('hi')


# All the buttons that are on the homepage in the format Button(root, text, command). Root is used to connect the
# button to the parents window. Text is used to display text on the button. Command is used to call a function when
# the button is clicked.
btn1 = Button(mainFrame, text='Upload Student CSV', command=students_list)
btn2 = Button(mainFrame, text='Upload Project CSV', command=project_list)
btn4 = Button(mainFrame, text='Project Irregularity Test', command=project_list)
btn5 = Button(mainFrame, text='Generate PDF', command=project_list)

btn1.pack(pady=10)
btn2.pack(pady=10)
btn4.pack(pady=10)
btn5.pack(pady=10)

# the main loop that keeps the app running
mainloop()
