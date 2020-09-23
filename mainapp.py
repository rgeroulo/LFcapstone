#importing libraries for GUI, GUI file upload, GUI message pop up
from tkinter import *
from tkinter.filedialog import askopenfile
from tkinter import messagebox
import pandas as pd
from IPython.display import display


#Setting up the GUI window and size of the initial window. The window can be dragged and altered to fit the desired size on the screen.
root = Tk()
root.title("The Learning Factory")
root.geometry('850x700')

#Three different frames are created.
mainFrame = Frame(root)
studentFrame = Frame(root)
projectFrame = Frame(root)

#setting up the text on top of the window 
mainFrameLabel = Label(mainFrame, text= "Learning Factory Dashboard", font = ("Courier", 35))
subTitle = Label(mainFrame, text= "Please upload the proper CSV files to start", font = ("Courier", 20))
studentFrameLabel = Label(studentFrame, text = "Student Search", font = ("Courier", 20))
projectFrameLabel = Label(projectFrame, text = "Project Search", font = ("Courier", 20))

#This will align the frames to their respective parts on the GUI interface.
mainFrame.pack(side = TOP)
studentFrame.pack(side = LEFT, expand = TRUE)
projectFrame.pack(side = RIGHT, expand = TRUE)

#These following lines will pack the labels for each frame so that they are properly displayed.
mainFrameLabel.pack()
subTitle.pack()
studentFrameLabel.pack()
projectFrameLabel.pack()

#functions for the buttons on the home page
#open_student_file and open_project_file allow the user to choose and open the desired CSV file. Upon upload the buttons for student list or project list will pop up
def open_student_file(): 
	global studentFile
	studentFile = askopenfile(mode ='r+', filetypes =[('CSV Files', '*.csv')])
	#btn3.pack(side = TOP, pady = 10) 


def open_project_file(): 
	global projectFile
	projectFile = askopenfile(mode ='r+', filetypes =[('CSV Files', '*.csv')])
	btn4.pack(side = TOP, pady = 10)
	btn5.pack(side = TOP, pady = 10)
 
#student and project list buttons allow the user to go to the list of students and projects in the future. For now it checks if the proper CSV file has been uploaded and shows content of CSV
#file by setting offset at 0 and reading the file, if the file is missing an error will pop up
def students_list():
	if studentFile is not None:
		newWindow = Toplevel(root)
		newWindow.title("Student List Window")
		newWindow.geometry("500x350")
		Label(newWindow, text="This window needs more information").pack()
		studentFile.seek(0)
		content = pd.read_csv(studentFile, delimiter=',')
		#This display(content) is a pd function that displays the dataframe in the terminal.
		# I need to inplement this so it shows in a message box.
		display(content)
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

def openNewWindow():
	newWindow = Toplevel(root)
	newWindow.title("")
	newWindow.geometry("500x350")
	Label(newWindow, text="New Window").pack()




#All the buttons that are on the homepage in the format Button(root, text, command). Root is used to connect the button to the parents window. 
# Text is used to display text on the button. Command is used to call a function when the button is clicked.
btn1 = Button(mainFrame, text ='Upload Student CSV', command = lambda:open_student_file())
btn2 = Button(mainFrame, text ='Upload Project CSV', command = lambda:open_project_file()) 
btn3 = Button(mainFrame, text ='List of Students', command = students_list) 
btn4 = Button(mainFrame, text ='List of Projects', command = project_list)
btn5 = Button(mainFrame, text ='Project Irregularity Test', command = project_list) 

btn1.pack(pady = 10)
btn2.pack(pady = 10)
btn3.pack(pady = 10)
btn4.pack(pady = 10)
btn5.pack(pady = 10)

studentSearchLabel = Label(studentFrame, text = "Student Name:", font = ("Courier", 10))
studentSearchLabel.pack(side = LEFT)
studentSearch = Entry(studentFrame)
studentSearch.pack(side = RIGHT)

projectSearchLabel = Label(projectFrame, text = "Project name:", font = ("Courier", 10))
projectSearchLabel.pack(side = LEFT)
projectSearch = Entry(projectFrame)
projectSearch.pack(side = RIGHT)


#the initial packing of the homepage buttons 3-5 are packed into the homepage upon pressing of buttons 1-2
#mainTitle.pack(side = TOP, pady = 10)
#subTitle.pack(side = TOP, pady = 10)
#btn1.pack(side = TOP, pady = 10) 
#btn2.pack(side = TOP, pady = 10) 


#the main loop that keeps the app running 
mainloop()