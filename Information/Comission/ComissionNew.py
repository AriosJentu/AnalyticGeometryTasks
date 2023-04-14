import random

from ..Default import Exam
import Modules.Imports as Imports

from ..Scripts import Lines
from ..Scripts import TextReplacer

from ..Controls.Control1 import tasks_updater as lines_tasks_updater 
from ..Controls.Control1 import task1_updater as lines_task1_updater 

from ..Controls.Control2 import tasks_updater as seconds_tasks_updater 

from ..Controls.Control3 import tasks_updater as transfs_tasks_updater 

control_event = "Повторная промежуточная аттестация"
event_number = 2
prefix = "Tasks/"

tasks = []

tasks1 = Imports.Tasks.SpecificTasks()
task11 = Imports.Tasks.SpecificTaskInfo(f"{prefix}Linears/Task1.tex")
task12 = Imports.Tasks.SpecificTaskInfo(f"{prefix}Exam/Task1/Variant1.tex")
task13 = Imports.Tasks.SpecificTaskInfo(f"{prefix}Exam/Task1/Variant2.tex")
task14 = Imports.Tasks.SpecificTaskInfo(f"{prefix}Exam/Task1/Variant3.tex")
task15 = Imports.Tasks.SpecificTaskInfo(f"{prefix}Exam/Task1/Variant4.tex")
task16 = Imports.Tasks.SpecificTaskInfo(f"{prefix}Exam/Task2/Variant1.tex")
task17 = Imports.Tasks.SpecificTaskInfo(f"{prefix}Exam/Task2/Variant3.tex")
task11.set_updater_function(lines_task1_updater)
task12.set_updater_function(lines_tasks_updater)
task13.set_updater_function(lines_tasks_updater)
task14.set_updater_function(lines_tasks_updater)
task15.set_updater_function(lines_tasks_updater)
task16.set_updater_function(lines_tasks_updater)
task17.set_updater_function(lines_tasks_updater)

tasks1.append(task11)
tasks1.append(task12)
tasks1.append(task13)
tasks1.append(task14)
tasks1.append(task15)
tasks1.append(task16)
tasks1.append(task17)
tasks.append(tasks1)

tasks2 = Imports.Tasks.SpecificTasks()
task21 = Imports.Tasks.SpecificTaskInfo(f"{prefix}Seconds/Task1/Variant1.tex")
task22 = Imports.Tasks.SpecificTaskInfo(f"{prefix}Seconds/Task1/Variant2.tex")
task23 = Imports.Tasks.SpecificTaskInfo(f"{prefix}Seconds/Task2/Variant1.tex")
task24 = Imports.Tasks.SpecificTaskInfo(f"{prefix}Seconds/Task2/Variant2.tex")
task25 = Imports.Tasks.SpecificTaskInfo(f"{prefix}Seconds/Task3/Variant1.tex")
task26 = Imports.Tasks.SpecificTaskInfo(f"{prefix}Seconds/Task3/Variant2.tex")
task21.set_updater_function(seconds_tasks_updater)
task22.set_updater_function(seconds_tasks_updater)
task23.set_updater_function(seconds_tasks_updater)
task24.set_updater_function(seconds_tasks_updater)
task25.set_updater_function(seconds_tasks_updater)
task26.set_updater_function(seconds_tasks_updater)

tasks2.append(task21)
tasks2.append(task22)
tasks2.append(task23)
tasks2.append(task24)
tasks2.append(task25)
tasks2.append(task26)
tasks.append(tasks2)

tasks3 = Imports.Tasks.SpecificTasks()
task31 = Imports.Tasks.SpecificTaskInfo(f"{prefix}Exam/Task4.tex")
task32 = Imports.Tasks.SpecificTaskInfo(f"{prefix}Exam/Task3/Variant2.tex")
task31.set_updater_function(transfs_tasks_updater)
task32.set_updater_function(transfs_tasks_updater)
tasks3.append(task31)
tasks3.append(task32)
tasks.append(tasks3)

task = Imports.Tasks.EmptyTask()
tasks.append(task)

tasksinfo = []
for index, task in enumerate(tasks):
	n = 2 if index < 2 else 1
	taskinfo = [Imports.Tasks.TasksInformation(task, n)]
	tasksinfo.append(taskinfo)

exercises = []
for index, taskinfo in enumerate(tasksinfo):
	exercise = Imports.Exercises.Exercise(taskinfo)
	if index == len(tasksinfo) - 1:
		exercise = Imports.Exercises.Exercise(taskinfo, title="Теоретический вопрос")

	exercises.append(exercise)

class ComissionNew(Imports.Assignments.Assignment):

	layout = Imports.Documents.DocumentLayout(Exam.LayoutLocation, Exam.PageStyle)
	test = Imports.Tests.Test(exercises)
	document_entries = Imports.Entries.DocumentEntries(control_event=control_event, event_number=event_number)
	prefix = "ageom_comission"
	number = event_number

