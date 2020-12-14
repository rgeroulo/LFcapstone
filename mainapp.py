# importing libraries for GUI, GUI file upload, GUI message pop up
from tkinter import *
from tkinter.filedialog import askopenfile
from tkinter import filedialog as fd
from tkinter import messagebox
import pandas as pd
from IPython.display import display
from csv import DictReader
from LFparser import parser
from LFparser import projectFileParser
import csv

studentFileOpenCount = 0
projectFileOpenCount = 0
_window_counter = 0
filtered = False
studentFile = None
projectFile = None

def student_search(event):
    # Enter a student's name, major, project ID, or student IP in the search abar and hit enter. This will filter out other students' names
    # and only show relevant students. These desired students will be in the listbox. To go back to the full
    #list, hit enter on an empty search box and it will revert back to the start. This serach supports partial
    #name searching as well so you dont have to type the whole name
    global student_filter
    student_filter = []
    filter = event.widget.get().lower()
    cursor = 0
    #This line deletes the line in the csv that has the labels
    studentlst.delete(0, END)
    #studentlst.insert(END, "First Name Last Name , Major , Project ID"))
    for obj in studentlist[1:]:
        if filter in obj.lastName.lower() or filter in obj.firstName.lower() or filter in obj.major.lower() or filter in obj.projectID.lower():
            student_filter.append((obj.firstName + ' ' + obj.lastName + ' ' + obj.major + ' ' + obj.projectID, cursor))
            studentlst.insert(END, obj.firstName + " " + obj.lastName + " , " + obj.major + " , " + obj.projectID)
            cursor += 1
        else:
            cursor += 1
            continue


def project_search(event):
    # Enter a project's title, project ID, or comapny name in the entry and hit enter. This will filter out other projects' names
    # and only show relevant projects. These desired projects will be in the listbox. To go back to the full
    #list, hit entet on an empty search box and it will revert back to the start. This serach supports partial
    #name searching as well so you dont have to type the whole title
    global project_filter
    project_filter = []
    filter = event.widget.get().lower()
    cursor = 0
    projlst.delete(0, END)
    #projlst.insert(END, "Project Title, Project ID , Company")
    for obj in projectlist[1:]:
        if filter in obj.projectTitle.lower() or filter in obj.projectID.lower() or filter in obj.companyName.lower():
            project_filter.append((obj.projectTitle + ' ' + obj.projectID + ' ' + obj.companyName, cursor))
            projlst.insert(END, obj.projectTitle + " , " + obj.projectID + " , " + obj.companyName)
            cursor += 1
        else:
            cursor += 1
            continue



# Setting up the GUI window and size of the initial window. The window can be dragged and altered to fit the desired
# size on the screen.
root = Tk()
root.title("The Learning Factory")
root.geometry('1000x700')

#################################################  MAIN FRAME  #################################################
mainFrame = Frame(root)
mainFrame.pack(side=TOP)
mainFrameLabel = Label(mainFrame, text="Learning Factory Dashboard", font=("Courier", 35))
mainFrameLabel.pack()
subTitle = Label(mainFrame, text="Please upload the proper CSV files to start", font=("Courier", 20))
subTitle.pack()

#################################################  STUDENT FRAME  #################################################
studentFrame = Frame(root, width = 450)
studentFrame.pack(side=LEFT, expand=TRUE, fill=BOTH)

studentFrameLabel = Label(studentFrame, text="Student Search", font=("Courier", 20))
studentFrameLabel.pack(side=TOP)

studentSearchLabel = Label(studentFrame, text="Student Name:", font=("Courier", 10))
studentSearchLabel.pack(side=TOP)

studentSearch = Entry(studentFrame)
studentSearch.bind('<Return>', student_search)
studentSearch.pack(side=TOP)
filtered = len(studentSearch.get()) != 0

#################################################  PROJECT FRAME  #################################################
projectFrame = Frame(root, width = 450)
projectFrame.pack(side=RIGHT, expand=TRUE, fill=BOTH)

projectFrameLabel = Label(projectFrame, text="Project Search", font=("Courier", 20))
projectFrameLabel.pack(side=TOP)

