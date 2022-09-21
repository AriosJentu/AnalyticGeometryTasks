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

		self.variables = Matrix.Vector.from_list(generate_variables(self.dimension))

	def to_expr(self):
		left = Matrix.Matrix.from_vector(self.variables, False)
		simple = sympy.nsimplify(
				sympy.expand(
					(left * self.seconds * self.variables).to_list()[0] 
					+ self.firsts * self.variables 
					+ self.free
				)
			)

		return simple

	def to_str(self):
		return str(sympy.latex(self.to_expr()))

	def __str__(self):
		return self.to_str()

	def __repr__(self):
		return self.to_str()

class SecondOrderCurves(SecondOrder):

	def __init__(self, seconds: Matrix.Matrix, firsts: Matrix.Vector, free: float):
		super().__init__(2, seconds, firsts, free)

	@staticmethod
	def generate_ellipse(horizontal: float, vertical: float, centered: tuple[float, float]):
		a = horizontal
		b = vertical
		c, d = centered

		mtx = Matrix.Matrix.from_list_of_lists([[1/a**2, 0], [0, 1/b**2]])
		vec = Matrix.Vector.from_list([-2*c/a**2, -2*d/b**2])
		free = c**2/a**2 + d**2/b**2 - 1

		return SecondOrderCurves(mtx, vec, free)

	@staticmethod
	def generate_hyperbola(horizontal: float, vertical: float, centered: tuple[float, float]):
		a = horizontal
		b = vertical
		c, d = centered

		mtx = Matrix.Matrix.from_list_of_lists([[1/a**2, 0], [0, -1/b**2]])
		vec = Matrix.Vector.from_list([-2*c/a**2, 2*d/b**2])
		free = c**2/a**2 - d**2/b**2 - 1

		return SecondOrderCurves(mtx, vec, free)

	@staticmethod
	def generate_parabola(parameter: float, centered: tuple[float, float]):
		p = parameter
		c, d = centered

		mtx = Matrix.Matrix.from_list_of_lists([[0, 0], [0, 1]])
		vec = Matrix.Vector.from_list([-2*p, -2*d])
		free = d**2 + 2*p*c

		return SecondOrderCurves(mtx, vec, free)

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
		
	for i in range(30):
		s.append(SecondOrderCurves.generate_parabola( *(list(func())[1:]) ))

	random.shuffle(s)
	for i in s:
		print(f"\\item \\( {str(i)} = 0 \\);")