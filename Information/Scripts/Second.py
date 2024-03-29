import random
import math
import sympy

if __package__ == "" or __package__ is None:
	import Expression
	import Fraction
	import Matrix
else: 
	from . import Expression
	from . import Fraction
	from . import Matrix

def generate_variables(
		size: int = 2, 
		with_initial: bool = True,
		formats=lambda x: x
) -> list[Expression.Variable]:
	if with_initial:
		basic = ["x", "y", "z", "w", "t"]
	else:
		basic = []

	other = [chr(ord("a")+i) for i in range(size-len(basic))]
	return sympy.symbols(" ".join((basic + other)[:size]))

def generate_parameters(
		dimension: int = 2, count: int = 1
) -> list[Expression.Variable]:
	variables = ["t", "v"]
	other = [chr(ord("g")+i) for i in range(count-2)]
	variables = [Expression.Variable(i) for i in variables+other]

	if dimension <= 4:
		return sympy.symbols(" ".join(variables[:count]))
	else:
		return sympy.symbols(" ".join(variables[1:count+1]))

class SecondOrder:

	#Matrix n*n, Matrix n*1
	def __init__(self, dimension: int, seconds: Matrix.Matrix, firsts: Matrix.Vector, free: float):
		
		self.dimension = dimension
		self.seconds = seconds
		self.firsts = firsts
		self.free = free
		self.transl_matrix = Matrix.Matrix.generate_diagonal_matrix(value=1, rows=dimension)

		self.variables = Matrix.Vector.from_list(generate_variables(self.dimension))


	@staticmethod
	def generate_random(dimension: int, steps: int = 3):

		seconds = Matrix.Matrix.generate_random_det1_matrix(size=dimension, max_steps=steps)

		s = Matrix.Matrix.generate_matrix_with_eigenvalues(values=[random.randint(-5, 5) for i in range(dimension)])
		firsts = Matrix.Vector.from_list([s[i][i] for i in range(dimension)])
		free = random.randint(-10, 10)

		return SecondOrder(dimension, seconds, firsts, free)


	@staticmethod
	def generate_random_3d_canonicasable(maxval: int = 6, with_inv: bool = True, debug: bool = False):

		def rand_wzero():
			return random.randint(-maxval, maxval)

		def rand_pos():
			return random.randint(1, maxval)

		def rand_neg():
			return random.randint(-maxval, -1)

		def rand_nneg():
			return random.randint(0, maxval)

		def rand_nzero():
			return rand_neg() if random.randint(0, 9)%2 == 0 else rand_pos()


		def rand_pos_sq():
			return random.randint(1, maxval)**2

		def rand_neg_sq():
			return -random.randint(1, maxval)**2

		def rand_nneg_sq():
			return random.randint(0, maxval)**2

		def rand_npos_sq():
			return -random.randint(0, maxval)**2

		def rand_nzero_sq():
			return rand_neg_sq() if random.randint(0, 9)%2 == 0 else rand_pos_sq()

		def rand_wzero_sq():
			return rand_nneg_sq() if random.randint(0, 9)%2 == 0 else rand_npos_sq()


		def rand_pos_sq_inv():
			if with_inv:
				return 1/rand_pos_sq()
			else:
				return rand_pos_sq()

		def rand_neg_sq_inv():
			if with_inv:
				return 1/rand_neg_sq()
			else:
				return rand_neg_sq()

		def rand_nzero_sq_inv():
			return rand_neg_sq_inv() if random.randint(0, 9)%2 == 0 else rand_pos_sq_inv()


		def rand_pos_sq_winv():
			return rand_pos_sq() if random.randint(0, 9)%2 == 0 else rand_pos_sq_inv()

		def rand_neg_sq_winv():
			return rand_neg_sq() if random.randint(0, 9)%2 == 0 else rand_neg_sq_inv()

		def rand_nzero_sq_winv():
			return rand_nzero_sq() if random.randint(0, 9)%2 == 0 else rand_nzero_sq_inv()


		def random_spherical():
			k = rand_pos_sq_winv()
			seconds = Matrix.Matrix.generate_matrix_with_eigenvalues([k for i in range(3)])
			free = rand_nzero()

			return seconds, free, None

		def random_elliptical():
			seconds = Matrix.Matrix.generate_matrix_with_eigenvalues([rand_pos_sq_winv() for i in range(3)])
			free = rand_nzero_sq()

			return seconds, free, None

		def random_cone():
			posit = random.randint(0, 2)
			seconds = Matrix.Matrix.generate_matrix_with_eigenvalues([
				rand_pos_sq_winv() if i != posit else rand_nzero_sq_winv()
				for i in range(3) 
			])
			free = 0

			return seconds, free, None

		def random_elliptic_cylindrical():
			posit = random.randint(0, 2)
			seconds = Matrix.Matrix.generate_matrix_with_eigenvalues([
				rand_pos_sq_winv() if i != posit else 0
				for i in range(3) 
			])
			free = rand_nzero_sq()

			return seconds, free, None

		def random_elliptic_parabolloid():
			posit = random.randint(0, 2)
			seconds = Matrix.Matrix.generate_matrix_with_eigenvalues([
				rand_pos_sq_winv() if i != posit else 0
				for i in range(3) 
			])
			firsts = Matrix.Vector.from_list([
				0 if i != posit else rand_neg() 
				for i in range(3)
			])
			free = rand_nzero_sq()

			return seconds, free, firsts

		def random_hyperbolic_cylindrical():
			posit1 = random.randint(0, 2)
			posit2 = random.choice([i for i in range(2) if i != posit1])

			seconds = Matrix.Matrix.generate_matrix_with_eigenvalues([
				rand_pos_sq_winv() if (i != posit1 and i != posit2) 
				else (rand_neg_sq_winv() if i != posit2 else 0)
				for i in range(3) 
			])
			free = rand_nzero_sq()

			return seconds, free, None

		def random_hyperbolic_parabolloid():
			posit1 = random.randint(0, 2)
			posit2 = random.choice([i for i in range(2) if i != posit1])

			seconds = Matrix.Matrix.generate_matrix_with_eigenvalues([
				rand_pos_sq_winv() if (i != posit1 and i != posit2) 
				else (rand_neg_sq_winv() if i != posit2 else 0)
				for i in range(3) 
			])
			firsts = Matrix.Vector.from_list([
				0 if i != posit2 else rand_neg() 
				for i in range(3)
			])
			free = rand_nzero()

			return seconds, free, firsts

		def random_hyperboloid():
			posit = random.randint(0, 2)

			seconds = Matrix.Matrix.generate_matrix_with_eigenvalues([
				rand_pos_sq_winv() if i != posit else rand_neg_sq_winv()
				for i in range(3) 
			])
			free = rand_nzero()

			return seconds, free, None

		def random_intersecting_plane():
			posit1 = random.randint(0, 2)
			posit2 = random.choice([i for i in range(2) if i != posit1])

			seconds = Matrix.Matrix.generate_matrix_with_eigenvalues([
				rand_pos_sq_winv() if (i != posit1 and i != posit2) 
				else (rand_nzero_sq_winv() if i != posit2 else 0)
				for i in range(3) 
			])
			free = 0

			return seconds, free, None

		options = [
			random_spherical,
			random_elliptical,
			random_cone,
			random_elliptic_cylindrical,
			random_elliptic_parabolloid,
			random_hyperbolic_cylindrical,
			random_hyperbolic_parabolloid,
			random_hyperboloid,
			random_intersecting_plane
		]
		option = random.choice(options)

		seconds, free, firsts = option()
	
		if not firsts:
			firsts = Matrix.Vector.from_list([0 for i in range(3)])

		if debug:
			return SecondOrder(3, seconds, firsts, free), option, options

		return SecondOrder(3, seconds, firsts, free)


	def to_expr(self):

		variables = self.transl_matrix * self.variables

		left = Matrix.Matrix.from_vector(variables, False)
		simple = sympy.nsimplify(
				sympy.expand(
					(left * self.seconds * variables).to_list()[0] 
					+ self.firsts * variables 
					+ self.free
				)
			)

		return simple

	def get_maximal_denominator(self):
		return self.to_expr().as_numer_denom()[1]

	def to_str(self):
		return str(sympy.latex(self.to_expr()))

	def __str__(self):
		return self.to_str()

	def __repr__(self):
		return self.to_str()

