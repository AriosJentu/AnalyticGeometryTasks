import Scripts.Assignments as Assignments
AssignmentsInformation = Assignments.AssignmentsInformationClass()

#Imports 
from .Homework import Homework1
from .Homework import Homework2
from .Homework import Homework3
from .Controls import Control1
from .Controls import Control2
from .Controls import Control3
from .Controls import Control4
from .Exam import Exam
from .Comission import Comission

#Append assignments into Assignments Information List
AssignmentsInformation.append(Homework1.Homework1, "h")
AssignmentsInformation.append(Homework2.Homework2, "h")
AssignmentsInformation.append(Homework3.Homework3, "h")
AssignmentsInformation.set_description("h", "Homework tasks for analytic geometry course")

AssignmentsInformation.append(Control1.Control1, "c")
AssignmentsInformation.append(Control2.Control2, "c")
AssignmentsInformation.append(Control3.Control3, "c")
AssignmentsInformation.append(Control4.Control4, "c")
AssignmentsInformation.set_description("c", "Control tasks for analytic geometry course")

AssignmentsInformation.append(Exam.Exam, "e")
AssignmentsInformation.set_description("e", "Exam tasks of analytic geometry course")

AssignmentsInformation.append(Comission.Comission, "k")
AssignmentsInformation.set_description("k", "Comission tasks")