projectSearchLabel = Label(projectFrame, text="Project name:", font=("Courier", 10))
projectSearchLabel.pack(side=TOP)

projectSearch = Entry(projectFrame)
projectSearch.bind('<Return>', project_search)
projectSearch.pack(side=TOP)
filtered = len(studentSearch.get()) != 0


#students_list will be used to display the students in a listbox in the bottom left corner
#after the student CSV file is uploaded using the button in the middle of the GUI. This will
#generate a search bar and a scroll bar as well.
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
        scrollbar.pack(side=RIGHT, expand=TRUE, fill = Y)
        studentlst = Listbox(studentFrame, yscrollcommand=scrollbar.set)
        #studentlst.insert(END, "First Name Last Name , Major , Project ID")
        for obj in studentlist[1:]:
            # avoid the first row in the csv that just has titles
            # add the student's first and last name to the listbox
            studentlst.insert(END, obj.firstName + " " + obj.lastName + " , " + obj.major + " , " + obj.projectID)
        studentlst.pack(side=LEFT, expand=TRUE, fill=BOTH)
        scrollbar.config(command=studentlst.yview)
        studentFileOpenCount += 1
        studentlst.bind('<Double-1>', student_select)
    # studentFile.seek(0)
    else:
        messagebox.showerror("Error", "No student CSV file detected")

#project_list will be used to display the projects in a listbox in the bottom right corner
#after the project CSV file is uploaded using the button in the middle of the GUI. This function is
#extremely similar to the student_list fucntion above. This will generate a search bar and a scroll bar as well.
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
        scrollbar.pack(side=RIGHT, expand=TRUE, fill=Y)
        projlst = Listbox(projectFrame, yscrollcommand=scrollbar.set)
        #The following line will add the titles for each column. If you ever change the
        #attributes being changed, make sure to change these titles as well.
        #projlst.insert(END, "Project Title, Project ID , Company")
        for obj in projectlist[1:]:
            # avoid the first row in the csv that just has titles
            projlst.insert(END, obj.projectTitle + " , " + obj.projectID + " , " + obj.companyName)
        projlst.pack(side=LEFT, expand=TRUE, fill=BOTH)
        scrollbar.config(command=projlst.yview)
        projectFileOpenCount += 1
        projlst.bind('<Double-1>', project_select)
    # projectFile.seek(0)
    else:
        messagebox.showerror("Error", "No project CSV file detected")


#This is the window that comes up after you double click on a student
#The searching for students will support parital names,
#just first name, just last name, major, 
def student_select(event):
    global projid

    newWindow = Toplevel(root)
    newWindow.title("Student")
    newWindow.geometry("800x400")
    Label(newWindow, text="Student window").pack()
    filtered = len(studentSearch.get()) != 0
    if filtered:
        studentPicked = student_filter[studentlst.curselection()[0]][1]
    else:
        studentPicked = studentlst.curselection()[0]
    name = Label(newWindow,
                 text=studentlist[studentPicked + 1].firstName + " " + studentlist[studentPicked + 1].lastName)
    major = Label(newWindow, text="Major : " + studentlist[studentPicked + 1].major)
    projid = Label(newWindow, text="Project ID : " + studentlist[studentPicked + 1].projectID)
    studentIP = Label(newWindow, text="Student IP : " + studentlist[studentPicked + 1].studentIP)
    #onCampus = Label(newWindow, text="On Campus? " + studentlist[studentPicked + 1].onCampus)
    #campusID = Label(newWindow, text="Campus ID : " + studentlist[studentPicked + 1].campusID)
    nda = Label(newWindow, text="NDA? " + studentlist[studentPicked + 1].studentNDA)

    change_l = [(studentlst.selection_get(), studentlst.curselection()[0])]
    btn1 = Button(newWindow, text='Swap teams with another student', command=lambda: swapStudents(change_l))
    btn2 = Button(newWindow, text='Move to a different team', command=lambda: moveStudent(change_l))
    name.pack(pady=10)
    major.pack(pady=10)
    projid.pack(pady=10)
    studentIP.pack(pady=10)
    #onCampus.pack(pady=10)
    #campusID.pack(pady=10)
    nda.pack(pady=10)
    btn1.pack(pady=10)
    btn2.pack(pady=10)


