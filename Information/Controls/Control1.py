import random

from ..Default import Control
import Modules.Imports as Imports

from ..Scripts import Lines
from ..Scripts import TextReplacer

control_event = "Контрольная работа"
# control_event = "Контрольная работа на тему <<Прямые, плоскости и вектора>>"
event_number = 1

prefix = "Tasks/"

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

def task1_updater(text):

	names = ["a", "b", "c"]
	vectors = {i: Lines.Vector.generate_random_vector(3, maxvalue=6) for i in names}

	lambd = random.choice([i for i in range(-5, 6) if (i != 0 and abs(i) != 1)])
	lambdp = random.randint(2, 5)

	random.seed()
	a, b, c = random.sample(names, 3)
	va, vb, vc = [vectors[i] for i in [a, b, c]]

	variations1 = [
		"{a} \\times {lp}{b} + {c}", 
		"{a} \\cdot \\pares{{ {l}{b} \\times {c} }}", 
		"{l} {a} + {b} \\times {c}",
		"{a} \\times \\pares{{ {b} \\times {c} }}",
		"\\pares{{ {a} \\times {b} }} \\times {c}",
	]

	comments1 = [
		str( va.cross_product(lambdp*vb) + vc ),
		str( va * ( (lambd*vb).cross_product(vc) ) ),
		str( lambd*va + vb.cross_product(vc) ),
		str( va.cross_product( vb.cross_product(vc) ) ),
		str( ( va.cross_product(vb) ).cross_product(vc) ),
	]

	variations2 = [
		"Объем паралеллепипеда, образованного тройкой векторов $\\bracs{{ {a}, {b}, {c} }}$",
		"Угол между векторами ${a}, {b}$",
		"Площадь параллелограмма, образованного векторами \\( \\bracs{{ {lp}{a}, {l}{b} }} \\)",
		"Коэффициент $\\lambda$ в уравнении: \\( {a} \\times {b} + \\lambda {c} = {r} \\)"	
	]

	text = text.replace("#VECTORL1#", vectors["a"].to_str())
	text = text.replace("#VECTORL2#", vectors["b"].to_str())
	text = text.replace("#VECTORL3#", vectors["c"].to_str())

	num1 = random.randint(0, len(variations1)-1)
	num2 = random.randint(0, len(variations2)-1)

	part1str = variations1[num1].format(a=a, b=b, c=c, l=lambd, lp=lambdp)
	part1cmtstr = comments1[num1]

	random.seed()
	a, b, c = random.sample(names, 3)
	va, vb, vc = [vectors[i] for i in [a, b, c]]
	vr = va.cross_product(vb) + vc * lambd

	part2str = variations2[num2].format(a=a, b=b, c=c, l=lambd, lp=lambdp, r=vr.to_str())

	text = text.replace("#LVARIATION1#", f"\\( \\displaystyle {part1str} \\)")
	text = text.replace("#COMMENT1#", part1cmtstr)
	text = text.replace("#LVARIATION2#", part2str)

	return text

# locations = lambda arr: [f"{prefix}Task1/Variant{i}.tex" for i in arr]

# tasks = []
# for pair in [[1, 2], [3, 4]]:
# 	tasks_i = Imports.Tasks.SpecificTasks()
# 	for location in locations(pair):
# 		task_j = Imports.Tasks.SpecificTaskInfo(location)
# 		task_j.set_updater_function(tasks_updater)
# 		tasks_i.append(task_j)
# 	tasks.append(tasks_i)

tasks = []

tasks1 = Imports.Tasks.SpecificTasks()
task11 = Imports.Tasks.SpecificTaskInfo(f"{prefix}Linears/Task1.tex")
task11.set_updater_function(task1_updater)
tasks1.append(task11)
tasks.append(tasks1)

tasks2 = Imports.Tasks.SpecificTasks()
task21 = Imports.Tasks.SpecificTaskInfo(f"{prefix}Exam/Task1/Variant1.tex")
task22 = Imports.Tasks.SpecificTaskInfo(f"{prefix}Exam/Task1/Variant2.tex")
task23 = Imports.Tasks.SpecificTaskInfo(f"{prefix}Exam/Task2/Variant3.tex")
task21.set_updater_function(tasks_updater)
task22.set_updater_function(tasks_updater)
task23.set_updater_function(tasks_updater)
tasks2.append(task21)
tasks2.append(task22)
tasks2.append(task23)
tasks.append(tasks2)

tasks3 = Imports.Tasks.SpecificTasks()
task31 = Imports.Tasks.SpecificTaskInfo(f"{prefix}Exam/Task1/Variant3.tex")
task32 = Imports.Tasks.SpecificTaskInfo(f"{prefix}Exam/Task1/Variant4.tex")
task33 = Imports.Tasks.SpecificTaskInfo(f"{prefix}Exam/Task2/Variant1.tex")
task31.set_updater_function(tasks_updater)
task32.set_updater_function(tasks_updater)
task33.set_updater_function(tasks_updater)
tasks3.append(task31)
tasks3.append(task32)
tasks3.append(task33)
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

