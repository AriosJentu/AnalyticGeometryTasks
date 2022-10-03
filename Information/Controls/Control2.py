import random

from ..Default import Control
import Modules.Imports as Imports

from ..Scripts import Lines
from ..Scripts import Second
from ..Scripts import Matrix
from ..Scripts import TextReplacer

control_event = "Контрольная работа"
# control_event = "Контрольная работа на тему <<Кривые и поверхности второго порядка>>"
event_number = 2

prefix = "Tasks/Seconds/"

def parameters():
		
	rad1 = random.randint(1, 9)
	rad2 = random.randint(1, 9)
	pt1 = random.randint(-10, 10)
	pt2 = random.randint(-10, 10)

	return rad1, rad2, (pt1, pt2)

def get_random_curve():
	curves = [
		Second.SecondOrderCurves.generate_ellipse( *(list(parameters())), True),
		Second.SecondOrderCurves.generate_hyperbola( *(list(parameters())), True),
		Second.SecondOrderCurves.generate_parabola( *(list(parameters())[1:]), True),

		Second.SecondOrderCurves.generate_ellipse( *(list(parameters())), True),
		Second.SecondOrderCurves.generate_hyperbola( *(list(parameters())), True),
	]

	for i, curve in enumerate(curves):
		if len(str(curve[1])) > 5:
			curves[i] = 0

	vals = [i[0] for i in curves if i != 0]

	if len(vals) <= 1:
		return get_random_curve()
	else:
		return random.choice(vals)

def get_random_surface():

	mtx = Matrix.Matrix.generate_random_det1_matrix(size=3, max_steps=2, max_iters=1)

	obj = Second.SecondOrder.generate_random_3d_canonicasable()
	obj.transl_matrix = mtx

	s = str(obj)
	strs = s\
		.replace("-", "+")\
		.replace("=", "+")\
		.replace("}{", "+")\
		.replace("^{2}", "")\
		.replace("\\frac", "")\
		.replace("{", "")\
		.replace("}", "")\
		.replace("x", "")\
		.replace("y", "")\
		.replace("z", "")\
		.replace(" ", "")\
		.split("+")
	print(strs)
	lst = [len(i) for i in strs]

	if max(lst) > 2:
		return get_random_surface()
	else:
		return s


def tasks_updater(text):
	random.seed()

	text = TextReplacer.text_replacer(text)
	
	text = text.replace("#POINT1#", Lines.Point.generate_random_point(2).to_str(
		Lines.generate_point_name()
	))

	text = text.replace("#SECONDS1#", f"\\[ {get_random_curve()} = 0 \\]")
	text = text.replace("#SECONDS2#", f"\\[ {get_random_surface()} = 0 \\]")

	return text

tasks = []

for i in [1, 2, 3]:

	tasks_i = Imports.Tasks.SpecificTasks()
	task1_i = Imports.Tasks.SpecificTaskInfo(f"{prefix}Task{i}.tex")
	task1_i.set_updater_function(tasks_updater)
	tasks_i.append(task1_i)
	tasks.append(tasks_i)

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

class Control2(Imports.Assignments.Assignment):

	layout = Imports.Documents.DocumentLayout(Control.LayoutLocation, Control.PageStyle)
	test = Imports.Tests.Test(exercises)
	document_entries = Imports.Entries.DocumentEntries(control_event=control_event, event_number=event_number)
	prefix = "ageom_control"
	number = event_number

