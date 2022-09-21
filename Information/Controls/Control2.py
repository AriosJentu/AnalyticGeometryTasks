import random

from ..Default import ControlLonger
import Modules.Imports as Imports

from ..Scripts import Lines
from ..Scripts import TextReplacer

control_event = "Контрольная работа"
# control_event = "Контрольная работа на тему <<Преобразования координат>>"
event_number = 2

prefix = "Tasks/Exam/"

SurfaceEquations = Imports.Tasks.TasksGetter(prefix+"Special/Surfaces.tex")
SurfaceEquations.add_prefix_path(Imports.MODULE_PATH)
SurfaceEquations.read_information()

def tasks_updater(text):
	random.seed()

	text = text.replace("#POINT1#", Lines.Point.generate_random_point(3).to_str(
		Lines.generate_point_name()
	))

	text = text.replace("#COORDSYSTEM#", random.choice(["сферической", "циллиндрической"]))
	text = text.replace("#PLANETYPE#", random.choice(["параметрическое", "каноническое"]))
	
	text = text.replace("#COORDSYSTEME#", random.choice(["spherical", "cylindrical"]))
	text = text.replace("#PLANETYPEE#", random.choice(["parametric", "canonical"]))

	text = text.replace("#MATRIX#", Lines.Matrix.Matrix.generate_random_detn_matrix(3).to_latex())

	text = text.replace("#ANGLE1#", random.choice(Lines.ANGLES))
	text = text.replace("#ANGLE2#", random.choice(Lines.ANGLES))
	text = text.replace("#ANGLE3#", random.choice(Lines.ANGLES))

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

	text = text.replace("#SURFACE1#", SurfaceEquations.generate_task_string())

	text = TextReplacer.text_replacer(text)

	return text

tasks = []

tasks1 = Imports.Tasks.SpecificTasks()
task11 = Imports.Tasks.SpecificTaskInfo(f"{prefix}Task4.tex")
task11.set_updater_function(tasks_updater)
tasks1.append(task11)
tasks.append(tasks1)

tasks2 = Imports.Tasks.SpecificTasks()
task21 = Imports.Tasks.SpecificTaskInfo(f"{prefix}Task3/Variant2.tex")
task21.set_updater_function(tasks_updater)
tasks2.append(task21)
tasks.append(tasks2)

tasks3 = Imports.Tasks.SpecificTasks()
task31 = Imports.Tasks.SpecificTaskInfo(f"{prefix}Task3/Variant1_1.tex")
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

class Control2(Imports.Assignments.Assignment):

	layout = Imports.Documents.DocumentLayout(ControlLonger.LayoutLocation, ControlLonger.PageStyle)
	test = Imports.Tests.Test(exercises)
	document_entries = Imports.Entries.DocumentEntries(control_event=control_event, event_number=event_number)
	prefix = "ageom_control"
	number = event_number