def project_select(event):
    # Create a new window with the student attributes and 2 buttons to swap projects with another student
    # or move to a different project. Once this is completed, create a new CSV file and return to the user
    newWindow = Toplevel(root)
    newWindow.title("Project")
    newWindow.geometry("400x600")

    projectPicked = projlst.curselection()
    projectPicked = projectPicked[0]
    #Check to see what majors are required for the chosen project, they will be stored in "needed"
    needed = []
    if projectlist[projectPicked + 1].bme != "0":
        needed.append("bme")
    if projectlist[projectPicked + 1].cmpen != "0":
        needed.append("cmpen")
    if projectlist[projectPicked + 1].cmpsc != "0":
        needed.append("cmpsc")
    if projectlist[projectPicked + 1].ds != "0":
        needed.append("ds")
    if projectlist[projectPicked + 1].ed != "0":
        needed.append("ed")
    if projectlist[projectPicked + 1].ee != "0":
        needed.append("ee")
    if projectlist[projectPicked + 1].egee != "0":
        needed.append("egee")
    if projectlist[projectPicked + 1].esc != "0":
        needed.append("esc")
    if projectlist[projectPicked + 1].ie != "0":
        needed.append("ie")
    if projectlist[projectPicked + 1].matse != "0":
        needed.append("matse")
    if projectlist[projectPicked + 1].me != "0":
        needed.append("me")

    #Display the information that is relevant to the selected project.
    name = Label(newWindow, text=projectlist[projectPicked + 1].projectTitle)
    company = Label(newWindow, text="Company : " + projectlist[projectPicked + 1].companyName)
    projid = Label(newWindow, text="Project ID : " + projectlist[projectPicked + 1].projectID)
    confid = Label(newWindow, text="Confidentiality? " + projectlist[projectPicked + 1].confidentiality)
    ip = Label(newWindow, text="IP : " + projectlist[projectPicked + 1].ip)
    courseName = Label(newWindow, text="Course Name: " + projectlist[projectPicked + 1].courseName)
    courseTime = Label(newWindow, text="Course Time: " + projectlist[projectPicked + 1].courseTime)
    physPrototype = Label(newWindow, text="Physical Prototype? " + projectlist[projectPicked + 1].physicalPrototype)
    usedMajors = Label(newWindow, text="Majors Desired : " + str(needed))


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
    usedMajors.pack(pady=10)
    btn1.pack(pady=10)
    btn2.pack(pady=10)


def _delete_window():
    global _window_counter
    # print(_window_counter)
    try:
        student_change.destroy()
        _window_counter -= 1
        # print(_window_counter)
    except:
        pass


def _destroy(event):
    pass


def swap_select(event):
    # Create a new window with the student attributes and 2 buttons to swap projects with another student
    # or move to a different project.
    newWindow = Toplevel(root)
    newWindow.title("Student")
    newWindow.geometry("400x400")
    Label(newWindow, text="Student window").pack()

    # studentPicked = stu_lst.curselection()
    studentPicked = stu_lst.curselection()[0]
    if pass_name and passed_index <= stu_lst.curselection()[0]:
        studentPicked += 1
    name = Label(newWindow,
                 text=studentlist[studentPicked + 1].firstName + " " + studentlist[studentPicked + 1].lastName)
    major = Label(newWindow, text="Major : " + studentlist[studentPicked + 1].major)
    projid = Label(newWindow, text="Project ID : " + studentlist[studentPicked + 1].projectID)
    studentIP = Label(newWindow, text="Student IP : " + studentlist[studentPicked + 1].studentIP)
    onCampus = Label(newWindow, text="On Campus? " + studentlist[studentPicked + 1].onCampus)
    campusID = Label(newWindow, text="Campus ID : " + studentlist[studentPicked + 1].campusID)
    nda = Label(newWindow, text="NDA? " + studentlist[studentPicked + 1].studentNDA)

    name.pack(pady=10)
    major.pack(pady=10)
    projid.pack(pady=10)
    studentIP.pack(pady=10)
    onCampus.pack(pady=10)
    campusID.pack(pady=10)
    nda.pack(pady=10)


