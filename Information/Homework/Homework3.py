import random

from ..Default import Homework
import Modules.Imports as Imports

from ..Scripts import Lines
from ..Scripts import TextReplacer

control_event = "Индивидуальное домашнее задание"
event_number = 3

prefix = "Tasks/Homework3/"

def tasks_updater(text):
	line = Lines.Line(3)
	plane = Lines.HyperPlane(3)

	line.generate_random_line_points()
	text = text.replace("#LINEPOINTS#", line.to_points_form())

	plane.generate_random_plane_points()
	text = text.replace("#PLANEPOINTS#", plane.to_points_form())
	
	line.generate_random_line_points()
	text = text.replace("#LINE1#", line.to_random_form())
	
	line.generate_random_line_points()
	text = text.replace("#LINE2#", line.to_random_form())
	
	plane.generate_random_plane_points()
	text = text.replace("#PLANE1#", plane.to_random_form())
	
	plane.generate_random_plane_points()
	text = text.replace("#PLANE2#", plane.to_random_form())
	
	text = text.replace("#POINT#", Lines.Point.generate_random_point(3).to_str(
		Lines.generate_point_name()
	))

	text = TextReplacer.text_replacer(text)

	return text

tasks = []
for i in range(6):
	tasks_i = Imports.Tasks.SpecificTasks()
	task_i = Imports.Tasks.SpecificTaskInfo(prefix+f"Task{i+1}.tex")
	task_i.set_updater_function(tasks_updater)
	tasks_i.append(task_i)
	tasks.append(tasks_i)

tasksinfo = []
for task in tasks:
	taskinfo = [Imports.Tasks.TasksInformation(task)]
	tasksinfo.append(taskinfo)

exercises = []
for taskinfo in tasksinfo:
	exercise = Imports.Excercises.Excercise(taskinfo)
	exercises.append(exercise)


class Homework3(Imports.Assignments.Assignment):

	layout = Imports.Documents.DocumentLayout(Homework.LayoutLocation, Homework.PageStyle)
	test = Imports.Tests.Test(exercises)
	document_entries = Imports.Entries.DocumentEntries(control_event=control_event, event_number=event_number)
	prefix = "ageom_hw"
	number = event_number

