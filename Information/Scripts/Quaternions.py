import random

if __package__ == "" or __package__ is None:
	from Lines import Vector
else: 
	from .Lines import Vector

class Expression:

	EXPRESSIONS = [
		"\\frac{{#C#w_1 + #D#w_2}}{{w_3}}",
		"\\frac{{#C#w_1 - #D#w_2}}{{w_3}}",
		"\\frac{{#C#w_1 \\cdot w_2}}{{w_3}}",
		"#C#w_1 \\cdot w_2 + #D#w_3",
		"#C#w_1 \\cdot w_2 - #D#w_3",
		"#C#w_1 \\cdot w_2 \\cdot w_3",
	]

	@staticmethod
	def generate_expression():

		expr = random.choice(Expression.EXPRESSIONS)
		expr = expr.replace("#C#", str(random.randint(2, 6)))
		expr = expr.replace("#D#", str(random.randint(2, 6)))

		return "w = "+expr


class Quaternion:

	def __init__(self, real: float, imag: Vector(float, float, float)):
		self.real = real
		self.imag = imag

	@staticmethod
	def from_values(a: float = 0, b: float = 0, c: float = 0, d: float = 0):
		return Quaternion(a, Vector(b, c, d))

	def is_imag_zero(self, b: bool = True, c: bool = True, d: bool = True) -> bool:
		b1 = self.imag.x == 0 or not b
		c1 = self.imag.y == 0 or not c
		d1 = self.imag.z == 0 or not d

		return b1 and b2 and b3

	@staticmethod
	def generate_random_number(irange: int = 3) -> 'Quaternion':
		random.seed()

		a = random.randint(-irange, irange)
		b = random.randint(-irange, irange)
		c = random.randint(-irange, irange)
		d = random.randint(-irange, irange)

		return Quaternion.from_values(a, b, c, d)

	def sum(self, number: 'Quaternion') -> 'Quaternion':
		if isinstance(number, (int, float)):
			return Quaternion(self.real + number, self.imag)

		elif isinstance(number, complex):
			imag = Vector(number.imag, 0, 0)
			return Quaternion(self.real + number.real, self.imag + imag)

		elif isinstance(number, Quaternion):
			return Quaternion(self.real + number.real, self.imag + number.imag)

	def multiply_by_quaternion(self, number: 'Quaternion') -> 'Quaternion':
		real = self.real * number.real - self.imag*number.imag
		imag = self.real*number.imag + number.real*self.imag + self.imag**number.imag
		return Quaternion(real, imag)

	def multiply(self, number: [int, float, complex, 'Quaternion']) -> 'Quaternion':
		if isinstance(number, (int, float)):
			return Quaternion(self.real*number, self.imag*number)

		elif isinstance(number, complex):
			return self.multiply_by_quaternion(
				Quaternion(number.real, Vector(number.imag, 0, 0) )
			)

		elif isinstance(number, Quaternion):
			return self.multiply_by_quaternion(number)

	def len(self) -> float:
		return (self.real**2 + self.imag.len()**2)**(1/2)

	@property
	def conjugate(self) -> 'Quaternion':
		return Quaternion(self.real, -self.imag)

	def inverse(self) -> 'Quaternion':
		return (self.conjugate)/(self.len()**2)

	def __compare_equality__(self, value: [int, float, complex, 'Quaternion']) -> bool:
		if isinstance(value, (int, float)):
			return self.real == value and self.is_imag_zero()
		elif isinstance(value, complex):
			return self.real == value.real and self.imag.x == value.imag and self.is_imag_zero(False)
		elif isinstance(value, Quaternion):
			return self.real == value.real and self.imag == value.imag

	def __nonzero_str__(self, value: float, key: str, nonzero: bool, nonreal: bool) -> str:
		res = ""
		if value != 0:
			if value > 0 and nonzero:
				res += "+"

			if nonreal:
				value = str(value) if abs(value) != 1 else str(value)[:-1]

			res += str(value) + key

		return res

	def __round_elements__(self, element, size):
		element = round(element, size)
		if element == int(element):
			element = int(element)

		return element


	def str(self, iround=3) -> str:
		a, b, c, d = self.real, self.imag.x, self.imag.y, self.imag.z

		if iround > 0:
			a = self.__round_elements__(a, iround)
			b = self.__round_elements__(b, iround)
			c = self.__round_elements__(c, iround)
			d = self.__round_elements__(d, iround)

		res = ""
		res += self.__nonzero_str__(a, "", len(res) > 0, False)
		res += self.__nonzero_str__(b, "i", len(res) > 0, True)
		res += self.__nonzero_str__(c, "j", len(res) > 0, True)
		res += self.__nonzero_str__(d, "k", len(res) > 0, True)

		if len(res) == 0:
			res = "0"

		return res

	def __add__(self, number: 'Quaternion') -> 'Quaternion':
		return self.sum(number)

	def __radd__(self, number: 'Quaternion') -> 'Quaternion':
		return self.sum(number)

	def __mul__(self, number: 'Quaternion') -> 'Quaternion':
		return self.multiply(number)

	def __rmul__(self, number: 'Quaternion') -> 'Quaternion':
		if isinstance(number, Quaternion):
			return number.multiply(self)
		else:
			return self*number

	def __sub__(self, number: 'Quaternion') -> 'Quaternion':
		return self.sum(-number)

	def __rsub__(self, number: 'Quaternion') -> 'Quaternion':
		return -self.sum(number)

	def __neg__(self) -> 'Quaternion':
		return Quaternion(-self.real, -self.imag)

	def __truediv__(self, number: 'Quaternion') -> 'Quaternion':
		if isinstance(number, Quaternion):
			return self*number.inverse()
		else:
			return self*(1/number)

	def __rtruediv__(self, number: 'Quaternion') -> 'Quaternion':
		return number*self.inverse()

	def __eq__(self, number: 'Quaternion') -> bool:
		return self.__compare_equality__(number)
	
	def __ne__(self, number: 'Quaternion') -> bool:
		return not self.__compare_equality__(number)

	def __str__(self):
		return self.str()

	def __repr__(self):
		return self.str()


