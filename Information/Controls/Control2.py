import random
import sympy

from ..Default import ControlMiddle
import Modules.Imports as Imports

from ..Scripts import Lines
from ..Scripts import Second
from ..Scripts import Matrix
from ..Scripts import TextReplacer

control_event = "Контрольная работа"
# control_event = "Контрольная работа на тему <<Кривые и поверхности второго порядка>>"
event_number = 2

prefix = "Tasks/Seconds/"

SurfacePointEquations = Imports.Tasks.TasksGetter("Tasks/Exam/Special/SurfacesInitial.tex")
SurfacePointEquations.add_prefix_path(Imports.MODULE_PATH)
SurfacePointEquations.read_information()

char_lambda = sympy.symbols("\\lambda")

def parameters():
		
	rad1 = random.randint(1, 9)
	rad2 = random.randint(1, 9)
	pt1 = random.randint(-10, 10)
	pt2 = random.randint(-10, 10)

	return rad1, rad2, (pt1, pt2)

def generate_random_additions_matrix():
	a = random.choice([i for i in range(-5, 6) if i != 0])
	b = random.choice([i for i in range(-5, 6) if i != 0])

	chs = random.randint(0, 3)

	if chs == 0:
		return Matrix.Matrix.from_list_of_lists([[a*char_lambda, 0], [0, b*char_lambda]])
	elif chs == 1:
		return Matrix.Matrix.from_list_of_lists([[0, a*char_lambda], [0, b*char_lambda]])
	elif chs == 2:
		return Matrix.Matrix.from_list_of_lists([[a*char_lambda, 0], [b*char_lambda, 0]])
	elif chs == 3:
		return Matrix.Matrix.from_list_of_lists([[0, a*char_lambda], [b*char_lambda, 0]])

def generate_random_additions_vector():
	a = random.choice([i for i in range(-5, 6) if i != 0])
	chs = random.randint(0, 1)

	if chs:
		return Matrix.Vector.from_list([a*char_lambda, 0])
	else:
		return Matrix.Vector.from_list([0, a*char_lambda])


def get_random_curve(with_parameter: bool = False):

	is_found = False
	this_curve = None
	this_name = ""

	while not is_found:

		r1, r2, pt = parameters()
		pt1, pt2 = pt
		angles_full = [0, 0, sympy.pi/6, sympy.pi/4, sympy.pi/3, sympy.pi/2, sympy.pi*5/6, sympy.pi*2/3, sympy.pi*3/4]
		angles_no_simple = [sympy.pi/6, sympy.pi/4, sympy.pi/3, sympy.pi*5/6, sympy.pi*2/3, sympy.pi*3/4]

		right_matrix = Matrix.Matrix.generate_diagonal_matrix(0)
		right_vector = Matrix.Vector.from_list([0, 0])

		figure_names = [
			"Эллипс",
			"Парабола",
			"Гипербола",
			"Мнимый эллипс",
			"Пересекающиеся прямые",
			"Мнимые пересекающиеся прямые",
			"Параллельные прямые",
			"Мнимые параллельные прямые",
		]

		addfigs = [
			"эллипсом",
			"параболой",
			"гиперболой",
			"песекающимися прямыми",
		]

		if with_parameter:
			angles_full = [0, 0, sympy.pi/2]
			angles_no_simple = angles_full

			figure_names = [
				"Эллипс",
				"Парабола",
				"Гипербола",
				"Пересекающиеся прямые",
			]

			right_matrix = generate_random_additions_matrix()
			right_vector = generate_random_additions_vector()

		choises = {
			"Эллипс": [
				Second.SecondOrderCurves.generate_ellipse(r1, r2, pt, debug=True), 
				"\\[ {figure} = 0 \\] \t\t % {name}, Полуоси: \\({r1}, {r2}\\), Центр: \\( ({pt1}, {pt2}) \\), Угол: \\(\\displaystyle {angle}\\);",
				angles_full
			],
			"Парабола": [
				Second.SecondOrderCurves.generate_parabola(r1, pt, debug=True), 
				"\\[ {figure} = 0 \\] \t\t % {name}, Параметр: \\({r1}\\), Центр: \\( ({pt1}, {pt2}) \\), Угол: \\(\\displaystyle {angle}\\);",
				angles_no_simple
			],
			"Гипербола": [
				Second.SecondOrderCurves.generate_hyperbola(r1, r2, pt, debug=True), 
				"\\[ {figure} = 0 \\] \t\t % {name}, Полуоси: \\( {r1}, {r2} \\), Центр: \\( ({pt1}, {pt2}) \\), Угол: \\(\\displaystyle {angle}\\);",
				angles_full
			],
			"Мнимый эллипс": [
				Second.SecondOrderCurves.generate_imaginary_ellipse(r1, r2, pt, debug=True), 
				"\\[ {figure} = 0 \\] \t\t % {name}, Полуоси: \\( {r1}, {r2} \\), Центр: \\( ({pt1}, {pt2}) \\), Угол: \\(\\displaystyle {angle}\\);",
				angles_full
			],
			"Пересекающиеся прямые": [
				Second.SecondOrderCurves.generate_cross_lines(r1, r2, pt, debug=True), 
				"\\[ {figure} = 0 \\] \t\t % {name}, Направляющие: \\({r1}, {r2}\\), Центр: \\( ({pt1}, {pt2}) \\), Угол: \\(\\displaystyle {angle}\\);",
				angles_no_simple
			],
			"Мнимые пересекающиеся прямые": [
				Second.SecondOrderCurves.generate_imaginary_cross_lines(r1, r2, pt, debug=True), 
				"\\[ {figure} = 0 \\] \t\t % {name}, Направляющие: \\({r1}, {r2}\\), Центр: \\( ({pt1}, {pt2}) \\), Угол: \\(\\displaystyle {angle}\\);",
				angles_no_simple
			],
			"Параллельные прямые": [
				Second.SecondOrderCurves.generate_parallel_lines(r1, pt, debug=True), 
				"\\[ {figure} = 0 \\] \t\t % {name}, Расстояние: \\({r1}\\), Центр: \\( ({pt1}, {pt2}) \\), Угол: \\(\\displaystyle {angle}\\);",
				angles_no_simple
			],
			"Мнимые параллельные прямые": [
				Second.SecondOrderCurves.generate_imaginary_parallel_lines(r1, pt, debug=True), 
				"\\[ {figure} = 0 \\] \t\t % {name}, Расстояние: \\({r1}\\), Центр: \\( ({pt1}, {pt2}) \\), Угол: \\(\\displaystyle {angle}\\);",
				angles_no_simple
			],
		}

		sign = random.choice([1, -1, -1, 1, 1, -1, -1, 1])

		choice = random.choice(figure_names)
		figure, curve = choises[choice][0]

		figure_string = choises[choice][1]
		angles = choises[choice][2]

		angle = random.choice(angles)*sign

		figure.set_rotation_translation_matrix(angle)
		figure.seconds += right_matrix
		figure.firsts += right_vector

		if figure.get_maximal_denominator() > 128:
			continue

		is_found = True
		this_curve = figure_string.format(figure=str(figure), name=choice, r1=r1, r2=r2, pt1=pt1, pt2=pt2, angle=sympy.latex(angle))
		
		if with_parameter:
			this_name = addfigs[figure_names.index(choice)]

	if with_parameter:
		return this_curve, this_name

	return this_curve


