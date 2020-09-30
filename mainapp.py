#importing libraries for GUI, GUI file upload, GUI message pop up
from tkinter import *
from tkinter.filedialog import askopenfile
from tkinter import messagebox
import pandas as pd
from IPython.display import display
from csv import DictReader
from LFparser import parser


studentFileOpenCount = 0



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



#functions for the buttons on the home page
#open_student_file and open_project_file allow the user to choose and open the desired CSV file. Upon upload the buttons for student list or project list will pop up
#def open_student_file(): 
	#global studentFile
	#studentFile = askopenfile(mode ='r+', filetypes =[('CSV Files', '*.csv')])
	#btn3.pack(side = TOP, pady = 10) 


def open_project_file(): 
	global projectFile
	projectFile = askopenfile(mode ='r+', filetypes =[('CSV Files', '*.csv')])
	#btn4.pack(side = TOP, pady = 10)
	#btn5.pack(side = TOP, pady = 10)
 
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
		for obj in studentlist:
			if obj.major != "Major":
				lst.insert(END, obj.firstName + " " + obj.lastName)
		lst.pack(side = LEFT, expand = TRUE, fill = BOTH)
		scrollbar.config( command = lst.yview )
		studentFileOpenCount += 1
		studentFile.seek(0)
		#This display(content) is a pd function that displays the dataframe in the terminal.
		# I need to inplement this so it shows in a message box.
		#display(content)
	else:
		messagebox.showerror("Error", "No student CSV file detected")


def project_list():
	if projectFile is not None:
		projectFile.seek(0)
		content = pd.read_csv(projectFile, delimiter=',')
		#This display(content) is a pd function that displays the dataframe in the terminal.
		# I need to inplement this so it shows in a message box.
		display(content)
	else:
		messagebox.showerror("Error", "No project CSV file detected")




#All the buttons that are on the homepage in the format Button(root, text, command). Root is used to connect the button to the parents window. 
# Text is used to display text on the button. Command is used to call a function when the button is clicked.
btn1 = Button(mainFrame, text ='Upload Student CSV', command = students_list)
btn2 = Button(mainFrame, text ='Upload Project CSV', command = lambda:open_project_file()) 
#btn3 = Button(mainFrame, text ='List of Students', command = students_list) 
btn4 = Button(mainFrame, text ='Project Irregularity Test', command = project_list)
btn5 = Button(mainFrame, text ='Generate PDF', command = project_list) 

btn1.pack(pady = 10)
btn2.pack(pady = 10)
#btn3.pack(pady = 10)
btn4.pack(pady = 10)
btn5.pack(pady = 10)


#the initial packing of the homepage buttons 3-5 are packed into the homepage upon pressing of buttons 1-2
#mainTitle.pack(side = TOP, pady = 10)
#subTitle.pack(side = TOP, pady = 10)
#btn1.pack(side = TOP, pady = 10) 
#btn2.pack(side = TOP, pady = 10) 


#the main loop that keeps the app running 
mainloop()