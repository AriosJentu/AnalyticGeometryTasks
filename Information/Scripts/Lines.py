import random

def generate_point_name(*excepts: list[str]) -> str:
	if not excepts:
		excepts = []

	ordA = ord("A")
	ordW = ord("W")

	ords = [ord(i) for i in excepts]
	numbers = [i for i in range(ordA, ordW+1) if i not in ords]

	return chr(random.choice(numbers))

def generate_variables(size: int = 2) -> list[str]:
	basic = ["x", "y", "z", "w", "t"]
	other = [chr(ord("a")+i) for i in range(size-5)]
	return (basic + other)[:size]

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

class Linear:

	def __init__(self, variable: str, diff: int, multiplier: int = 1):
		self._variable = variable
		
		self._diff = abs(diff)
		self._diff_sign = ["-", "+"][abs(diff) == diff]
		
		self._multiplier = abs(multiplier)
		self._multiplier_sign = ["-", "+"][abs(multiplier) == multiplier]

	def to_str(self):

		if self._diff == 0 and self._multiplier == 0:
			return "0"

		real = f"{self._diff}"
		variable = f"{self._multiplier}{self._variable}"

		if self._multiplier == 1:
			variable = f"{self._variable}"

		signreal = self._diff_sign
		signvariable = self._multiplier_sign

		if self._diff == 0:
			real = ""
			signreal = ""

		if self._multiplier == 0:
			variable = ""
			signvariable = ""

		if signvariable == "-" and signreal == "+":
			if signreal == "+":
				signreal = ""

			if real == "" and signvariable == "+":
				signvariable = ""
			
			return f"{signreal}{real}{signvariable}{variable}"

		else:
			if signvariable == "+":
				signvariable = ""

			if variable == "" and signreal == "+":
				signreal = ""

			return f"{signvariable}{variable}{signreal}{real}"

	def __str__(self):
		return self.to_str()


class Line:

	def __init__(self, dimension: int = 2, maxvalue: int = 10):
		self._dimension = dimension
		self._maxvalue = maxvalue
		self._point1 = Point(*[0 for i in range(dimension)])
		self._point2 = Point(*[0 for i in range(dimension)])

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
			numer = Linear(variables[i], point1.point[i])
			denom = pdiff.point[i]
			parts.append(f"\\frac{{{numer.to_str()}}}{{{denom}}}")

		return " = ".join(parts)

	def to_parametric_form(self):

		parts = []
		variables = generate_variables(self.dimension)
		parameter = ["t", "u"][self.dimension > 4]

		pdiff = self._point2 - self._point1

		for i in range(self.dimension):
			right = Linear(parameter, self._point1.point[i], pdiff.point[i])
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

def main(*args):

	line = Line(2)
	line.generate_random_line_points()
	print(line.to_points_form())
	print(line.to_canonical_form())
	print(line.to_parametric_form())
	print(line.to_random_form())

	print()

	line = Line(3)
	line.generate_random_line_points()
	print(line.to_points_form())
	print(line.to_canonical_form())
	print(line.to_parametric_form())
	print(line.to_random_form())


if __name__ == "__main__":
	main()