class SecondOrderCurves(SecondOrder):

	def __init__(self, seconds: Matrix.Matrix, firsts: Matrix.Vector, free: float):
		super().__init__(2, seconds, firsts, free)

	def set_rotation_translation_matrix(self, angle=sympy.pi):
		self.transl_matrix = Matrix.Matrix.from_list_of_lists([
			[sympy.cos(angle), sympy.sin(angle)],
			[-sympy.sin(angle), sympy.cos(angle)]
		])


	@staticmethod
	def generate_ellipse(horizontal: float, vertical: float, centered: tuple[float, float], debug: bool = False, imaginary: bool = False):
		a = horizontal
		b = vertical
		c, d = centered

		mtx = Matrix.Matrix.from_list_of_lists([[1/a**2, 0], [0, 1/b**2]])
		vec = Matrix.Vector.from_list([-2*c/a**2, -2*d/b**2])
		free = c**2/a**2 + d**2/b**2 - 1

		if imaginary:
			free = free + 2

		if not debug:
			return SecondOrderCurves(mtx, vec, free)

		return SecondOrderCurves(mtx, vec, free), sympy.nsimplify(abs(free))


	@staticmethod
	def generate_imaginary_ellipse(horizontal: float, vertical: float, centered: tuple[float, float], debug: bool = False):
		return SecondOrderCurves.generate_ellipse(horizontal, vertical, centered, debug, imaginary=True)


	@staticmethod
	def generate_hyperbola(horizontal: float, vertical: float, centered: tuple[float, float], debug: bool = False, imaginary: bool = False):
		a = horizontal
		b = vertical
		c, d = centered

		mtx = Matrix.Matrix.from_list_of_lists([[1/a**2, 0], [0, -1/b**2]])
		vec = Matrix.Vector.from_list([-2*c/a**2, 2*d/b**2])
		free = c**2/a**2 - d**2/b**2 - 1

		if imaginary:
			free = -free

		if not debug:
			return SecondOrderCurves(mtx, vec, free)

		return SecondOrderCurves(mtx, vec, free), sympy.nsimplify(abs(free))


	@staticmethod
	def generate_parabola(parameter: float, centered: tuple[float, float], debug: bool = False):
		p = parameter
		c, d = centered

		mtx = Matrix.Matrix.from_list_of_lists([[0, 0], [0, 1]])
		vec = Matrix.Vector.from_list([-2*p, -2*d])
		free = d**2 + 2*p*c

		if not debug:
			return SecondOrderCurves(mtx, vec, free)

		return SecondOrderCurves(mtx, vec, free), sympy.nsimplify(abs(free))

	@staticmethod
	def generate_cross_lines(horizontal: float, vertical: float, centered: tuple[float, float], debug: bool = False, imaginary: bool = False):
		a = horizontal
		b = vertical
		c, d = centered

		if imaginary:
			mtx = Matrix.Matrix.from_list_of_lists([[1/a**2, 0], [0, 1/b**2]])
			vec = Matrix.Vector.from_list([-2*c/a**2, -2*d/b**2])
			free = c**2/a**2 + d**2/b**2
		
		else:
			mtx = Matrix.Matrix.from_list_of_lists([[1/a**2, 0], [0, -1/b**2]])
			vec = Matrix.Vector.from_list([-2*c/a**2, 2*d/b**2])
			free = c**2/a**2 - d**2/b**2

		if not debug:
			return SecondOrderCurves(mtx, vec, free)

		return SecondOrderCurves(mtx, vec, free), sympy.nsimplify(abs(free))

	@staticmethod
	def generate_imaginary_cross_lines(horizontal: float, vertical: float, centered: tuple[float, float], debug: bool = False):
		return SecondOrderCurves.generate_cross_lines(horizontal, vertical, centered, debug, imaginary=True)


	@staticmethod
	def generate_parallel_lines(distance: float, centered: tuple[float, float], debug: bool = False, imaginary: bool = False):
		a = distance
		c, d = centered

		mtx = Matrix.Matrix.from_list_of_lists([[1/a**2, 0], [0, 0]])
		vec = Matrix.Vector.from_list([0, 0])
		free = -1

		if imaginary:
			free = -free

		if not debug:
			return SecondOrderCurves(mtx, vec, free)

		return SecondOrderCurves(mtx, vec, free), sympy.nsimplify(abs(free))


	@staticmethod
	def generate_imaginary_parallel_lines(distance: float, centered: tuple[float, float], debug: bool = False):
		return SecondOrderCurves.generate_parallel_lines(distance, centered, debug, imaginary=True)


