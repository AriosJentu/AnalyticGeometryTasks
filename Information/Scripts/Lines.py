import random

if __package__ == "" or __package__ is None:
	import Expression
	import Matrix
else: 
	from . import Expression
	from . import Matrix

def generate_point_name(*excepts: list[str]) -> str:
	if not excepts:
		excepts = []

	ordA = ord("A")
	ordW = ord("W")

	ords = [ord(i) for i in excepts]
	numbers = [i for i in range(ordA, ordW+1) if i not in ords]

	return chr(random.choice(numbers))

def generate_variables(size: int = 2) -> list[Expression.Variable]:
	basic = ["x", "y", "z", "w", "t"]
	other = [chr(ord("a")+i) for i in range(size-5)]
	return [
		Expression.Variable(var)
		for var in (basic + other)[:size]
	]

def generate_parameter(dimension: int = 2) -> Expression.Variable:
	if dimension <= 4:
		return Expression.Variable("t")
	else:
		return Expression.Variable("v")

class Point:

	def __init__(self, *coordinates: tuple[int]):
		self._point = coordinates

	@classmethod
	def generate_random_point(cls, 
			dimension: int = 2, 
			maxvalue: int = 10
	) -> 'Point':
		return Point(*[
			random.randint(-maxvalue, maxvalue) 
			for _ in range(dimension)
		])

	@property
	def x(self) -> int:
		if self.dimension > 0:
			return self._point[0]

	@property
	def y(self) -> int:
		if self.dimension > 1:
			return self._point[1]

	@property
	def z(self) -> int:
		if self.dimension > 2:
			return self._point[2]

	@property
	def w(self) -> int:
		if self.dimension > 3:
			return self._point[3]

	@property
	def t(self) -> int:
		if self.dimension > 4:
			return self._point[4]

	@property
	def point(self) -> tuple:
		return self._point

	@property
	def dimension(self) -> int:
		return len(self.point)

	def add(self, point: 'Point') -> 'Point':
		if self.dimension == point.dimension:
			return Point(*[ 
				self.point[i] + point.point[i] 
				for i in range(self.dimension) 
			])

	def multiply(self, value: float) -> 'Point':
		return Point(*[i*value for i in self.point])

	def to_str(self, name: str = None) -> str:
		if not name:
			return str(self._point)
		else:
			return f"{name} = {str(self._point)}"

	def __str__(self) -> str:
		return self.to_str()

	def __add__(self, point: 'Point') -> 'Point':
		return self.add(point)

	def __sub__(self, point: 'Point') -> 'Point':
		return self.add(point.multiply(-1))

	def __mul__(self, value: float) -> 'Point':
		return self.multiply(value)

	def __rmul__(self, value: float) -> 'Point':
		return self.multiply(value) 


class Line:

	def __init__(self, dimension: int = 2, maxvalue: int = 10):
		if dimension < 2:
			return 

		self._dimension = dimension
		self._maxvalue = maxvalue
		self._point1 = Point(*[0 for _ in range(dimension)])
		self._point2 = Point(*[0 for _ in range(dimension)])

	def generate_random_line_points(self):
		self._point1 = Point.generate_random_point(self._dimension, self._maxvalue)
		self._point2 = Point.generate_random_point(self._dimension, self._maxvalue)

	def set_points(self, point1: Point, point2: Point):
		if point1.dimension == point2.dimension == self.dimension:
			self._point1 = point1
			self._point2 = point2

	@property
	def dimension(self) -> int:
		return self._dimension

	def to_points_form(self):
		pointM = generate_point_name()
		pointN = generate_point_name(pointM)
		return f"{self._point1.to_str(pointM)}, ~ {self._point2.to_str(pointN)}"

	def to_canonical_form(self):
		
		parts = []
		variables = generate_variables(self.dimension)

		pdiff = self._point2 - self._point1
		point1 = self._point1*(-1)
		
		for i in range(self.dimension):
			numer = Expression.LinearExpression(variables[i], point1.point[i])
			numer.shuffle()
			denom = pdiff.point[i]
			parts.append(f"\\frac{{{numer.to_str()}}}{{{denom}}}")

		return " = ".join(parts)

	def to_parametric_form(self):

		parts = []
		variables = generate_variables(self.dimension)
		parameter = generate_parameter(self.dimension)

		pdiff = self._point2 - self._point1

		for i in range(self.dimension):
			right = Expression.LinearExpression(
				parameter*pdiff.point[i], 
				self._point1.point[i]
			)
			right.shuffle()

			parts.append(f"{variables[i]} &= {right.to_str()}")

		result = " \\\\\n\t\t\t".join(parts)
		return f"""\t\t\\left\\lbrace \\begin{{split}}
			{result}
		\\end{{split}} \\right."""

	def to_random_form(self):
		form = random.choice([
			self.to_points_form,
			self.to_canonical_form,
			self.to_parametric_form
		])
		return form()

	def __str__(self):
		return self.to_random_form()

class HyperPlane:

	def __init__(self, dimension: int = 3, maxvalue: int = 4):
		if dimension < 2:
			return 

		self._dimension = dimension
		self._maxvalue = maxvalue
		self._points = [
			Point(*[0 for _ in range(dimension)]) 
			for _ in range(dimension)
		]

	@property
	def dimension(self) -> int:
		return self._dimension

	def generate_random_plane_points(self):
		for i in range(self.dimension):
			point = Point.generate_random_point(self.dimension, self._maxvalue)
			self._points[i] = point

	def set_points(self, points: list[Point]):
		if not points:
			points = []

		conditions = [
			point.dimension == self.dimension
			for point in points
		]

		if len(conditions) == self.dimension and False not in conditions:
			self._points = points

	def to_points_form(self):
		pnames = []
		for _ in range(self.dimension):
			pnames.append(generate_point_name(*pnames))

		points = [
			self._points[i].to_str(pnames[i])
			for i in range(self.dimension)
		]

		return ", ~ ".join(points)

	def to_planar_form(self):
		variables = generate_variables(self.dimension)

		top_vector = Matrix.Vector.from_list([
			Expression.LinearExpression(variables[i]) - self._points[0].point[i]
			for i in range(self.dimension)
		])
		other_vectors = [
			Matrix.Vector.from_list([
				self._points[i].point[j] - self._points[0].point[j]
				for j in range(self.dimension)
			])
			for i in range(1, self.dimension)
		]

		matrix = Matrix.Matrix.from_list_of_vectors([top_vector] + other_vectors)
		expression = matrix.determinant()
		mul = expression.get_common_multiplicator()
		
		expression = expression*(1/mul)
		expression.int()
		expression.shuffle()
		expression.as_positive()
		
		coeff = expression.get_free_coefficient()*(-1)
		
		if coeff.is_positive():
			expression = expression + coeff
			coeff = coeff.to_str()
		else:
			coeff = ""
		
		if not coeff:
			coeff = "0"

		return f"{expression.to_str()} = {coeff}"


def main(*args):

	line = Line(2)
	line.generate_random_line_points()
	# print(line.to_points_form())
	# print(line.to_canonical_form())
	# print(line.to_parametric_form())
	# print(line.to_random_form())

	print()

	line = Line(3)
	line.generate_random_line_points()
	# print(line.to_points_form())
	# print(line.to_canonical_form())
	# print(line.to_parametric_form())
	# print(line.to_random_form())

	hplane = HyperPlane(3)
	hplane.generate_random_plane_points()
	print(hplane.to_points_form())
	print(hplane.to_planar_form())


if __name__ == "__main__":
	main()
