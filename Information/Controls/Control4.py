import random
import sympy as sp

from ..Default import Control
import Modules.Imports as Imports

from ..Scripts import Lines
from ..Scripts import Quaternions
from ..Scripts import TextReplacer

control_event = "Контрольная работа"
# control_event = "Контрольная работа на тему <<Кватернионы>>"
event_number = 4

prefix = "Tasks/Exam/"

SurfaceEquations = Imports.Tasks.TasksGetter(prefix+"Special/Surfaces.tex")
SurfaceEquations.add_prefix_path(Imports.MODULE_PATH)
SurfaceEquations.read_information()

def generate_random_simple_vector():
	angles = [
		sp.pi/2,
		sp.pi/3, 2*sp.pi/3, 4*sp.pi/3, 5*sp.pi/3,
		sp.pi/4, 3*sp.pi/4, 5*sp.pi/4, 7*sp.pi/4,
	]

	phi, theta = random.sample(angles, 2)

	#Spherical coordinates
	if theta != sp.pi/2:
		s = [sp.cos(phi)*sp.cos(theta), sp.sin(phi)*sp.cos(theta), sp.sin(theta)]
		random.shuffle(s)
		x, y, z = s
	else:
		s = [sp.cos(phi)*sp.sin(theta), sp.sin(phi)*sp.sin(theta), sp.cos(theta)]
		random.shuffle(s)
		x, y, z = s

	denoms = [sp.fraction(i)[1] for i in [x, y, z]]
	com_mul = sp.lcm(denoms)*random.choice([1, sp.sqrt(2), sp.sqrt(3), sp.sqrt(6)])*random.choice([-1, 1])

	return "\\left\\lbrace"+sp.latex(x*com_mul)+", "+sp.latex(y*com_mul)+", "+sp.latex(z*com_mul)+"\\right\\rbrace"

def tasks_updater(text):
	random.seed()

	text = TextReplacer.text_replacer(text)
	
	text = text.replace("#POINT1#", Lines.Point.generate_random_point(3).to_str(
		Lines.generate_point_name()
	))

	# text = text.replace("#VECTOR1#", Lines.Vector.generate_random_vector(3).to_str())
	text = text.replace("#VECTOR1#", generate_random_simple_vector())
	text = text.replace("#DANGLE1#", random.choice(Lines.ANGLES_DOUBLE))

	text = text.replace("#SURFACE1#", SurfaceEquations.generate_task_string())
	
	text = text.replace("#QUAT1#", str(Quaternions.Quaternion.generate_random_number()))
	text = text.replace("#QUAT2#", str(Quaternions.Quaternion.generate_random_number()))
	text = text.replace("#QUAT3#", str(Quaternions.Quaternion.generate_random_number()))

	text = text.replace("#EXPRESSION#", Quaternions.Expression.generate_expression())

	return text

tasks = []

for i in [5, 6, 7]:

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
	exercise = Imports.Exercises.Exercise(taskinfo)
	if index == len(tasksinfo) - 1:
		exercise = Imports.Exercises.Exercise(taskinfo, title="Теоретический вопрос")

	exercises.append(exercise)

class Control4(Imports.Assignments.Assignment):

	layout = Imports.Documents.DocumentLayout(Control.LayoutLocation, Control.PageStyle)
	test = Imports.Tests.Test(exercises)
	document_entries = Imports.Entries.DocumentEntries(control_event=control_event, event_number=event_number)
	prefix = "ageom_control"
	number = event_number

