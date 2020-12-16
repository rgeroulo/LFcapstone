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

#########################################################################################################
############################### Student and project searching ###########################################
#########################################################################################################
def student_search(event):
    # Enter a student's name, major, or project ID in the search abar and hit enter. This will filter out other students' names
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


def swap_search(event):
    # Enter a student's name, major, or project ID in the search bar and hit enter. This will filter out other students' names
    # and only show relevant students. These desired students will be in the listbox. To go back to the full
    #list, hit enter on an empty search box and it will revert back to the start. This serach supports partial
    #name searching as well so you dont have to type the whole name

    global swap_filter
    swap_filter = []
    filter = event.widget.get().lower()
    cursor = 0
    #This line deletes the line in the csv that has the labels
    stu_lst.delete(0, END)
    for obj in studentlist[1:]:
        if filter in obj.lastName.lower() or filter in obj.firstName.lower() or filter in obj.major.lower() or filter in obj.projectID.lower():
            swap_filter.append((obj.firstName + ' ' + obj.lastName + ' ' + obj.major + ' ' + obj.projectID, cursor))
            stu_lst.insert(END, obj.firstName + " " + obj.lastName + " , " + obj.major + " , " + obj.projectID)
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
    for obj in projectlist[1:]:
        if filter in obj.projectTitle.lower() or filter in obj.projectID.lower() or filter in obj.companyName.lower():
            project_filter.append((obj.projectTitle + ' ' + obj.projectID + ' ' + obj.companyName, cursor))
            projlst.insert(END, obj.projectTitle + " , " + obj.projectID + " , " + obj.companyName)
            cursor += 1
        else:
            cursor += 1
            continue

#########################################################################################################
################################## Initial window creation ###########################################
#########################################################################################################

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
subTitle = Label(mainFrame, text="Please upload both CSV files to start", font=("Courier", 20))
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

#########################################################################################################
###################### Displaying students and projects after CSV input #################################
#########################################################################################################
#students_list will be used to display the students in a listbox in the bottom left corner
#after the student CSV file is uploaded using the button in the middle of the GUI. This will
#generate a scroll bar as well.
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
        scrollbar.pack(side=RIGHT, fill = Y)
        labeling = Label(studentFrame, text="Ordering: FirstName LastName , Major, Project ID")
        labeling.pack(side=TOP)
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
        scrollbar.pack(side=RIGHT, fill=Y)
        labeling = Label(projectFrame, text="Ordering: Project Title , Project ID, Company Name")
        labeling.pack(side=TOP)
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

#########################################################################################################
####################### Student or Project selected from initial widnow #################################
#########################################################################################################

#This is the window that comes up after you double click on a student
#The searching for students will support parital names,
#just first name, just last name, major, 
def student_select(event):
    global projid
    global newWindow

    newWindow = Toplevel(root)
    newWindow.title("Student")
    newWindow.geometry("400x400")
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
    newWindow.geometry("400x550")

    #projectPicked = projlst.curselection()
    #projectPicked = projectPicked[0]
    filtered = len(projectSearch.get()) != 0
    if filtered:
        projectPicked = project_filter[projlst.curselection()[0]][1]
    else:
        projectPicked = projlst.curselection()[0]
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
    desiredMajors = Label(newWindow, text="Majors Desired : " + str(needed))

    name.pack(pady=10)
    company.pack(pady=10)
    projid.pack(pady=10)
    confid.pack(pady=10)
    ip.pack(pady=10)
    courseName.pack(pady=10)
    courseTime.pack(pady=10)
    physPrototype.pack(pady=10)
    desiredMajors.pack(pady=10)

#########################################################################################################
################################## Window destroy functions #############################################
#########################################################################################################
#Used to delete windows when they are conclused
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

