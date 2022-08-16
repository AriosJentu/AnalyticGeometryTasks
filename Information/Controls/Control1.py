import random

from ..Default import Control
import Modules.Imports as Imports

from ..Scripts import Lines
from ..Scripts import TextReplacer

control_event = "Контрольная работа"
# control_event = "Контрольная работа на тему <<Прямые, плоскости и вектора>>"
event_number = 1

prefix = "Tasks/Exam/"

def tasks_updater(text):
	random.seed()

	line = Lines.Line(3)
	plane = Lines.HyperPlane(3)

	line.generate_random_line_points()
	text = text.replace("#LINE1#", line.to_random_form())

	line.generate_random_line_points()
	text = text.replace("#LINE2#", line.to_random_form())
	
	plane.generate_random_plane_points()
	text = text.replace("#PLANE1#", plane.to_random_form())
	
	plane.generate_random_plane_points()
	text = text.replace("#PLANE2#", plane.to_random_form())

	text = text.replace("#POINT1#", Lines.Point.generate_random_point(3).to_str(
		Lines.generate_point_name()
	))

	text = text.replace("#VECTOR1#", Lines.Vector.generate_random_vector(3).to_str())
	text = text.replace("#VECTOR2#", Lines.Vector.generate_random_vector(3).to_str())

	text = TextReplacer.text_replacer(text)

	return text

locations = lambda arr: [f"{prefix}Task1/Variant{i}.tex" for i in arr]

tasks = []
for pair in [[1, 2], [3, 4]]:
	tasks_i = Imports.Tasks.SpecificTasks()
	for location in locations(pair):
		task_j = Imports.Tasks.SpecificTaskInfo(location)
		task_j.set_updater_function(tasks_updater)
		tasks_i.append(task_j)
	tasks.append(tasks_i)

tasks3 = Imports.Tasks.SpecificTasks()
task31 = Imports.Tasks.SpecificTaskInfo(f"{prefix}Task2/Variant1.tex")
task31.set_updater_function(tasks_updater)
tasks3.append(task31)
tasks.append(tasks3)

task = Imports.Tasks.EmptyTask()
tasks.append(task)

tasksinfo = []
for task in tasks:
	taskinfo = [Imports.Tasks.TasksInformation(task)]
	tasksinfo.append(taskinfo)

exercises = []
for index, taskinfo in enumerate(tasksinfo):
	exercise = Imports.Excercises.Excercise(taskinfo)
	if index == len(tasksinfo) - 1:
		exercise = Imports.Excercises.Excercise(taskinfo, title="Теоретический вопрос")

	exercises.append(exercise)

class Control1(Imports.Assignments.Assignment):

	layout = Imports.Documents.DocumentLayout(Control.LayoutLocation, Control.PageStyle)
	test = Imports.Tests.Test(exercises)
	document_entries = Imports.Entries.DocumentEntries(control_event=control_event, event_number=event_number)
	prefix = "ageom_control"
	number = event_number

