import random

class Coefficient:

	def __init__(self, value: (float, 'Coefficient') = 1):
		
		if isinstance(value, Coefficient):
			self._coefficient = value._coefficient
			self._sign = value._sign
		else:
			self._coefficient = abs(value)
			self._sign = ["-", "+"][abs(value) == value]

	@property
	def coeff(self):
		return self._coefficient
	
	def __get_sign_drawing__(self, with_sign: bool = False):
		sign = self._sign
		if not with_sign and self.is_positive():
			sign = ""

		return sign

	def to_str(self, with_sign: bool = False) -> str:
		sign = self.__get_sign_drawing__(with_sign)
		
		if self.coeff == 0:
			return ""

		return f"{sign}{self.coeff}"

	def to_float(self) -> float:
		return [-1, 1][self.is_positive()]*self.coeff

	def multiply(self, value: (float, 'Coefficient')) -> 'Coefficient':
		
		if isinstance(value, Coefficient):
			value = value.to_float()

		coefficient = self.to_float() * value
		return Coefficient(coefficient)

	def add(self, value: (float, 'Coefficient')) -> 'Coefficient':
		coeff = self.to_float()
		if isinstance(value, Coefficient):
			coeff += value.to_float()
		else:
			coeff += value

		return Coefficient(coeff)

	def int(self):
		self._coefficient = int(self.coeff)

	def is_positive(self):
		return self._sign == "+"

	def __add__(self, value: (float, 'Coefficient')) -> 'Coefficient':
		return self.add(value)

	def __radd__(self, value: (float, 'Coefficient')) -> 'Coefficient':
		return self.add(value)

	def __sub__(self, value: (float, 'Coefficient')) -> 'Coefficient':
		return self.add(value*(-1))

	def __rsub__(self, value: (float, 'Coefficient')) -> 'Coefficient':
		return (self*(-1)).add(value)

	def __mul__(self, value: (float, 'Coefficient')) -> 'Coefficient':
		return self.multiply(value)

	def __rmul__(self, value: (float, 'Coefficient')) -> 'Coefficient':
		return self.multiply(value)

	def __str__(self) -> str:
		return self.to_str()

	def __repr__(self) -> str:
		return self.__str__()+" "+str(self.__class__)

	def __eq__(self, coeff: 'Coefficient') -> bool:
		return isinstance(coeff, (Coefficient, float, int))

	def __ne__(self, coeff: 'Coefficient') -> bool:
		return not self.__eq__(coeff)

	def __round__(self, signs: int = 0) -> 'Coefficient':
		return Coefficient(round(self.coeff, signs))

class Variable(Coefficient):

	def __init__(self, variable: str = "x", coefficient: float = 1):
		super().__init__(coefficient)
		self._variable = variable

	@property
	def var(self):
		return self._variable

	def to_float(self, at_point: float = 1):
		return super().to_float()*at_point

	def to_str(self, with_sign: bool = False) -> str:
		if self.coeff == 0:
			return ""

		if self.coeff != 1:
			return f"{super().to_str(with_sign)}{self.var}"
		else:
			return f"{self.__get_sign_drawing__(with_sign)}{self.var}"

	def multiply(self, value: (float, 'Coefficient')) -> 'Variable':
		coeff = super().multiply(value)
		return Variable(self.var, coeff)

	def add(self, value: (float, 'Variable')) -> 'Variable':
		coeff = super().add(value)
		if self == value:
			return Variable(self.var, coeff)

	def __eq__(self, variable: 'Variable') -> bool:
		return (
					isinstance(variable, Variable) 
				and self.var == variable.var
		)

	def __round__(self, signs: int = 0) -> 'Variable':
		return Variable(self.var, round(self.coeff, signs))

