import math

class Fraction:

	ACCURACY = 4

	def __init__(self, value: float, root: int = 0, prefered: int = -1):

		if root != 0 and int(root**(1/2)) == root**(1/2):
				value *= root**(1/2)
				root = 0

		self._value = value
		self._numerator = 0 
		self._denominator = 0
		self._root = root
		self._addon = ""

		self.extract(prefered)

	def set_numerator(self, value: str):
		self._numerator = value

	def set_denominator(self, value: str):
		self._denominator = value

	@classmethod
	def extract_denominator(cls, value) -> int:
		result =  1
		# print(
		# 	round(abs(value*result), 0),
		# 	round(abs(value*result), cls.ACCURACY),
		# 	value*result, result, value 
		# )
		while round(abs(value*result), 0) != round(abs(value*result), cls.ACCURACY):
			result += 1
			# print(
			# 	round(abs(value*result), 0),
			# 	round(abs(value*result), cls.ACCURACY),
			# 	value*result, result, value 
			# )

		# print("Found", result)

		return result

	def extract(self, prefered=-1):
		if self._value == int(self._value):
			self._numerator = int(self._value)
			self._denominator = 1
		else:
			extr_den = Fraction.extract_denominator(self._value)
			extr_pi = Fraction.extract_denominator(self._value/math.pi)
			extr_exp = Fraction.extract_denominator(self._value/math.e)

			denoms = [extr_den, extr_pi, extr_exp]
			denom = min(denoms)
			index = denoms.index(denom)
			if prefered >= 0 and prefered < len(denoms):
				denom = denoms[prefered]
				index = prefered


			val = [1, math.pi, math.e][index]
			self._addon = ["", " \\pi", " e"][index] 

			self._numerator = int(round(self._value*denom/val, 0))
			self._denominator = denom

	def get_sign(self) -> int:
		numer, denom = self._numerator, self._denominator
		if numer == 0 or denom == 0:
			return 1

		s1 = numer/abs(numer)
		s2 = denom/abs(denom)
		return s1*s2

	def to_str(self, reprs: bool = False) -> str:
		if self._denominator == 0 and self._numerator == 0:
			return "?"

		if self._numerator == 0:
			return "0"
	
		sign = ["-", ""][self.get_sign() == 1]
		if self._denominator == 0:
			return sign + "\\infty"

		if abs(self._denominator) == 1:
			return sign + str(abs(self._numerator))

		numer = str(abs(self._numerator))
		denom = str(abs(self._denominator))

		if self._root != 0:
			format1 = f" \\sqrt{{{self._root}}} "
			format2 = f"v{{{self._root}}}"

			div1 = self._denominator/self._root
			div2 = self._root/self._denominator
			
			if div1 == int(div1):
				div1 = int(div1)

				if self._numerator/div1 == self._numerator//div1:
					numer = f"{abs(self._numerator)//div1}"
					div1 = ""
			
				if div1 != "" and abs(div1) == 1:
					div1 = ""

				denom = f"{div1}{[format1, format2][int(reprs)]}"
			
			elif div2 == int(div2):
				val = self._numerator*int(div2)
				denom = [format1, format2][int(reprs)]
				numer = str(abs(val))
			
			else:
				if numer == "1":
					numer = ""
			
				numer += [format1, format2][int(reprs)] 
		
		if numer == "1" and self._addon != "":
			numer = ""
	
		numer += self._addon
		format1 = f"\\frac{{{numer}}}{{{denom}}}"
		format2 = f"{numer}/{denom}"

		return sign + [format1, format2][int(reprs)]

	def __str__(self):
		return self.to_str()

	def __repr__(self):
		return self.to_str(True)