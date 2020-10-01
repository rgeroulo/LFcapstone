<<<<<<< HEAD
#This returns a list of lists with no headers
#import pandas as pd
#content = pd.read_csv("test.csv", delimiter=',')
#lst = [list(row) for row in content.values]
#print(lst)

#The student class contains all the attributes that a student would have.
class Students:
    def __init__(self, Major = '', ProjectID = '', TimeA = '',TimeB = '', TimeC = '', Comments = '', Student_NDA = '', Student_IP = '', campus_id = '', last_name = '', first_name = '', OnCampus = '',Var14 = ''):
        self.major = Major
        self.projectID = ProjectID
        self.timeA = TimeA
        self.timeB = TimeB
        self.timeC = TimeC
        self.comments = Comments
        self.studentNDA = Student_NDA
        self.studentIP = Student_IP
        self.campusID = campus_id
        self.lastName = last_name
        self.firstName = first_name
        self.onCampus = OnCampus
        self.var14 = Var14

#This returns a list of dictionaries
import csv
people = []
with open('test.csv', 'r') as file:
    reader = csv.reader(file, delimiter = ',')
    for line in reader:
        for row in line:
            print(row)
            people.append({'major': row[1], 'projectID': row[2], 'timeA': row[3], 'timeB': row[4], 'timeC': row[5], 'comments': row[6], 'studentNDA': row[7], 'studentIP': row[8], 'campusID': row[9],
            'lastName': row[10], 'firstName': row[11], 'onCampus': row[12], 'var14': row[0]})

print(people)



=======
#The student class contains all the attributes that a student would have.
class Students:
    def __init__(self, Major = '', ProjectID = '', TimeA = '',TimeB = '', TimeC = '', Comments = '', Student_NDA = '', Student_IP = '', campus_id = '', last_name = '', first_name = '', OnCampus = '',Var14 = ''):
        self.major = Major
        self.projectID = ProjectID
        self.timeA = TimeA
        self.timeB = TimeB
        self.timeC = TimeC
        self.comments = Comments
        self.studentNDA = Student_NDA
        self.studentIP = Student_IP
        self.campusID = campus_id
        self.lastName = last_name
        self.firstName = first_name
        self.onCampus = OnCampus
        self.var14 = Var14



>>>>>>> 01ee2d04a3399757257cd99007038501b21d5a7f
