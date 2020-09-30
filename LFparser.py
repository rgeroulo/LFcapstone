from studentDataStructure import Students
import csv

#this function will take in a CSV file and give out a list filled with student objects
def parser(studentFile):
  people = []
  if studentFile is not None:
    reader = csv.reader(studentFile, delimiter = ',')
    for line in reader:
      people.append( Students(line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7], line[8], line[9], line[10], line[11], line[12]))
  return people
  



        

