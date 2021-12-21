import random

from ..Default import Exam
import Modules.Imports as Imports

from ..Scripts import Lines
from ..Scripts import Quaternions
from ..Scripts import TextReplacer

control_event = "Экзаменационный вариант"
event_number = 1

prefix = "Tasks/Exam/"

SurfaceEquations = Imports.Tasks.TasksGetter(prefix+"Special/Surfaces.tex")
SurfaceEquations.add_prefix_path(Imports.MODULE_PATH)
SurfaceEquations.read_information()

SurfacePointEquations = Imports.Tasks.TasksGetter(prefix+"Special/SurfacesInitial.tex")
SurfacePointEquations.add_prefix_path(Imports.MODULE_PATH)
SurfacePointEquations.read_information()

#Task1:
# - V1: Distance from line to point 3d
# - V2: Angle between lines 3d
# - V3: Plane equation from 2 lines and point
# - V4: Plane equation from 2 vectors and point

# Task2: 
# - V1: Distance from plane to point 3d
# - V2: Intersection point of line and surface
# - V3: Parametric line equation from plane and surface
# - V4: Tangent plane for surface at point

#Task3:
# - V1: Find new equation of surface after moving and rotating axis
# - V1: Find new equation of surface with transposition matrix

#Task4:
# - Transpose equation to cyllindric/spherical coordinates

#Task5:
# - Find expression result for quaternions

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

	text = text.replace("#COORDSYSTEM#", random.choice(["сферической", "циллиндрической"]))
	text = text.replace("#PLANETYPE#", random.choice(["параметрическое", "каноническое"]))

	text = text.replace("#SURFACE1#", SurfaceEquations.generate_task_string())
	text = text.replace("#SURFACEPOINT1#", SurfacePointEquations.generate_task_string())

	text = text.replace("#ANGLE1#", random.choice(Lines.ANGLES))
	text = text.replace("#ANGLE2#", random.choice(Lines.ANGLES))
	text = text.replace("#ANGLE3#", random.choice(Lines.ANGLES))

	text = text.replace("#MATRIX#", Lines.Matrix.Matrix.generate_random_detn_matrix(3).to_latex())
	
	text = text.replace("#OLDVECTOR#", Lines.Matrix.Vector.from_list(
		["x", "y", "z"]).to_latex()
	)
	text = text.replace("#NEWVECTOR#", Lines.Matrix.Vector.from_list(
		["\\tilde{{x}}", "\\tilde{{y}}", "\\tilde{{z}}"]).to_latex()
	)

	text = text.replace("#EXCHANGEVECTOR#", Lines.Matrix.Vector.from_list([
		random.randint(-10, 10),
		random.randint(-10, 10),
		random.randint(-10, 10)
	]).to_latex())

	text = text.replace("#QUAT1#", str(Quaternions.Quaternion.generate_random_number()))
	text = text.replace("#QUAT2#", str(Quaternions.Quaternion.generate_random_number()))
	text = text.replace("#QUAT3#", str(Quaternions.Quaternion.generate_random_number()))

	text = text.replace("#EXPRESSION#", Quaternions.Expression.generate_expression())

	text = TextReplacer.text_replacer(text)

	return text

tasks1 = Imports.Tasks.SpecificTasks()
for i in range(4):
	task1 = Imports.Tasks.SpecificTaskInfo(prefix+f"Task1/Variant{i+1}.tex")
	task1.set_updater_function(tasks_updater)
	tasks1.append(task1)

tasks2 = Imports.Tasks.SpecificTasks()
for i in range(4):
	task2 = Imports.Tasks.SpecificTaskInfo(prefix+f"Task2/Variant{i+1}.tex")
	task2.set_updater_function(tasks_updater)
	tasks2.append(task2)

tasks3 = Imports.Tasks.SpecificTasks()
for i in range(2):
	task3 = Imports.Tasks.SpecificTaskInfo(prefix+f"Task3/Variant{i+1}.tex")
	task3.set_updater_function(tasks_updater)
	tasks3.append(task3)

tasks4 = Imports.Tasks.SpecificTasks()
task4 = Imports.Tasks.SpecificTaskInfo(prefix+f"Task4.tex")
task4.set_updater_function(tasks_updater)
tasks4.append(task4)

tasks5 = Imports.Tasks.SpecificTasks()
task5 = Imports.Tasks.SpecificTaskInfo(prefix+f"Task5.tex")
task5.set_updater_function(tasks_updater)
tasks5.append(task5)

tasks6 = Imports.Tasks.SpecificTasks()
task6 = Imports.Tasks.SpecificTaskInfo(prefix+f"Task6.tex")
task6.set_updater_function(tasks_updater)
tasks6.append(task6)

tasks = [tasks1, tasks2, tasks3, tasks4, tasks5, tasks6]

tasksinfo = []
for task in tasks:
	taskinfo = [Imports.Tasks.TasksInformation(task)]
	tasksinfo.append(taskinfo)

exercises = []
for taskinfo in tasksinfo:
	exercise = Imports.Excercises.Excercise(taskinfo)
	exercises.append(exercise)

class Exam(Imports.Assignments.Assignment):

	layout = Imports.Documents.DocumentLayout(Exam.LayoutLocation, Exam.PageStyle)
	test = Imports.Tests.Test(exercises)
	document_entries = Imports.Entries.DocumentEntries(control_event=control_event, event_number=event_number)
	prefix = "ageom_exam"
	number = event_number
