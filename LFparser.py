from dataStructures import Students
from dataStructures import Projects
import csv


# this function will take in a CSV file and give out a list filled with student objects
def parser(studentFile):
    people = []
    if studentFile is not None:
        reader = csv.reader(studentFile, delimiter=',')
        for line in reader:
            people.append(
                Students(line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7], line[8], line[9],
                         line[10], line[11], line[12]))
    return people


def projectFileParser(projectFile):
    people = []
    if projectFile is not None:
        reader = csv.reader(projectFile, delimiter=',')
        for line in reader:
            people.append(
                Projects(line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7], line[8], line[9],
                         line[10], line[11], line[12], line[13], line[14], line[15], line[16],
                         line[17], line[18]))
    return people