#########################################################################################################
#################################### Student swapping  ##################################################
#########################################################################################################
#This is the window that will open when you double click on a student in the swap window. It will display
#the attributes of the stduent.
def swap_select(event):
    newWindow = Toplevel(root)
    newWindow.title("Student")
    newWindow.geometry("400x400")
    Label(newWindow, text="Student window").pack()

    studentPicked = stu_lst.curselection()[0]

    filtered = len(searchBar.get()) != 0
    if filtered:
        studentPicked = swap_filter[stu_lst.curselection()[0]][1]
    else:
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

#This function will preform the swap and change the student project IDs 
def swap(swap_l):
    studentPicked = stu_lst.curselection()[0]
    if pass_name:
        studentPicked += 1
    swap_l.append((stu_lst.selection_get(), studentPicked))
    student_info_one = swap_l[0][0].split(',')
    student_name_one = student_info_one[0].split()
    student_info_two = swap_l[1][0].split(',')
    student_name_two = student_info_two[0].split()
    for studentone in studentlist:
        if (studentone.firstName == student_name_one[0] and studentone.lastName == student_name_one[1]):
            break;
    for studenttwo in studentlist:
        if (studenttwo.firstName == student_name_two[0] and studenttwo.lastName == student_name_two[1]):
            break;
    swap_id = studentone.projectID
    swap_id_two = studenttwo.projectID
    studentone.projectID = studenttwo.projectID
    studenttwo.projectID = swap_id
    projid.config(text="Project ID : " + swap_id_two)
    studentlst.delete(0, END)
    for obj in studentlist[1:]:
        studentlst.insert(END, obj.firstName + " " + obj.lastName + " , " + obj.major + " , " + obj.projectID)
    _delete_window()
    newWindow.destroy()

#This is the window that will open when you have selected a student and then have hit the "swap" 
#button to choose another student to swap with.
def swapStudents(swap_l):
    global _window_counter, studentFileOpenCount, stu_lst, pass_name, passed_index, searchBar
    if _window_counter == 0:
        global student_change
        student_change = Toplevel(root)
        _window_counter += 1
    else:
        messagebox.showerror("Error", "Due to the limitation, can only open one swapping window at a time")
        student_change.lift()

    student_change.protocol("WM_DELETE_WINDOW", _delete_window)
    student_change.bind("<Destroy>", _destroy)
    student_change.title("Swapping Two Students")
    student_change.geometry("400x400")

    #Implement a search bar for the listbox
    searchBar = Entry(student_change)
    searchBar.bind('<Return>', swap_search)
    searchBar.pack(side=TOP)

    #Implement a scrollnbar for the listbox
    scrollbar = Scrollbar(student_change)
    scrollbar.pack(side=RIGHT, fill=Y)
    stu_lst = Listbox(student_change, yscrollcommand=scrollbar.set)

    #Fill the listbox with the students names
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
        stu_lst.insert(END, obj.firstName + " " + obj.lastName + ", " + obj.major + ", " + obj.projectID)
    stu_lst.pack(side=LEFT, expand=TRUE, fill=BOTH)
    scrollbar.config(command=stu_lst.yview)
    studentFileOpenCount += 1
    stu_lst.bind('<Double-1>', swap_select)

    confirmBtn = Button(student_change, text='Confirm Swap', command=lambda: swap(swap_l))
    confirmBtn.pack(pady=10)

#########################################################################################################
##################################### Student moving ####################################################
#########################################################################################################

#move_select will just display the project attributes when you double click on a project when you are moving
#a student to a new team
def move_select(event):
    newWindow = Toplevel(root)
    newWindow.title("Project")
    newWindow.geometry("400x400")

    projectPicked = proj_lst.curselection()[0]

    name = Label(newWindow, text=projectlist[projectPicked + 1].projectTitle)
    company = Label(newWindow, text="Company : " + projectlist[projectPicked + 1].companyName)
    projid = Label(newWindow, text="Project ID : " + projectlist[projectPicked + 1].projectID)
    confid = Label(newWindow, text="Confidentiality? " + projectlist[projectPicked + 1].confidentiality)
    ip = Label(newWindow, text="IP : " + projectlist[projectPicked + 1].ip)
    courseName = Label(newWindow, text="Course Name: " + projectlist[projectPicked + 1].courseName)
    courseTime = Label(newWindow, text="Course Time: " + projectlist[projectPicked + 1].courseTime)
    physPrototype = Label(newWindow, text="Physical Prototype? " + projectlist[projectPicked + 1].physicalPrototype)

    name.pack(pady=10)
    company.pack(pady=10)
    projid.pack(pady=10)
    confid.pack(pady=10)
    ip.pack(pady=10)
    courseName.pack(pady=10)
    courseTime.pack(pady=10)
    physPrototype.pack(pady=10)

