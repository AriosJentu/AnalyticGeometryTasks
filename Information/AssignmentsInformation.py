import Scripts.Assignments as Assignments
AssignmentsInformation = Assignments.AssignmentsInformationClass()

#Imports 
from .Homework import Homework1
from .Homework import Homework2

#Append assignments into Assignments Information List
AssignmentsInformation.append(Homework1.Homework1, "h")
AssignmentsInformation.append(Homework2.Homework2, "h")
