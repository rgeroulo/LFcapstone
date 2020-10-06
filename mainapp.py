#importing libraries for GUI, GUI file upload, GUI message pop up
from tkinter import *
from tkinter.filedialog import askopenfile
from tkinter import messagebox
import pandas as pd
from IPython.display import display
from csv import DictReader
from LFparser import parser
from LFparser import projectFileParser


studentFileOpenCount = 0
projectFileOpenCount = 0




#Setting up the GUI window and size of the initial window. The window can be dragged and altered to fit the desired size on the screen.
root = Tk()
root.title("The Learning Factory")
root.geometry('850x700')

#################################################  MAIN FRAME  #################################################
mainFrame = Frame(root)
mainFrame.pack(side = TOP)
mainFrameLabel = Label(mainFrame, text= "Learning Factory Dashboard", font = ("Courier", 35))
mainFrameLabel.pack()
subTitle = Label(mainFrame, text= "Please upload the proper CSV files to start", font = ("Courier", 20))
subTitle.pack()


#################################################  STUDENT FRAME  #################################################
studentFrame = Frame(root)
studentFrame.pack(side = LEFT, expand = TRUE, fill = BOTH)

studentFrameLabel = Label(studentFrame, text = "Student Search", font = ("Courier", 20))
studentFrameLabel.pack(side = TOP)

studentSearchLabel = Label(studentFrame, text = "Student Name:", font = ("Courier", 10))
studentSearchLabel.pack(side = TOP)

studentSearch = Entry(studentFrame)
studentSearch.pack(side = TOP)


#################################################  PROJECT FRAME  #################################################
projectFrame = Frame(root)
projectFrame.pack(side = RIGHT, expand = TRUE, fill = BOTH)

projectFrameLabel = Label(projectFrame, text = "Project Search", font = ("Courier", 20))
projectFrameLabel.pack(side = TOP)

projectSearchLabel = Label(projectFrame, text = "Project name:", font = ("Courier", 10))
projectSearchLabel.pack(side = TOP)

projectSearch = Entry(projectFrame)
projectSearch.pack(side = TOP)

 
#student and project list buttons allow the user to go to the list of students and projects in the future. For now it checks if the proper CSV file has been uploaded and shows content of CSV
#file by setting offset at 0 and reading the file, if the file is missing an error will pop up
def students_list():
	global studentFile
	global studentFileOpenCount
	studentFile = askopenfile(mode ='r+', filetypes =[('CSV Files', '*.csv')])

	if studentFile is not None:
		#calls in parser to create a list of objects from CSV
		studentlist = parser(studentFile)

		#if a prevous CSV is open then the list will be deleted
		if studentFileOpenCount != 0:
			scrollbar.delete("1.0", tk.END)

		#the scrollbar is implemented and filled with content 
		scrollbar = Scrollbar(studentFrame)
		scrollbar.pack(side = RIGHT, expand = TRUE, fill = BOTH)
		lst = Listbox(studentFrame, yscrollcommand = scrollbar.set)
		for obj in studentlist[1:]:
			#avoid the first row in the csv that just has titles
			#add the student's first and last name to the listbox
			lst.insert(END, obj.firstName + " " + obj.lastName)
		lst.pack(side = LEFT, expand = TRUE, fill = BOTH)
		scrollbar.config( command = lst.yview )
		studentFileOpenCount += 1
		lst.bind('<Double-1>', student_select)
		#studentFile.seek(0)
	else:
		messagebox.showerror("Error", "No student CSV file detected")


def project_list():
	global projectFile
	global projectFileOpenCount
	projectFile = askopenfile(mode ='r+', filetypes =[('CSV Files', '*.csv')])

	if projectFile is not None:
		#calls in parser to create a list of objects from CSV
		projectlist = projectFileParser(projectFile)

		#if a prevous CSV is open then the list will be deleted
		if projectFileOpenCount != 0:
			scrollbar.delete("1.0", tk.END)

		#the scrollbar is implemented and filled with content 
		scrollbar = Scrollbar(projectFrame)
		scrollbar.pack(side = RIGHT, expand = TRUE, fill = BOTH)
		lst = Listbox(projectFrame, yscrollcommand = scrollbar.set)
		for obj in projectlist[1:]:
			#avoid the first row in the csv that just has titles
			lst.insert(END, obj.projectTitle)
		lst.pack(side = LEFT, expand = TRUE, fill = BOTH)
		scrollbar.config( command = lst.yview )
		projectFileOpenCount += 1
		lst.bind('<Double-1>', project_select)
		#projectFile.seek(0)
	else:
		messagebox.showerror("Error", "No project CSV file detected")


def student_select(event):
	#Create a new window with the student attributes and 2 buttons to swap projects with another student
	#or move to a different project. Once this is completed, create a new CSV file and return to the user
	newWindow = Toplevel(root)
	newWindow.title("Student")
	newWindow.geometry("400x400")
	Label(newWindow, text = "Student window").pack()

	btn1 = Button(newWindow, text ='Swap teams with another student')
	btn2 = Button(newWindow, text ='Move to a different team') 
	btn1.pack(pady = 10)
	btn2.pack(pady = 10)

def project_select(event):
	#Create a new window with the student attributes and 2 buttons to swap projects with another student
	#or move to a different project. Once this is completed, create a new CSV file and return to the user
	newWindow = Toplevel(root)
	newWindow.title("Project")
	newWindow.geometry("400x400")
	Label(newWindow, text = "Project window").pack()

	btn1 = Button(newWindow, text ='Swap teams with another student')
	btn2 = Button(newWindow, text ='Move to a different team') 
	btn1.pack(pady = 10)
	btn2.pack(pady = 10)

	person = lst.get(lst.curselection())
	
	


def team_irregularity():
	#Search through the team file and find teams that are too big, too small, or dont have all of the 
	#correct majors assigned for the team by cross checking with the student file.
	print('hi')




#All the buttons that are on the homepage in the format Button(root, text, command). Root is used to connect the button to the parents window. 
# Text is used to display text on the button. Command is used to call a function when the button is clicked.
btn1 = Button(mainFrame, text ='Upload Student CSV', command = students_list)
btn2 = Button(mainFrame, text ='Upload Project CSV', command = project_list) 
btn4 = Button(mainFrame, text ='Project Irregularity Test', command = project_list)
btn5 = Button(mainFrame, text ='Generate PDF', command = project_list) 

btn1.pack(pady = 10)
btn2.pack(pady = 10)
btn4.pack(pady = 10)
btn5.pack(pady = 10)


#the main loop that keeps the app running 
mainloop()