#move will preform the move operation by changing the students project ID to the new chosen project
def move(move_l):
    projectPicked = proj_lst.curselection()[0]
    student_info = move_l[0][0].split(',')
    student_name = student_info[0].split()
    for student in studentlist:
        if (student.firstName == student_name[0] and student.lastName == student_name[1]):
            student.projectID = projectlist[projectPicked + 1].projectID
            break;
    projid.config(text="Project ID : " + projectlist[projectPicked + 1].projectID)
    studentlst.delete(0, END)
    for obj in studentlist[1:]:
        studentlst.insert(END, obj.firstName + " " + obj.lastName + " , " + obj.major + " , " + obj.projectID)
    _delete_window()


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
    scrollbar.pack(side=RIGHT, fill=Y)
    proj_lst = Listbox(student_change, yscrollcommand=scrollbar.set)

    #Following line is the title for the listbox. If you change any attributes that are to be displayed.
    #Make sure to change the title to the corresponding attributes that you want.
    for obj in projectlist[1:]:
        # avoid the first row in the csv that just has titles
        proj_lst.insert(END, obj.projectTitle + " , " + obj.companyName + " , " + obj.projectID)
    proj_lst.pack(side=LEFT, expand=TRUE, fill=BOTH)
    scrollbar.config(command=proj_lst.yview)
    projectFileOpenCount += 1
    proj_lst.bind('<Double-1>', move_select)

    move_btn = Button(student_change, text='Confirm Move', command=lambda: move(move_l))
    move_btn.pack(pady=10)

