import random

class Number:

	EXPRESSIONS = [
		"\\frac{{#C#w_1 + #D#w_2}}{{w_3}}",
		"\\frac{{#C#w_1 - #D#w_2}}{{w_3}}",
		"\\frac{{#C#w_1 \\cdot w_2}}{{w_3}}",
		"#C#w_1 \\cdot w_2 + #D#w_3",
		"#C#w_1 \\cdot w_2 - #D#w_3",
		"#C#w_1 \\cdot w_2 \\cdot w_3",
	]

	def __init__(self, a=0, b=0, c=0, d=0):
		self.a = a
		self.b = b
		self.c = c
		self.d = d

	@staticmethod
	def generate_random_number():
		random.seed()

		a = random.randint(-3, 3)
		b = random.randint(-3, 3)
		c = random.randint(-3, 3)
		d = random.randint(-3, 3)

		return Number(a, b, c, d)

	def to_str(self):
		res = ""

		if self.a != 0:
			res += str(self.a)

		if self.b != 0:
			if self.b > 0 and len(res) > 0:
				res += "+"

			b = str(self.b) if abs(self.b) != 1 else str(self.b)[:-1]
			res += b+"i"

		if self.c != 0:
			if self.c > 0 and len(res) > 0:
				res += "+"

			c = str(self.c) if abs(self.c) != 1 else str(self.c)[:-1]
			res += c+"j"

		if self.d != 0:
			if self.d > 0 and len(res) > 0:
				res += "+"

			d = str(self.d) if abs(self.d) != 1 else str(self.d)[:-1]
			res += d+"k"

		return res

	@staticmethod
	def generate_expression():

		expr = random.choice(Number.EXPRESSIONS)
		expr = expr.replace("#C#", str(random.randint(2, 6)))
		expr = expr.replace("#D#", str(random.randint(2, 6)))

		return "w = "+expr