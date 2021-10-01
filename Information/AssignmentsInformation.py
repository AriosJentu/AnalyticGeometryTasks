import Scripts.Assignments as Assignments
AssignmentsInformation = Assignments.AssignmentsInformationClass()

#Imports 
from .Homework import Homework1

#Append assignments into Assignments Information List
AssignmentsInformation.append(Homework1.Homework1, "h")