def swap(swap_l):
    studentPicked = stu_lst.curselection()[0]
    if pass_name:
        studentPicked += 1
    swap_l.append((stu_lst.selection_get(), studentPicked))
    studentlist[swap_l[0][1] + 1].projectID, studentlist[swap_l[1][1] + 1].projectID = \
        studentlist[swap_l[1][1] + 1].projectID, studentlist[swap_l[0][1] + 1].projectID
    projid.config(text="Project ID : " + studentlist[swap_l[0][1] + 1].projectID)


def swapStudents(swap_l):
    global _window_counter, studentFileOpenCount, stu_lst, pass_name, passed_index
    if _window_counter == 0:
        global student_change
        student_change = Toplevel(root)
        _window_counter += 1
    else:
        messagebox.showerror("Error", "Due to the limitation, can only open one swapping window at a time")
        student_change.lift()

    student_change.protocol("WM_DELETE_WINDOW", _delete_window)
    student_change.bind("<Destroy>", _destroy)
    student_change.title("Swapping Student")
    student_change.geometry("400x400")

    scrollbar = Scrollbar(student_change)
    scrollbar.pack(side=RIGHT, expand=TRUE, fill=BOTH)
    stu_lst = Listbox(student_change, yscrollcommand=scrollbar.set)

    pass_name = False
    index = 0
    for obj in studentlist[1:]:
        # avoid the first row in the csv that just has titles
        # add the student's first and last name to the listbox
        if obj.firstName + " " + obj.lastName == swap_l[0][0]:
            pass_name = True
            passed_index = index
            continue
        index += 1
        stu_lst.insert(END, obj.firstName + " " + obj.lastName)
    stu_lst.pack(side=LEFT, expand=TRUE, fill=BOTH)
    scrollbar.config(command=stu_lst.yview)
    studentFileOpenCount += 1
    stu_lst.bind('<Double-1>', swap_select)

    swap_btn = Button(student_change, text='Swap with selected', command=lambda: swap(swap_l))
    swap_btn.pack(pady=10)


# 1) Open another listbox with students to choose from and have the ability to double click and display that students
# 		attributes.
# 2) Have a confirmation button that when clicked, the swap will be made that will change the two students project IDs
# 3) As the confirmation button is displayed, show possible project/student disagreements by using the two project's
# 		attributes


def move_select(event):
    # Create a new window with the student attributes and 2 buttons to swap projects with another student
    # or move to a different project. Once this is completed, create a new CSV file and return to the user
    newWindow = Toplevel(root)
    newWindow.title("Project")
    newWindow.geometry("800x800")

    projectPicked = proj_lst.curselection()[0]

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


def move(move_l):
    projectPicked = proj_lst.curselection()[0]
    studentlist[move_l[0][1] + 1].projectID = projectlist[projectPicked + 1].projectID
    projid.config(text="Project ID : " + studentlist[move_l[0][1] + 1].projectID)


def moveStudent(move_l):
    global _window_counter, projectFileOpenCount, proj_lst
    if _window_counter == 0:
        global student_change
        student_change = Toplevel(root)
        _window_counter += 1
    else:
        messagebox.showerror("Error", "Due to the limitation, can only open one moving window at a time")
        student_change.lift()

    student_change.geometry("400x400")
    student_change.protocol("WM_DELETE_WINDOW", _delete_window)
    student_change.bind("<Destroy>", _destroy)
    student_change.title("Moving Student")

    scrollbar = Scrollbar(student_change)
    scrollbar.pack(side=RIGHT, expand=TRUE, fill=BOTH)
    proj_lst = Listbox(student_change, yscrollcommand=scrollbar.set)

    #Following line is the title for the listbox. If you change any attributes that are to be displayed.
    #Make sure to change the title to the corresponding attributes that you want.
    #proj_lst.insert(END, "Project Title, Company, Project ID")
    for obj in projectlist[1:]:
        # avoid the first row in the csv that just has titles
        proj_lst.insert(END, obj.projectTitle + " , " + obj.companyName + " , " + obj.projectID)
    proj_lst.pack(side=LEFT, expand=TRUE, fill=BOTH)
    scrollbar.config(command=proj_lst.yview)
    projectFileOpenCount += 1
    proj_lst.bind('<Double-1>', move_select)

    move_btn = Button(student_change, text='move to selected', command=lambda: move(move_l))
    move_btn.pack(pady=10)