def get_random_surface(random_matrix: bool = True):

	obj = Second.SecondOrder.generate_random_3d_canonicasable()

	if random_matrix:
		mtx = Matrix.Matrix.generate_random_det1_matrix(size=3, max_steps=2, max_iters=1)
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

	lst = [len(i) for i in strs if i != ""]
	# print([i for i in strs if i != ""])

	if max(lst) > 2:
		return get_random_surface(random_matrix)
	else:
		return s


def tasks_updater(text):
	random.seed()

	text = TextReplacer.text_replacer(text)
	
	if "#POINT1#" in text:
		text = text.replace("#POINT1#", 
			Lines.Point.generate_random_point(2).to_str(
				Lines.generate_point_name()
			)
		)

	if "#CURVE#" in text:
		text = text.replace("#CURVE#", get_random_curve())
	
	if "#CURVEPARAM#" in text:
		param, name = get_random_curve(True)
		text = text.replace("#CURVEPARAM#", param)
		text = text.replace("#CURVENAME#", name)
	
	if "#SURFACE#" in text:
		text = text.replace("#SURFACE#", f"\\[ {get_random_surface()} = 0 \\]")

	if "#SURFACESIMPLE#" in text:
		text = text.replace("#SURFACESIMPLE#", f"{get_random_surface(False)} = 0")

	if "#LINE#" in text:
		line = Lines.Line(3)
		line.generate_random_line_points()
		text = text.replace("#LINE#", line.to_canonical_form())

	if "#PLANE#" in text:
		plane = Lines.HyperPlane(3)
		plane.generate_random_plane_points()
		text = text.replace("#PLANE#", plane.to_canonical_form())

	if "#GENSURFACE#" in text:
		text = text.replace("#GENSURFACE#", SurfacePointEquations.generate_task_string())

	return text

# #CURVE# - second order 2D curve with "\[ \]"
# #CURVEPARAM# - second order 2D curve with parameter "lambda" and with "\[ \]"
# #CURVENAME# - string of curve name
# #SURFACE# - second order 3D surface to canonical with "\[ \]"
# #SURFACESIMPLE# - simple second order 3D surface without "\[ \]"
# #LINE# - 3D line equation (canonical) without "\[ \]"
# #POINT1# - Point in 3D space with name
# #GENSURFACE# - General surface with initial point without "\[ \]"
# #PLANE# - plane

tasks = []

for i in [1, 2, 3]:

	tasks_i = Imports.Tasks.SpecificTasks()
	task1_i = Imports.Tasks.SpecificTaskInfo(f"{prefix}Task{i}/Variant1.tex")
	task2_i = Imports.Tasks.SpecificTaskInfo(f"{prefix}Task{i}/Variant2.tex")
	task1_i.set_updater_function(tasks_updater)
	task2_i.set_updater_function(tasks_updater)
	tasks_i.append(task1_i)
	tasks_i.append(task2_i)
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

	layout = Imports.Documents.DocumentLayout(ControlMiddle.LayoutLocation, ControlMiddle.PageStyle)
	test = Imports.Tests.Test(exercises)
	document_entries = Imports.Entries.DocumentEntries(control_event=control_event, event_number=event_number)
	prefix = "ageom_control"
	number = event_number

