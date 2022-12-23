import random

from ..Default import Homework
import Modules.Imports as Imports

from ..Scripts import Lines

control_event = "Индивидуальное домашнее задание"
event_number = 1

prefix = "Tasks/Homework1/"

def tasks_updater(text):
	line = Lines.Line(2)

	line.generate_random_line_points()
	text = text.replace("#PARAMSYSTEM#", line.to_parametric_form())

	line.generate_random_line_points()
	text = text.replace("#POINTS#", line.to_points_form())
	
	line.generate_random_line_points()
	text = text.replace("#LINE1#", line.to_random_form())
	
	line.generate_random_line_points()
	text = text.replace("#LINE2#", line.to_random_form())
	
	text = text.replace("#POINT#", Lines.Point.generate_random_point(2).to_str(
		Lines.generate_point_name()
	))

	if text.find("\\left[") >= 0:
		text = text.replace("#R#", ", заданной точками")
		text = text.replace("#RS#",
			", где одна из них задана точками"
			if text.count("\\left[") == 1 else
			", заданных точками"
		)
		
	text = text.replace("#R#", "")
	text = text.replace("#RS#", "")

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
	exercise = Imports.Exercises.Exercise(taskinfo)
	exercises.append(exercise)

class Homework1(Imports.Assignments.Assignment):

	layout = Imports.Documents.DocumentLayout(Homework.LayoutLocation, Homework.PageStyle)
	test = Imports.Tests.Test(exercises)
	document_entries = Imports.Entries.DocumentEntries(control_event=control_event, event_number=event_number)
	prefix = "ageom_hw"
	number = event_number