#########################################################################################################
################################## Team Irregularity Checking ###########################################
#########################################################################################################
#The following function will be used to find all team sizes, the max/min sized team, and teams that
#do not utilize all of the desired majors for the project assigned.
def team_irregularity():
    # Search through the team file and find teams that are too big, too small, or don't have all of the
    # correct majors assigned for the team by cross checking with the student file.
    #this dictionary will contain the project IDs and the count of how many students are in each
    #project
    if (studentFileOpenCount != 0 and projectFileOpenCount != 0):
        count = {}
        major = {}
        for student in studentlist[1:]:
            #If the projectID is already in the dictionary, increase its count to see how many
            #total student are on the project team. Also add the major of the student as well for 
            #comparision lower in the code
            if student.projectID in count.keys():
                count[student.projectID] = count[student.projectID] + 1
                major[student.projectID].append(student.major.lower())
            #Otherwise, initialize the count. When we initialize, we will also keep track of and initialize what
            #major the student being added is as well
            else:
                count[student.projectID] = 1
                major[student.projectID] = []
                major[student.projectID].append(student.major.lower())

        #open a new window for the irregularities
        newWindow2 = Toplevel(root)
        newWindow2.title("Irregularities")
        newWindow2.geometry("800x400")
        #Split the new irregularities window into two frames, the left side will display the team
        #sizes and the right side will display teams that do not utilize all of the desired majors
        irrFrameLeft = Frame(newWindow2, width = 450)
        irrFrameLeft.pack(side=LEFT, expand=TRUE, fill=BOTH)

        irrFrameRight = Frame(newWindow2, width = 450)
        irrFrameRight.pack(side=RIGHT, expand=TRUE, fill=BOTH)

        #This loop will iterate through the dictionary and display the counts for each
        #project ID and will calculate the min and max team size
        maxSize = 0
        minSize = 20
        for key in count:
            tmp = Label(irrFrameLeft, text= "Project ID " + str(key) + ": " + str(count[key]) + " members")
            tmp.pack(pady=10)
            if maxSize < count[key]:
                maxSize = count[key]
            if minSize > count[key]:
                minSize = count[key]
        #Displays the min and max team sizes
        minTeam = Label(irrFrameLeft, text= "Min team size is " + str(minSize) + " on Project ID " + min(count, key = count.get))
        minTeam.pack(pady=10)
        maxTeam = Label(irrFrameLeft, text= "Max team size is " + str(maxSize) + " on Project ID " + max(count, key = count.get))
        maxTeam.pack(pady=10)

        #Check to make sure the projects are utilizing all of the desired majors.
        #This loop will check to see what majors are needed for each project and
        #append them to a dictionary "needed". This will then be compared with the 
        #"majors" dictionary above to see if all the needed majors are the same as the 
        #current majors on the team
        needed = {}
        for obj in projectlist[1:]:
            for projID in count:
                #We found a project that is being used so append the requireed majors to the dictionary "needed"
                if obj.projectID == projID:
                    needed[projID] = []
                    if obj.bme != "0":
                        needed[projID].append("bme")
                    if obj.cmpen != "0":
                        needed[projID].append("cmpen")
                    if obj.cmpsc != "0":
                        needed[projID].append("cmpsc")
                    if obj.ds != "0":
                        needed[projID].append("ds")
                    if obj.ed != "0":
                        needed[projID].append("ed")
                    if obj.ee != "0":
                        needed[projID].append("ee")
                    if obj.egee != "0":
                        needed[projID].append("egee")
                    if obj.esc != "0":
                        needed[projID].append("esc")
                    if obj.ie != "0":
                        needed[projID].append("ie")
                    if obj.matse != "0":
                        needed[projID].append("matse")
                    if obj.me != "0":
                        needed[projID].append("me")
        #Compare the "needed" and "majors" dictionaries to see if there are any disprecancies between
        #what the project requires for majors and what majors the current students on the team have
        difference = {}
        for proj in needed:
            if proj in major.keys():
                #Compare the majors for the project
                difference[proj] = [item for item in needed[proj] if item not in major[proj]]
            #The major needed was not found in the current list of students on the team so append
            #This major to the difference list
        for key, value in difference.items():
            majorDifference = Label(irrFrameRight, text= "Majors not utilize for project ID " + key + " are " + str(value))
            majorDifference.pack(pady=10)

                
    else:
        messagebox.showerror("Error", "Missing student or project CSV file")