if __name__ == "__main__":

	import math

	x = Quaternion(0, Vector(1, 0, 0))
	y = Quaternion(0, Vector(0, 1, 0))
	# print(x, y)
	# print(x*y)
	# print(y*x)
	# print(x+y)
	# print(x-y)

	z = Quaternion(1, Vector(1, 1, 0))
	# print(3*z.inverse())

	#--------------------------------------------------------------------------------------------------------------------------

	#Quaternion rotation
	def rotate(point: Vector, axis: Vector, angle: float):
		# 1) Define point on 3D space, but define it as vector:
		# 2) Define axis direction which will be axis of rotation:
		# 3) Define angle of rotation around this axis:

		# 4) Define rotation quaternion around axis for specific angle (it's half of the angle, COS is real part, SIN is imaginary)
		q = Quaternion(math.cos(angle/2), axis*math.sin(angle/2))

		# 5) Find inverse of this rotation quaternion:
		qi = q.inverse()

		# 6) Convert 3D point to quaternion with 0 real part:
		point = Quaternion(0, point)

		# 7) Rotate point with formula: p1 = q * p * q^{-1}:
		point1 = q * point * qi

		# 8) Convert new point back to vector:
		point1 = point1.imag

		return point1

	#Rotation examples:
	print(rotate(Vector(1, 0, 0), Vector(0, 1, 0), math.pi/2).to_str())
	print(rotate(Vector(1, 0, 0), Vector(1, 1, 0), math.pi).to_str())
	print(rotate(Vector(1, 0, 0), Vector(0, 0, 1), math.pi/2).to_str())


	#--------------------------------------------------------------------------------------------------------------------------
