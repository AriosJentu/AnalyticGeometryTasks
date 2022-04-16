import random
import math

POSITIVE_ANGLES = [
	"\\dfrac{{\\pi}}{{6}}", 
	"\\dfrac{{\\pi}}{{4}}", 
	"\\dfrac{{\\pi}}{{3}}", 
	"\\dfrac{{\\pi}}{{2}}", 
	"\\dfrac{{2\\pi}}{{3}}",
	"\\dfrac{{3\\pi}}{{4}}",
	"\\dfrac{{5\\pi}}{{6}}",
	"\\pi",
	"\\dfrac{{7\\pi}}{{6}}", 
	"\\dfrac{{5\\pi}}{{4}}", 
	"\\dfrac{{4\\pi}}{{3}}", 
	"\\dfrac{{3\\pi}}{{2}}", 
	"\\dfrac{{5\\pi}}{{3}}", 
	"\\dfrac{{7\\pi}}{{4}}", 
	"\\dfrac{{7\\pi}}{{6}}", 
]

POSITIVE_DOUBLE_ANGLES = [
	"\\dfrac{{\\pi}}{{3}}", 
	"\\dfrac{{\\pi}}{{2}}", 
	"\\dfrac{{2\\pi}}{{3}}",
	"\\pi",
	"\\dfrac{{4\\pi}}{{3}}", 
	"\\dfrac{{3\\pi}}{{2}}", 
	"\\dfrac{{5\\pi}}{{3}}", 
]


NEGATIVE_ANGLES = [f"-{i}" for i in POSITIVE_ANGLES[::-1]]
NEGATIVE_DOUBLE_ANGLES = [f"-{i}" for i in POSITIVE_DOUBLE_ANGLES[::-1]]

ANGLES = NEGATIVE_ANGLES + ["0"] + POSITIVE_ANGLES
ANGLES_DOUBLE = NEGATIVE_DOUBLE_ANGLES + ["0"] + POSITIVE_DOUBLE_ANGLES

if __package__ == "" or __package__ is None:
	import Expression
	import Fraction
	import Matrix
else: 
	from . import Expression
	from . import Fraction
	from . import Matrix

def generate_point_name(*excepts: list[str]) -> str:
	if not excepts:
		excepts = []

	ordA = ord("A")
	ordW = ord("W")

	ords = [ord(i) for i in excepts]
	numbers = [i for i in range(ordA, ordW+1) if i not in ords]

	return chr(random.choice(numbers))

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
	return [
		Expression.Variable(formats(var))
		for var in (basic + other)[:size]
	]