#########################################################################################################
####################################### CSV Output ######################################################
#########################################################################################################
#The following two functions are used to revert our data structure back to a CSV file.
#When the buttons for student or project output are clicked, it will open your directory and
#you can then save the file as whatwhever you want. Id recommend just overwriting your old file
#(save it as the same name as before) so you dont have a crammed directory.
def student_csv_output():
    if studentFile is not None:
        outputfile = fd.asksaveasfile(mode='w', defaultextension=".csv")
        student_writer = csv.writer(outputfile, lineterminator = '\n')
        student_writer.writerow(['Major', 'ProjectID','TimeA' , 'TimeB' , 'TimeC' , 'Comments' , 'Student_NDA' , 'Student_IP' , 'campus_id' , 'last_name' , 'first_name' , 'OnCampus' , 'Var14'])
        for obj in studentlist[1:]:
            student_writer.writerow([obj.major, obj.projectID, obj.timeA, obj.timeB, obj.timeC, obj.comments, obj.studentNDA, obj.studentIP, obj.campusID, obj.lastName, obj.firstName, obj.onCampus, obj.var14])
    else:
        messagebox.showerror("Error", "Please upload a student csv file first")
def project_csv_output():
    if projectFile is not None:
        outputfile = fd.asksaveasfile(mode='w', defaultextension=".csv")
        project_writer = csv.writer(outputfile, lineterminator = '\n')
        project_writer.writerow(['ProjectID' , 'CompanyName' , 'ProjectTitle' , 'BME' , 'CMPEN' , 'CMPSC' , 'DS' , 'ED' , 'EE' , 'EGEE' , 'ESC' , 'IE' , 'MATSE' , 'ME' , 'Confidentiality' , 'IP' , 'CourseTime' , 'CourseName' , 'PhysicalPrototype'])
        for obj in projectlist[1:]:
            project_writer.writerow([obj.projectID , obj.companyName , obj.projectTitle  , obj.bme , obj.cmpen , obj.cmpsc , obj.ds , obj.ed , obj.ee , obj.egee , obj.esc , obj.ie , obj.matse , obj.me , obj.confidentiality , obj.ip , obj.courseTime , obj.courseName , obj.physicalPrototype])
    else:
        messagebox.showerror("Error", "Please upload a project csv file first")



# All the buttons that are on the homepage in the format Button(root, text, command). Root is used to connect the
# button to the parents window. Text is used to display text on the button. Command is used to call a function when
# the button is clicked.
btn1 = Button(mainFrame, text='Upload Student CSV', command=students_list)
btn2 = Button(mainFrame, text='Upload Project CSV', command=project_list)
btn4 = Button(mainFrame, text='Project Irregularity Test', command=team_irregularity)
btn3 = Button(mainFrame, text='Export Student CSV', command=student_csv_output)
btn5 = Button(mainFrame, text='Export Project CSV', command=project_csv_output)

btn1.pack(pady=10)
btn2.pack(pady=10)
btn4.pack(pady=10)
btn3.pack(pady=10)
btn5.pack(pady=10)

# the main loop that keeps the app running
mainloop()
