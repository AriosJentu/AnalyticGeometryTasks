import random

from ..Default import Exam
import Modules.Imports as Imports

from ..Scripts import Lines
from ..Scripts import TextReplacer

control_event = "Экзаменационный вариант"
event_number = 1

prefix = "Tasks/Comission/"

def tasks_updater(text):
	random.seed()

	line = Lines.Line(3)
	plane = Lines.HyperPlane(3)

	line.generate_random_line_points()
	text = text.replace("#LINE#", line.to_random_form())

	plane.generate_random_plane_points()
	text = text.replace("#PLANE1#", plane.to_random_form())

	plane.generate_random_plane_points()
	text = text.replace("#PLANE2#", plane.to_random_form())

	for i in range(4):
		pt = f"#POINT{i+1}#"
		text = text.replace(pt, Lines.Point.generate_random_point(3).to_str(
			Lines.generate_point_name()
		))

	text = TextReplacer.text_replacer(text)

	return text

tasks1 = Imports.Tasks.SpecificTasks()
task1 = Imports.Tasks.SpecificTaskInfo(prefix+f"Task1.tex")
task1.set_updater_function(tasks_updater)
tasks1.append(task1)

tasks2 = Imports.Tasks.SpecificTasks()
task2 = Imports.Tasks.SpecificTaskInfo(prefix+f"Task2.tex")
task2.set_updater_function(tasks_updater)
tasks2.append(task2)

tasks3 = Imports.Tasks.SpecificTasks()
task3 = Imports.Tasks.SpecificTaskInfo(prefix+f"Task3.tex")
task3.set_updater_function(tasks_updater)
tasks3.append(task3)

tasks = [tasks1, tasks2, tasks3]

tasksinfo = []
for task in tasks:
	taskinfo = [Imports.Tasks.TasksInformation(task)]
	tasksinfo.append(taskinfo)

exercises = []
for taskinfo in tasksinfo:
	exercise = Imports.Exercises.Exercise(taskinfo)
	exercises.append(exercise)

class Comission(Imports.Assignments.Assignment):

	layout = Imports.Documents.DocumentLayout(Exam.LayoutLocation, Exam.PageStyle)
	test = Imports.Tests.Test(exercises)
	document_entries = Imports.Entries.DocumentEntries(control_event=control_event, event_number=event_number)
	prefix = "ageom_comission"
	number = event_number