#########################################################################################################
################################## Team irregularity checking ###########################################
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

        #)pen a new window
        newWindow2 = Toplevel(root)
        newWindow2.title("Irregularity Test")
        newWindow2.geometry("1200x600")

        #Split the new irregularities window into multiple frames. Each frame will hold a different 
        #irregularity test
        irrFrameLeft = Frame(newWindow2, width = 450)
        irrFrameLeft.pack(side=LEFT, expand=TRUE, fill=BOTH)

        irrFrameMid = Frame(newWindow2, width = 450)
        irrFrameMid.pack(side=LEFT, expand=TRUE, fill=BOTH)

        irrFrameMid2 = Frame(newWindow2, width = 450)
        irrFrameMid2.pack(side=LEFT, expand=TRUE, fill=BOTH)

        irrFrameRight = Frame(newWindow2, width = 450)
        irrFrameRight.pack(side=RIGHT, expand=TRUE, fill=BOTH)

        #Label for the left most frame which has the team sizes
        sizeLabel = Label(irrFrameLeft, text= "TEAM SIZE", font = (15))
        sizeLabel.pack(pady=10)

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
        #what the project requires for majors and what majors the current students on the team have.
        #We will then display the majors that are needed but not on the team yet.
        stillNeeded = {}
        for proj in needed:
            if proj in major.keys():
                #Compare the majors for the project
                stillNeeded[proj] = [item for item in needed[proj] if item not in major[proj]]
                
        #Check to see if there are nonrequired majors on the same project ID, if so, this can be useful
        #for changing teams for you will know there are dispensable students on a team
        extraNonNeeded = {}
        for proj in major:
            #If the projects majors are not in the needed majors dictionary, then add them to extraNonNeeded
            extraNonNeeded[proj] = list(set(major[proj]) - set(needed[proj]))

        #Check to see if there are multiple required majors on the same project ID, if so, this can be useful
        #for changing teams for you will know there are dispensable students on a team
        extraNeededMajors = {}
        tmp = {}
        for proj in needed:
            total = {}
            #Iterate through the needed majors for each project. Check to see how many occurances there
            #are of the needed item in the current team. Add this number to total. This can help to show that there are
            #multiple majors on a team that can be divided to other teams if needed.
            for item in needed[proj]:
                total[item] = major[proj].count(item)
            #Add the counts of each major to the tmp dictioanry. tmp is a dictionary of dictionarys that holds the
            #key = projectID value = a dictionary of majors to total total
            tmp[proj] = total
        
        for proj, value in tmp.items():
            extraNeededMajors[proj] = []
            for key in value:
                #If there are more than 1 required major for the class, display that info
                if value[key] > 1:
                    extraNeededMajors[proj].append(key)




        #These are the top labels for the irregularity tests
        stillNeededLabel = Label(irrFrameMid, text= "MAJORS STILL REQUIRED", font = (15))
        stillNeededLabel.pack(pady=10)

        nonNeededExtraLabel = Label(irrFrameMid2, text = "EXTRA NON-REQUIRED MAJORS", font = (15))
        nonNeededExtraLabel.pack(pady=10)

        neededExtraLabel = Label(irrFrameRight, text = "EXTRA REQUIRED MAJORS", font = (15))
        neededExtraLabel.pack(pady=10)

        #Iterate through each dictionary and print the key and values pairs in a label so that the user
        #can easily read and use the data
        for key, value in stillNeeded.items():
            majorStillNeeded = Label(irrFrameMid, text= "Project ID " + key + " does not have a " + str(value))
            majorStillNeeded.pack(pady=10)

        for key, value in extraNonNeeded.items():
            majorNonNeeded = Label(irrFrameMid2, text= "Project ID " + key + " does not need the " + str(value))
            majorNonNeeded.pack(pady=10)

        for key, value in extraNeededMajors.items():
            majorExtra = Label(irrFrameRight, text= "Project ID " + key + " has extra required " + str(value))
            majorExtra.pack(pady=10)

                
    else:
        messagebox.showerror("Error", "Missing student or project CSV file")

#########################################################################################################
####################################### CSV output ######################################################
#########################################################################################################
#The following function is used to revert our data structure back to a CSV file.
#When the button for save student csv is clicked, it will open your directory and
#you can then save the file as whatwhever you want. Id recommend just overwriting your old file
#name to save it as the same name so you dont have a crammed directory.
def student_csv_output():
    if studentFile is not None:
        outputfile = fd.asksaveasfile(mode='w', defaultextension=".csv")
        student_writer = csv.writer(outputfile, lineterminator = '\n')
        student_writer.writerow(['Major', 'ProjectID','TimeA' , 'TimeB' , 'TimeC' , 'Comments' , 'Student_NDA' , 'Student_IP' , 'campus_id' , 'last_name' , 'first_name' , 'OnCampus' , 'Var14'])
        for obj in studentlist[1:]:
            student_writer.writerow([obj.major, obj.projectID, obj.timeA, obj.timeB, obj.timeC, obj.comments, obj.studentNDA, obj.studentIP, obj.campusID, obj.lastName, obj.firstName, obj.onCampus, obj.var14])
    else:
        messagebox.showerror("Error", "Please upload a student csv file first")



# All the buttons that are on the homepage in the format Button(root, text, command). Root is used to connect the
# button to the parents window. Text is used to display text on the button. Command is used to call a function when
# the button is clicked.
btn1 = Button(mainFrame, text='Upload Student CSV', command=students_list)
btn2 = Button(mainFrame, text='Upload Project CSV', command=project_list)
btn4 = Button(mainFrame, text='Team Irregularity Test', command=team_irregularity)
btn3 = Button(mainFrame, text='Save Student CSV', command=student_csv_output, bg = 'yellow')

btn1.pack(pady=10)
btn2.pack(pady=10)
btn4.pack(pady=10)
btn3.pack(pady=10)

# the main loop that keeps the app running
mainloop()