def generate_parameters(
		dimension: int = 2, count: int = 1
) -> list[Expression.Variable]:
	variables = ["t", "v"]
	other = [chr(ord("g")+i) for i in range(count-2)]
	variables = [Expression.Variable(i) for i in variables+other]

	if dimension <= 4:
		return variables[:count]
	else:
		return variables[1:count+1]

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
			return self.point[0]

	@property
	def y(self) -> int:
		if self.dimension > 1:
			return self.point[1]

	@property
	def z(self) -> int:
		if self.dimension > 2:
			return self.point[2]

	@property
	def w(self) -> int:
		if self.dimension > 3:
			return self.point[3]

	@property
	def t(self) -> int:
		if self.dimension > 4:
			return self.point[4]

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

	def floordivide(self, value: float) -> 'Point':
		return Point(*[i//value for i in self.point])

	def equal(self, point: 'Point') -> bool:
		if self.dimension != point.dimension:
			return False

		return False not in [
			self.point[i] == point.point[i]
			for i in range(self.dimension)
		]

	def as_point(self) -> str:
		result = ", ".join([
			str(Fraction.Fraction(i))
			for i in self.point
		])
		return f"""\\left( {result} \\right)"""

	def as_real(self) -> str:
		result = ", ".join([str(i) for i in self.point])
		return f"""\\left( {result} \\right)"""

	def to_str(self, name: str = None) -> str:
		if not name:
			return self.as_point()
		else:
			return f"{name} = {self.as_point()}"

	def __str__(self) -> str:
		return self.to_str()

	def __repr__(self) -> str:
		return self.to_str()

	def __add__(self, point: 'Point') -> 'Point':
		return self.add(point)

	def __sub__(self, point: 'Point') -> 'Point':
		return self.add(point.multiply(-1))

	def __neg__(self) -> 'Point':
		return self*(-1)

	def __pos__(self) -> 'Point':
		return self*1

	def __mul__(self, value: float) -> 'Point':
		return self.multiply(value)

	def __rmul__(self, value: float) -> 'Point':
		return self.multiply(value) 

	def __truediv__(self, value: float) -> 'Point':
		return self.multiply(1/value)

	def __floordiv__(self, value: float) -> 'Point':
		return self.floordivide(value)

	def __eq__(self, point: 'Point') -> bool:
		return self.equal(point)

	def __ne__(self, point: 'Point') -> bool:
		return not self.equal(point)

class Vector(Point):

	def __init__(self, *coordinates: tuple[int], **root):
		self._point = coordinates
		self._root = root.get("root", 0)

	@property
	def vector(self) -> tuple:
		return self._point

	@classmethod
	def generate_random_vector(cls, 
			dimension: int = 2, 
			maxvalue: int = 10
	) -> 'Vector':
		v = super().generate_random_point(dimension, maxvalue).point
		if v.count(0) != len(v):
			return Vector(*v)
		else:
			return cls.generate_random_vector(dimension, maxvalue)

	def sum_squares(self) -> int:
		return sum([i**2 for i in self.point])

	def dot_product(self, vector: 'Vector') -> float:
		if self.dimension != vector.dimension:
			return False

		sums = 0
		for i in range(self.dimension):
			sums += self.vector[i] * vector.vector[i]

		return sums

	def cross_product(self, vector: 'Vector') -> 'Vector':
		if self.dimension == vector.dimension == 3:
			a, b, c = self.x, self.y, self.z
			f, g, h = vector.x, vector.y, vector.z

			p1 = abs(Matrix.Matrix.from_list_of_lists([[b, c], [g, h]]))
			p2 = -abs(Matrix.Matrix.from_list_of_lists([[a, c], [f, h]]))
			p3 = abs(Matrix.Matrix.from_list_of_lists([[a, b], [f, g]]))

			return Vector(p1, p2, p3)

	def add(self, vector: 'Vector') -> 'Vector':
		if self.dimension == vector.dimension:
			return Vector(*[ 
				self.point[i] + vector.point[i] 
				for i in range(self.dimension) 
			])

	def multiply(self, element: (float, 'Vector')) -> ('Vector', float):
		if isinstance(element, Vector):
			return self.dot_product(element)
		else:
			return Vector(*[i*element for i in self.point])

	def len(self) -> float:
		return self.sum_squares()**(1/2)

	def len_str(self, name: str = None) -> str:
		sums = self.sum_squares()
		fstring = (
			"\\left\\lvert {name} \\right\\rvert = {len}" 
			if name else "{len}"
		)

		if int(self.len()) == self.len():
			length = int(self.len())
			return fstring.format(name=name, len=length)
		else:
			return fstring.format(name=name, len=f"\\sqrt{{{sums}}}")

	def get_normalized(self) -> 'Vector':
		if self.sum_squares() == 0:
			return Vector(*self.point)

		return Vector(
			*(self/self.sum_squares()).point, 
			root=self.sum_squares()
		)

	def vector_format(self, string: str) -> str:
		return f"\\vec{{{string}}}"

	def as_point(self) -> str:
		result = ", ".join([
			str(Fraction.Fraction(i, self._root))
			for i in self.point
		])
		return f"""\\left( {result} \\right)"""

	def as_vector(self) -> str:
		result = ", ".join([
			str(Fraction.Fraction(i))
			for i in self.point
		])
		return f"""\\left\\lbrace {result} \\right\\rbrace"""

	def as_real(self) -> str:
		result = ", ".join([str(i) for i in self.point])
		return f"""\\left\\lbrace {result} \\right\\rbrace"""

	def to_str(self, name: str = None) -> str:
		if not name:
			return self.as_vector()
		else:
			return f"{self.vector_format(name)} = {self.as_vector()}"

	def __pow__(self, vector: 'Vector') -> 'Vector':
		return self.cross_product(vector)

	def __rpow__(self, vector: 'Vector') -> 'Vector':
		return vector.cross_product(self)


class Line:

	def __init__(self, dimension: int = 2, maxvalue: int = 10):
		if dimension < 2:
			return 

		self._dimension = dimension
		self._maxvalue = maxvalue
		self._points = [
			Point(*[0 for _ in range(dimension)])
			for _ in range(2)
		]

	def generate_random_line_points(self):
		self._points = [
			Point.generate_random_point(self._dimension, self._maxvalue)
			for _ in range(2)
		]

	def set_points(self, *points: tuple[Point]):
		if not points:
			points = []

		conditions = [
			point.dimension == self.dimension
			for point in points
		]

		if len(conditions) == 2 and False not in conditions:
			self._points = points

	@property
	def dimension(self) -> int:
		return self._dimension

	def to_points_form(self) -> str:
		pnames = []
		for _ in range(2):
			pnames.append(generate_point_name(*pnames))

		p1, p2 = [
			point.to_str(pnames[index]) 
			for index, point in enumerate(self._points)
		] 

		result = f"&{p1}\\\\\n\t\t\t&{p2}"
		return f"""\t\t\\left[ \\begin{{split}}
			{result}
		\\end{{split}} \\right."""

	def to_canonical_form(self) -> str:
		
		parts = []
		variables = generate_variables(self.dimension)

		pdiff = self._points[1] - self._points[0]
		point1 = self._points[0]*(-1)
		
		for i in range(self.dimension):
			numer = Expression.LinearExpression(variables[i], point1.point[i])
			numer.shuffle()
			denom = pdiff.point[i]
			parts.append(f"\\frac{{{numer.to_str()}}}{{{denom}}}")

		return " = ".join(parts)

	def to_parametric_form(self) -> str:

		parts = []
		variables = generate_variables(self.dimension)
		parameter = generate_parameters(self.dimension)[0]

		pdiff = self._points[1] - self._points[0]

		for i in range(self.dimension):
			right = Expression.LinearExpression(
				parameter*pdiff.point[i], 
				self._points[0].point[i]
			)
			right.shuffle()

			parts.append(f"{variables[i]} &= {right.to_str()}")

		result = " \\\\\n\t\t\t".join(parts)
		return f"""\t\t\\left\\lbrace \\begin{{split}}
			{result}
		\\end{{split}} \\right."""

	def to_random_form(self) -> str:
		form = random.choice([
			self.to_points_form,
			self.to_canonical_form,
			self.to_parametric_form
		])
		return form()

	def add(self, line: 'Line') -> 'Line':
		if self.dimension == line.dimension:
			line = Line(self.dimension, self._maxvalue)
			line.set_points(*[
				self._points[i] + line._points[i]
				for i in range(len(self._points))
			])

			return line

	def multiply(self, value: float) -> 'Line':
		line = Line(self.dimension, self._maxvalue)
		line.set_points(*[
			self._points[i]*value
			for i in range(len(self._points))
		])

		return line


	def floordivide(self, value: float) -> 'Point':
		line = Line(self.dimension, self._maxvalue)
		line.set_points(*[
			self._points[i]//value
			for i in range(len(self._points))
		])

		return line

	def __add__(self, line: 'Line') -> 'Line':
		return self.add(line)

	def __sub__(self, line: 'Line') -> 'Line':
		return self.add(line.multiply(-1))

	def __mul__(self, value: float) -> 'Line':
		return self.multiply(value)

	def __rmul__(self, value: float) -> 'Line':
		return self.multiply(value) 

	def __truediv__(self, value: float) -> 'Point':
		return self.multiply(1/value)

	def __floordiv__(self, value: float) -> 'Point':
		return self.floordivide(value)

	def __str__(self) -> str:
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
		self._points = [
			Point.generate_random_point(self.dimension, self._maxvalue)
			for _ in range(self.dimension)
		]

	def set_points(self, *points: tuple[Point]):
		if not points:
			points = []

		conditions = [
			point.dimension == self.dimension
			for point in points
		]

		if len(conditions) == self.dimension and False not in conditions:
			self._points = points

	def to_points_form(self) -> str:
		pnames = []
		for _ in range(self.dimension):
			pnames.append(generate_point_name(*pnames))

		points = [
			"&"+self._points[i].to_str(pnames[i])
			for i in range(self.dimension)
		]

		result = "\\\\\n\t\t\t".join(points)
		return f"""\t\t\\left[ \\begin{{split}}
			{result}
		\\end{{split}} \\right."""

	def to_canonical_form(self) -> str:
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

	def to_parametric_form(self) -> str:
		variables = generate_variables(self.dimension)
		parameters = generate_parameters(self.dimension, self.dimension-1)

		expressions = []
		for i in range(self.dimension):
			expr = Expression.LinearExpression()
			for j in range(self.dimension-1):
				difvar = self._points[j+1].point[i] - self._points[0].point[i]
				expr = expr + parameters[j]*difvar
			expr = expr + self._points[0].point[i]
			expr.shuffle()
			expressions.append(expr)
		
		parts = [
			f"{variables[i]} &= {expr.to_str()}" 
			for i, expr in enumerate(expressions)
		]
		result = " \\\\\n\t\t\t".join(parts)

		return f"""\t\t\\left\\lbrace \\begin{{split}}
			{result}
		\\end{{split}} \\right."""

	def to_random_form(self) -> str:
		form = random.choice([
			self.to_points_form,
			self.to_canonical_form,
			self.to_parametric_form
		])
		return form()

	def __str__(self):
		return self.to_random_form()


class ScalarProduct:

	def __init__(self, 
			dimension: int = 2, 
			vectors_count: int = 2,
			maxvalue: int = 5
	):
		if dimension < 2:
			return 

		self._dimension = dimension
		self._count = vectors_count
		self._maxvalue = maxvalue
		self._vectors = [
			Vector(*[0 for _ in range(dimension)]) 
			for _ in range(vectors_count)
		]

	@property
	def dimension(self) -> int:
		return self._dimension

	def generate_random_vectors(self):
		self._vectors = [
			Vector.generate_random_vector(self.dimension, self._maxvalue)
			for _ in range(self._count)
		]

	def set_vectors(self, *vectors: tuple[Vector]):
		if not vectors:
			vectors = []

		conditions = [
			vector.dimension == self.dimension
			for vector in vectors
		]

		if len(conditions) == self._count and False not in conditions:
			self._vectors = vectors

	def get_cosine(self) -> float:
		v1, v2 = self._vectors[:2]
		return v1*v2/(v1.len()*v2.len())

	def get_cosine_frac(self) -> Fraction.Fraction:
		v1, v2 = self._vectors[:2]
		numer = v1*v2
		denom = v1.len()*v2.len()
		return Fraction.Fraction(numer/denom**2, root=int(denom**2))

	def get_angle(self) -> float:
		return math.acos(self.get_cosine())

	def get_scalar_product(self) -> float:
		v1, v2 = self._vectors[:2]
		return v1*v2

	def vector_format(self, string: str) -> str:
		return f"\\vec{{{string}}}"

	def __to_vector_points__(self, 
			chars: list[Expression.Variable]
	) -> str:
		return ", ~".join([
			v.to_str(chars[i].to_str()) 
			for i, v in enumerate(self._vectors)
			if i < len(chars)-1
		])

	def __to_vector_lengths__(self,
			chars: list[Expression.Variable]
	) -> str:
		return ", ~".join([
			v.len_str(chars[i].to_str()) 
			for i, v in enumerate(self._vectors)
			if i < len(chars)-1
		])

	def __to_vector_lengths_cosine__(self, 
			chars: list[Expression.Variable]
	) -> str:
		cosine = ", \\quad \\cos{{\\alpha}} = "
		vlen = self.__to_vector_lengths__(chars)
		return vlen + cosine + str(self.get_cosine_frac())

	def __to_scalar_product_form__(self, 
			chars: list[Expression.Variable], 
			expr: list[str],
			function = None
	) -> str:
		if not function:
			function = self.__to_vector_points__

		vectors = function(chars)

		if len(expr) == 1:
			expression = f"{chars[-1]} = {expr[0]};"
		else:
			result = "\\\\\n\t\t\t".join([
				f"{chars[len(chars)-len(expr)+i]} &= {expr[i]}"
				for i in range(len(expr))
				if i < len(chars)-1
			])
			expression = "\t\t\\left\\lbrace \\begin{split}\n\t\t\t"
			expression += result
			expression += "\n\t\t\\end{split} \\right."
		
		return f"{expression} ~ {vectors}"

	def __create_expression__(self, 
			chars: list[Expression.Variable], 
			count: int = 2
	):
		exprs = []
		for i in range(count):
			expr = Expression.LinearExpression()
		
			for i in range(self._count):
				expr = expr + chars[i]*random.choice([
					i
					for i in range(-self._maxvalue, self._maxvalue)
					if i != 0
				])

			exprs.append(expr)

		return exprs

	def to_scalar_product_form(self) -> str:
		chars = generate_variables(self._count+1, False, self.vector_format)
		expr = " \\cdot ".join([str(i) for i in chars[:-1]])
		return self.__to_scalar_product_form__(chars, [expr])

	def to_linear_scalar_product_form(self, count: int = 2) -> str:
		chars = generate_variables(self._count+count, False, self.vector_format)
		exprs = self.__create_expression__(chars, count)
		return self.__to_scalar_product_form__(chars, exprs)

	def to_length_scalar_product_form(self) -> str:
		chars = generate_variables(3, False, self.vector_format)
		expr = " \\cdot ".join([str(i) for i in chars[:-1]])
		return self.__to_scalar_product_form__(
			chars, [expr], self.__to_vector_lengths_cosine__
		)

	def to_vectors_form(self) -> str:
		chars = generate_variables(2, False, self.vector_format)
		return f"""{
			', '.join([
				v.to_str(chars[i]) 
				for i, v in enumerate(self._vectors)
				if i < 2
			])
		}"""

	def to_lengths_form(self) -> str:
		chars = generate_variables(2, False, self.vector_format)
		vlength = self.__to_vector_lengths__(chars+[None])
		products = ' \\cdot '.join([i.to_str() for i in chars])
		prod = str(self.get_scalar_product())
		return f"{vlength}, ~ {products} = {prod}"

def main(*args):

	line = Line(2)
	line.generate_random_line_points()
	# print(line.to_points_form())
	# print(line.to_canonical_form())
	# print(line.to_parametric_form())
	# print(line.to_random_form())

	# print()

	line = Line(3)
	line.generate_random_line_points()
	# print(line.to_points_form())
	# print(line.to_canonical_form())
	# print(line.to_parametric_form())
	# print(line.to_random_form())

	hplane = HyperPlane(2)
	hplane.generate_random_plane_points()
	# print(hplane.to_points_form())
	# print(hplane.to_canonical_form())
	# print(hplane.to_parametric_form())

	hplane = HyperPlane(4)
	hplane.generate_random_plane_points()
	# print(hplane.to_points_form())
	# print(hplane.to_canonical_form())
	# print(hplane.to_parametric_form())

	points = [Point(random.randint(0, 5), random.randint(0, 5)), Point(random.randint(0, 5), random.randint(0, 5))]
	# points = [Point(1, 5), Point(1, 5)]

	line = Line(2)
	line.set_points(*points)

	hplane = HyperPlane(2)
	hplane.set_points(*points)

	# print(line.to_points_form())
	# print(hplane.to_points_form())
	# print()

	# print(line.to_canonical_form())
	# print(hplane.to_canonical_form())
	# print()
	
	# print(line.to_parametric_form())
	# print(hplane.to_parametric_form())
	# print()

	# vector = Vector(4, 2)
	# print(vector)
	# print(vector.len())
	# print(vector.len_str("a"))
	# print()
	# print(vector.get_normalized())

	sprod = ScalarProduct(2, 5, 3)
	# sprod.set_vectors(Vector(2, -2), Vector(1, 0))
	sprod.generate_random_vectors()
	# cosine = sprod.get_cosine()
	cosine_frac = sprod.get_cosine_frac()
	angle = sprod.get_angle()
	# print(sprod._vectors)
	# print(cosine, angle)
	# print(Fraction.Fraction(angle, prefered=1))
	# print(cosine_frac)
	# print(Fraction.Fraction(1/4))
	
	# print(sprod.to_scalar_product_form())
	# print(sprod.to_linear_scalar_product_form())
	print(sprod.to_length_scalar_product_form())
	# print(sprod.to_vectors_form())
	# print(sprod.to_lengths_form())

	vec = Vector(1, 2, 3)
	print(vec.to_str("a"))




if __name__ == "__main__":
	main()