class LinearExpression(Coefficient):

	def __init__(self, *elements: list[(Coefficient, Variable)]):
		if not elements:
			elements = []

		elements = list(elements)

		for i, element in enumerate(elements):
			if isinstance(element, (int, float)):
				elements[i] = Coefficient(element)

		self._elements = elements

	def add(self, 
			value: (float, Coefficient, Variable, 'LinearExpression')
	) -> 'LinearExpression':
		
		elements = self._elements[:]
		appended = []
		for index, element in enumerate(elements):

			if isinstance(value, LinearExpression):
				for expr_element in value:
					if expr_element == element:
						elements[index] = element + expr_element
						appended.append(expr_element)
						break

			elif value == element or (
						isinstance(value, (int, float)) 
					and isinstance(element, Coefficient)
					and not isinstance(element, Variable)
			):
				elements[index] = element + value
				break

		else:
			if (
						isinstance(value, (Coefficient, int, float)) 
					and not isinstance(value, (Variable, LinearExpression))
			):
				elements.append(Coefficient(value))
			
			if isinstance(value, Variable):
				elements.append(value)
			
			if isinstance(value, LinearExpression):
				for expr_element in value:
					for element in elements:
						if element == expr_element:
							continue
						if expr_element not in appended:
							elements.append(expr_element)
							appended.append(expr_element)

		return LinearExpression(*elements)

	def multiply(self, value: (float, Coefficient)) -> 'LinearExpression':
		elements = [element*value for element in self._elements]
		return LinearExpression(*elements)

	def shuffle(self):
		random.shuffle(self._elements)

	def get_common_multiplicator(self):

		coeffs = [
			abs(element.coeff) 
			for element in self._elements 
			if element.coeff != 0
		]

		minimal = min(coeffs)

		for divisor in range(minimal, 0, -1):
			isdivisible = [value//divisor == value/divisor for value in coeffs]
			if False not in isdivisible:
				return divisor

	def get_free_coefficient(self) -> Coefficient:
		for element in self._elements:
			if isinstance(element, Coefficient) and not isinstance(element, Variable):
				return element
		else:
			return Coefficient(0)

	def as_positive(self):
		if not self._elements[0].is_positive():
			self._elements = [i*(-1) for i in self._elements]

	def round(self, signs: int = 0):
		self._elements = [round(i, signs) for i in self._elements]

	def int(self):
		for element in self._elements:
			if element.coeff == int(element.coeff):
				element._coefficient = int(element.coeff)

	def to_str(self, with_sign: bool = False):
		elements = [element for element in self._elements if element.to_str() != ""]
		if len(elements) == 0:
			return "0"

		return "".join([
			element.to_str(i > 0) 
			for i, element in enumerate(elements)
		])

	def __iter__(self):
		for element in self._elements:
			yield element

	def __round__(self, signs: int = 0):
		self.round(signs)
		return self

def main(*args):
	coef1 = Coefficient(1)
	coef2 = Coefficient(5)
	# print((coef1-coef2)*(8))
	# print(coef2-coef1)
	# print(coef1*2 - coef2)
	# print(coef1*2 + coef2*(-1))
	# print(coef1*3 - coef2*2)
	# print(coef1*3 + coef2*(-2))
	# a = coef2*(-2)
	# b = coef1*3
	# print(a, b, a+b)
	# print(coef2*(-2) + coef1*3)
	# print(coef2*2 + coef1*3)

	var1 = Variable("x")
	var2 = Variable("x")
	var3 = Variable("y")
	print(var1*coef2)
	print(isinstance(var2, LinearExpression))

	linexp = LinearExpression()

	linexp = linexp+coef2
	linexp = linexp+var1*2
	linexp = linexp+coef1

	linexp2 = LinearExpression()
	linexp2 = linexp2 - var3*2
	linexp2 = linexp2 - coef2*3

	linexp3 = (linexp+linexp2)
	linexp3.shuffle()

	linexp4 = LinearExpression()
	linexp4 = linexp4 + 0

	print(linexp)
	print(linexp2)
	print(linexp3)
	print(linexp4)

if __name__ == "__main__":
	main()