if __name__ == "__main__":

	mtx = Matrix.Matrix.from_list_of_lists([[1, 1], [1, 1]])
	vec = Matrix.Vector.from_list([1, 1])
	free = 1

	so = SecondOrderCurves(mtx, vec, free)
	# print(so.to_str())

	ellipse = SecondOrderCurves.generate_ellipse(5, 2, (1, 0))
	# print(ellipse)

	s = []
	def func():
		
		rad1 = random.randint(1, 9)
		rad2 = random.randint(1, 9)
		pt1 = random.randint(-10, 10)
		pt2 = random.randint(-10, 10)

		return rad1, rad2, (pt1, pt2)


	hyperbola = SecondOrderCurves.generate_hyperbola(5, 2, (0, 0))
	# print(hyperbola)

	parabola = SecondOrderCurves.generate_parabola(5, (0, 0))
	# print(parabola)

	# for i in range(30):
	# 	s.append(SecondOrderCurves.generate_ellipse(*func()))

	# for i in range(30):
	# 	s.append(SecondOrderCurves.generate_hyperbola(*func()))
	
	mtx = Matrix.Matrix.generate_random_det1_matrix(size=3, max_steps=2, max_iters=1)

	for i in range(30):
		obj1, opt1, opts1 = SecondOrder.generate_random_3d_canonicasable(debug=True, with_inv=False)
		obj2, opt2, opts2 = SecondOrder.generate_random_3d_canonicasable(debug=True, with_inv=False)
		obj1.transl_matrix = mtx
		s.append((obj1, opt1))
		s.append((obj2, opt2))
		# s.append(SecondOrderCurves.generate_parabola( *(list(func())[1:]) ))
		# s.append(SecondOrderCurves.generate_hyperbola( *(list(func())) ))

	random.shuffle(s)
	for i in s:
		pass
		# print(str(i[0]) + " = 0", str(i[1]))
		# print(f"\\item \\( {str(i)} = 0 \\);")

	lists = []
	answs = []
	figures = []

	i = 0
	while i < 10:
	# for i in range(50):
		r1, r2, pt = func()
		pt1, pt2 = pt
		chses = {
			"Эллипс": [SecondOrderCurves.generate_ellipse(r1, r2, pt, debug=True), "\\item \\( \\displaystyle {figure} = 0 \\);", "\\item {name}, Полуоси: \\({r1}, {r2}\\), Центр: \\( ({pt1}, {pt2}) \\), Угол: \\(\\displaystyle {angle}\\);"],
			"Парабола": [SecondOrderCurves.generate_parabola(r1, pt, debug=True), "\\item \\( \\displaystyle {figure} = 0 \\);", "\\item {name}, Параметр: \\({r1}\\), Центр: \\( ({pt1}, {pt2}) \\), Угол: \\(\\displaystyle {angle}\\);"],
			"Гипербола": [SecondOrderCurves.generate_hyperbola(r1, r2, pt, debug=True), "\\item \\( \\displaystyle {figure} = 0 \\);", "\\item {name}, Полуоси: \\( {r1}, {r2} \\), Центр: \\( ({pt1}, {pt2}) \\), Угол: \\(\\displaystyle {angle}\\);"],
			"Мнимый эллипс": [SecondOrderCurves.generate_imaginary_ellipse(r1, r2, pt, debug=True), "\\item \\( \\displaystyle {figure} = 0 \\);", "\\item {name}, Полуоси: \\( {r1}, {r2} \\), Центр: \\( ({pt1}, {pt2}) \\), Угол: \\(\\displaystyle {angle}\\);"],
			"Пересекающиеся прямые": [SecondOrderCurves.generate_cross_lines(r1, r2, pt, debug=True), "\\item \\( \\displaystyle {figure} = 0 \\);", "\\item {name}, Направляющие: \\({r1}, {r2}\\), Центр: \\( ({pt1}, {pt2}) \\), Угол: \\(\\displaystyle {angle}\\);"],
			"Мнимые пересекающиеся прямые": [SecondOrderCurves.generate_imaginary_cross_lines(r1, r2, pt, debug=True), "\\item \\( \\displaystyle {figure} = 0 \\);", "\\item {name}, Направляющие: \\({r1}, {r2}\\), Центр: \\( ({pt1}, {pt2}) \\), Угол: \\(\\displaystyle {angle}\\);"],
			"Параллельные прямые": [SecondOrderCurves.generate_parallel_lines(r1, pt, debug=True), "\\item \\( \\displaystyle {figure} = 0 \\);", "\\item {name}, Расстояние: \\({r1}\\), Центр: \\( ({pt1}, {pt2}) \\), Угол: \\(\\displaystyle {angle}\\);"],
			"Мнимые параллельные прямые": [SecondOrderCurves.generate_imaginary_parallel_lines(r1, pt, debug=True), "\\item \\( \\displaystyle {figure} = 0 \\);", "\\item {name}, Расстояние: \\({r1}\\), Центр: \\( ({pt1}, {pt2}) \\), Угол: \\(\\displaystyle {angle}\\);"],
		}

		angles = [0, 0, 0, 0, sympy.pi/6, sympy.pi/4, sympy.pi/3, sympy.pi/2, sympy.pi*5/6, sympy.pi*2/3, sympy.pi*3/4]
		sign = random.choice([1, -1, -1, 1, 1, -1, -1, 1])
		angle = random.choice(angles)

		chs = random.choice(list(chses.keys()))
		figr, curve = chses[chs][0]
		figr.set_rotation_translation_matrix(angle)
		fig = chses[chs][1]
		ans = chses[chs][2]
		# print(figr, curve, type(curve))

		if figr.get_maximal_denominator() > 128:
			continue

		i += 1

		figures.append(figr)
		lists.append(fig.format(figure=str(figr)))
		answs.append(ans.format(name=chs, r1=r1, r2=r2, pt1=pt1, pt2=pt2, angle=sympy.latex(angle)))

		# print(fig.format(figure="kek", name="kek", r1=r1, r2=r2, pt1=pt1, pt2=pt2))
		# print(fig.format(figure=str(chses[chs][0]), name=chs, r1=r1, r2=r2, pt1=pt1, pt2=pt2))
	
	# print("\\begin{enumerate}")
	# for i in figures:
	# 	print("\t"+str(i.get_maximal_denominator()))
	# print("\\end{enumerate}")

	print("\\begin{enumerate}")
	for i in lists:
		print("\t"+str(i))
	print("\\end{enumerate}")

	print("\\begin{enumerate}")
	for i in answs:
		print("\t"+str(i))
	print("\\end{enumerate}")
