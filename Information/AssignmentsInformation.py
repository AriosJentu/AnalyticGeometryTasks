import Scripts.Assignments as Assignments
AssignmentsInformation = Assignments.AssignmentsInformationClass()

#Imports 
from .Homework import Homework1
from .Homework import Homework2
from .Homework import Homework3

#Append assignments into Assignments Information List
AssignmentsInformation.append(Homework1.Homework1, "h")
AssignmentsInformation.append(Homework2.Homework2, "h")
AssignmentsInformation.append(Homework3.Homework3, "h")
