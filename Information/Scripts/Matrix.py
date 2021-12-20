from random import randint, choice
import numpy

class Stack:

	def __init__(self, size: int = 3):
		self.array = []
		self.size = size

	def append(self, value):
		self.array.append(value)
		s = len(self.array)
		if s > self.size:
			self.array = self.array[s-self.size:]

	def __iter__(self):
		for i in self.array:
			yield i

class Vector:

	def __init__(self, size: int = 2):
		self.vector = [0 for i in range(size)]
		self.size = size

	@staticmethod
	def from_list(lst: list) -> "Vector":
		vec = Vector(len(lst))
		vec.vector = lst
		return vec

	def __check_size__(self, vector: "Vector") -> bool:
		return (
				isinstance(vector, Vector)
			and	self.size == vector.size
		)

	def count(self, value) -> int:
		return self.vector.count(value)

	def set_size(self, size: int = 2):
		if size < 0:
			return

		self.vector = [ 
			self.vector[i] 
			if i < self.size else 0 
			for i in range(size) 
		]
		self.size = size

	def get_size(self) -> int:
		return self.size

	def add(self, vector: "Vector") -> "Vector":
		if not self.__check_size__(vector):
			return

		newvector = Vector(self.size)
		newvector.vector = [
			self.vector[i] + vector.vector[i] 
			for i in range(self.size)
		]

		return newvector

	def scale(self, factor: float = 1) -> "Vector":
		return Vector.from_list([i*factor for i in self.vector])

	def dot_product(self, vector: "Vector") -> float:
		if not self.__check_size__(vector):
			return

		sums = 0
		for index, value in enumerate(self.vector):
			sums += value * vector[index]

		return sums

	def to_list(self):
		return self.vector

	def to_latex(self) -> str:
		return """\\begin{{pmatrix}}
			{vector}
		\\end{{pmatrix}}""".format(
			vector = ' \\\\\n\t\t\t'.join([
				self.value_to_latex(i) for i in self.vector
			])
		)

	def to_latex_floats(self) -> str:
		return """\\begin{{pmatrix}}
			{vector}
		\\end{{pmatrix}}""".format(
			vector = ' \\\\\n\t\t\t'.join([
				self.value_to_latex(i, True) for i in self.vector
			])
		)

	def distance(self) -> float:
		return sum([v*v for v in self.vector])**(1/2)

	def maxabs(self) -> [(float, complex, int), int]:
		res_index, res_value = -1, 0
		for index, value in enumerate(self.vector):
			if abs(value) > res_value:
				res_index = index
				res_value = abs(value)

		return res_value, res_index 

	def value_to_latex(self, value: (int, float, str), replaces: bool = False):
		res = str(value)
		if res.find("e") >= 0 and replaces:
			res = res.replace("e", " \\cdot 10^{")
			res += "}"

		return res


	def __getitem__(self, item: int) -> float:
		if isinstance(item, slice):
			return Vector.from_list(self.vector[item])

		return self.vector[item]

	def __setitem__(self, item: int, value: float):
		self.vector[item] = value

	def __add__(self, vector: "Vector") -> "Vector":
		return self.add(vector)

	def __radd__(self, vector: "Vector") -> "Vector":
		return self.__add__(vector)

	def __mul__(self, element: (float, "Vector")) -> (float, "Vector"):
		if isinstance(element, (float, int, complex)):
			return self.scale(element)

		elif isinstance(element, Vector):
			return self.dot_product(element)

	def __rmul__(self, element: (float, "Vector")) -> (float, "Vector"):
		return self.__mul__(element)

	def __len__(self):
		return len(self.vector)

	def __iter__(self):
		for element in self.vector:
			yield element

	def __str__(self):
		return f"""Vector[{self.size}]({
			', '.join([str(i) for i in self.vector])
		})"""

	def __repr__(self) -> str:
		return f"V{self.size}({', '.join([str(i) for i in self.vector])})"

class Matrix:

	def __init__(self, rows: int = 2, columns: int = 2):
		self.rows = rows
		self.columns = columns

		self.matrix = [
			Vector(columns)
			for _ in range(rows)
		]

	@staticmethod
	def from_list_of_vectors(lst: list[Vector]) -> "Matrix":
		matrix = Matrix(len(lst), len(lst[0]))
		for index, vector in enumerate(lst):
			matrix[index] = vector

		return matrix

	@staticmethod
	def from_vector(vec: Vector, vertical: bool = True) -> "Matrix":

		if vertical:
			matrix = Matrix(len(vec), 1)
			for index, value in enumerate(vec):
				matrix[index][0] = value
		else:
			matrix = Matrix(1, len(vec))
			matrix[0] = vec

		return matrix

	@staticmethod
	def from_list_of_lists(lst: list[list]) -> "Matrix":
		matrix = Matrix(len(lst), len(lst[0]))
		for index, element in enumerate(lst):
			matrix[index] = Vector.from_list(element)

		return matrix

	@staticmethod
	def generate_diagonal_matrix(
			value: float = 1, rows: int = 2, columns: int = None
	) -> "Matrix":
		if not columns:
			columns = rows

		matrix = Matrix(rows, columns)
		for i in range(min(rows, columns)):
			matrix[i][i] = value

		return matrix

	@staticmethod
	def generate_matrix_with_eigenvalues(
		values: list["Root"] = None, 
		linear_dependency: dict["Root", int] = None,
		direction: dict["Root", int] = None,
		with_complex: bool = False
	):
		if not linear_dependency:
			linear_dependency = {}

		if not direction:
			direction = {}

		values = sorted(values)
		size = len(values)
		matrix = Matrix(size, size)

		for i in range(size):
			root = values[i]
			prevroot = values[(i-1)%size]
			nextroot = values[(i+1)%size]
			matrix[i][i] = root

			if not with_complex:
				if hasattr(root, "imag") and root.imag != 0:
					realp = root.real
					complexp = root.imag

					if realp == int(realp):
						realp = int(realp)
					if complexp == int(complexp):
						complexp = int(complexp)

					if (
								hasattr(prevroot, "imag") 
							and root == prevroot.conjugate()
					):
						matrix[i][i] = realp
						matrix[i-1][i] = complexp
					elif (
								hasattr(nextroot, "imag") 
							and root == nextroot.conjugate()
					):
						matrix[i][i] = realp
						matrix[i+1][i] = complexp


			if (
					linear_dependency.get(root) != None 
				and	linear_dependency[root] > 0 
				and	nextroot == root
			):
				if (
						direction.get(root) != None 
					and	direction[root] < 0 
				):
					matrix[i+1][i] = 1
				else:
					matrix[i][i+1] = 1
	
				linear_dependency[root] -= 1

		return matrix

	@staticmethod
	def generate_random_detn_matrix(
			size: int = 2, 
			determinant: int = 1,
			min_iters: int = None,
			max_iters: int = None,
			max_multiplicator: int = 2,
			no_zeros: bool = False,
			max_steps: int = 50,
			minimize: bool = False,
	):

		if size <= 0:
			size = 2

		if not min_iters:
			min_iters = size

		if not max_iters:
			max_iters = 2*min_iters

		if min_iters > max_iters:
			min_iters, max_iters = max_iters, min_iters

		all_multiplicators = [
			i 
			for i in range(-max_multiplicator, max_multiplicator+1) 
			if i != 0
		]

		identity = Matrix.generate_diagonal_matrix(1, size)
		rows = list(range(size))

		firstrow = choice(rows)
		identity[firstrow] = identity[firstrow]*determinant

		cached_row = -1
		cached_values = Stack(max_multiplicator+1)

		#Basic preparing with sizes
		for row_from in range(size):
			for row_to in range(size):
				if row_from != row_to and row_to != cached_row:
					if randint(0, 1):
						identity.make_random_multiplier_row_addition(
							row_from, row_to, cached_values, 
							all_multiplicators, minimize
						)
					else:
						identity.swap_rows(row_from, row_to)

			cached_row = row_from

		#Making operations randomly
		if no_zeros:
			step = 0
			while identity.zeros_count() > 0 and step < max_steps:
				identity.make_random_operations(
					1, rows, cached_row, cached_values, 
					all_multiplicators, minimize
				)
				step += 1
		else:
			iters = randint(min_iters, max_iters)
			identity.make_random_operations(
				iters, rows, cached_row, cached_values, 
				all_multiplicators, minimize
			)

		return identity

	def get_minimal_distance_vector_row_index(self, 
			nonzero_col: int = -1,
			skip_row: int = -1
	) -> int:
		minlen, minrow = 2*self.maxabs()[0], 0
		
		for row, vector in enumerate(self.matrix):
			if row == skip_row:
				continue

			possible_len = vector.distance()
			if minlen > possible_len:
				if nonzero_col < 0 or vector[nonzero_col] != 0:
					minlen = possible_len
					minrow = row

		return minrow

	@staticmethod
	def generate_random_det1_matrix(
			size: int = 2, 
			min_iters: int = None,
			max_iters: int = None,
			max_multiplicator: int = 2,
			no_zeros: bool = False,
			max_steps: int = 50,
			minimize: bool = False,
	):
		return Matrix.generate_random_detn_matrix(
			size, 1, min_iters, max_iters, 
			max_multiplicator, no_zeros, max_steps, minimize
		)

	@staticmethod
	def generate_random_permutation_matrix(
			size: int = 2, 
	):
		identity = Matrix.generate_diagonal_matrix(1, size)

		rows = list(range(size))
		for i in range(randint(1, size+1)):
			cached_row = identity.make_random_row_permutation(
				rows, cached_row
			)

		return identity

	def __check_size__(self, mtx: "Matrix") -> bool:
		return (
				isinstance(mtx, Matrix)
			and	self.rows == mtx.rows and self.columns == mtx.columns
		)

	def __check_size_multiplication__(self, mtx: "Matrix") -> bool:
		return (
				isinstance(mtx, Matrix)
			and	self.columns == mtx.rows
		)

	def is_square(self):
		return self.rows == self.columns

	def set_columns(self, columns: int = 2):

		self.matrix = [
			Vector.from_list([
				row[i] if i < self.columns else 0 
				for i in range(columns) 
			]) 
			for row in self.matrix
		]
		self.columns = columns

	def zeros_count(self) -> int:
		return sum([
			vector.count(0) for vector in self.matrix
		])

	def set_rows(self, rows: int = 2):

		self.matrix = [
			self.matrix[i] if i < self.rows else Vector(self.columns)
			for i in range(rows)
		]

	def get_columns(self) -> int:
		return self.columns

	def get_rows(self) -> int:
		return self.rows

	def get_size(self) -> (int, int):
		return self.rows, self.columns

	def transpose(self) -> "Matrix":
		mtx = Matrix(self.columns, self.rows)
		for row, vector in enumerate(self.matrix):
			for column, element in enumerate(vector):
				mtx[column][row] = element

		return mtx

	def add(self, mtx: "Matrix") -> "Matrix":
		if not self.__check_size__(mtx):
			return

		newmatrix = Matrix(self.rows, self.columns)
		for index, vector in enumerate(self.matrix):
			newmatrix[index] = vector + mtx[index]

		return newmatrix

	def scale(self, factor: float = 1) -> "Matrix":
		return Matrix.from_list_of_vectors([
			factor*vector
			for vector in self.matrix
		])

	def multiply(self, mtx: "Matrix") -> "Matrix":
		if not self.__check_size_multiplication__(mtx):
			return

		newmatrix = Matrix(self.rows, mtx.columns)

		for row, vector in enumerate(newmatrix):
			for column, _ in enumerate(vector):
				left = self.matrix[row]
				right = mtx.transpose()[column]
				newmatrix[row][column] = left*right

		return newmatrix

	def vector_multiply(self, vector: Vector, isleft: bool = False):
		vec = Matrix.from_vector(vector, not isleft)

		if isleft:
			res = vec.multiply(self)
		else:
			res = self.multiply(vec).transpose()

		return res[0]


	def determinant(self):
		if not self.is_square():
			return
	
		size = self.columns
		if size == 1:
			return self.matrix[0][0]

		result = 0
		for index in range(size):
			submatrix = Matrix.from_list_of_lists(
				[ 
					[
						self.matrix[row][column] 
						for column in range(size)
						if column != index
					] 
					for row in range(size) 
					if row != 0
				]
			)

			det2 = submatrix.determinant()
			result += (-1)**index * det2 * self.matrix[0][index]

		return result

	def row_addition(self, 
		from_row: int = 0, to_row: int = 1, multiplier: int = 1
	):
		if to_row == from_row:
			return

		self.matrix[to_row] += multiplier*self.matrix[from_row]

	def swap_rows(self, from_row: int = 0, to_row: int = 1):
		if from_row == to_row:
			return

		self.matrix[from_row], self.matrix[to_row] =\
			self.matrix[to_row], self.matrix[from_row]

	def inverse(self, 
			rounding: bool = True, 
			only_matrix: bool = False
	) -> ("Matrix", float):
		det = self.determinant()
		if det == 0 or not self.is_square():
			return

		invdet = 1/det
		if invdet == int(invdet):
			invdet = int(invdet)

		mtx = Matrix.from_list_of_lists([
			[
				float(col)
				for col in row
			]
			for row in numpy.linalg.inv(self.matrix)
		])

		for row, line in enumerate(mtx):
			for column, element in enumerate(line):
				val = element
				if rounding:
					val = round(element*det)

					if val == int(val):
						val = int(val)

				mtx[row][column] = val

		if only_matrix:
			return mtx

		return mtx, invdet

	def make_random_row_permutation(self, 
			rows: list[int], 
			cached_row: int = -1
	) -> int:

		row_from = choice([i for i in rows if i != cached_row])
		row_to = choice([i for i in rows if i != row_from])

		self.swap_rows(row_from, row_to)

		return row_from

	def make_random_multiplier_row_addition(self, 
			from_row: int, to_row: int,
			cached_values: Stack,
			all_multiplicators: list[int],
			minimize: bool = False
	) -> int:

		multiplicators = [
			i for i in all_multiplicators 
			if i not in cached_values
		]

		if minimize:
			vec1 = self.matrix[from_row]
			vec2 = self.matrix[to_row]

			mindist, multiplicator = vec1.distance() + vec2.distance(), 1
			for k in multiplicators:
				curdist = (vec1 + k*vec2).distance()
				if curdist < mindist:
					mindist, multiplicator = curdist, k
				# print("For", k, "it's", curdist)

			# print("Minimization on", multiplicator, "with dist", mindist)

		else:
			multiplicator = choice(multiplicators)

		self.row_addition(from_row, to_row, multiplicator)
		return multiplicator


	def make_random_row_addition(self, 
			rows: list[int],
			cached_row: int,
			cached_values: Stack, 
			all_multiplicators: list[int],
			minimize: bool = False
	) -> int:


		row_from = choice([i for i in rows if i != cached_row])
		row_to = choice([i for i in rows if i != row_from])

		multiplication = self.make_random_multiplier_row_addition(
			row_from, row_to, cached_values, all_multiplicators, minimize
		)
		cached_values.append(multiplication)

		return row_from

	def make_random_operations(self,
			iters: int,
			rows: list[int],
			cached_row: int,
			cached_values: Stack,
			all_multiplicators: list[int],
			minimize: bool = False
	) -> int:
		for _ in range(iters):
			if randint(0, 1):
				cached_row = self.make_random_row_addition(
					rows, cached_row, cached_values, 
					all_multiplicators, minimize
				)
			else:
				cached_row = self.make_random_row_permutation(
					rows, cached_row
				)

		return cached_row

	def to_latex(self, string: str = "") -> str:
		return """\\begin{{pmatrix}}
			{matrix}
			% {string}
		\\end{{pmatrix}}""".format(
			matrix = ' \\\\\n\t\t\t'.join(
				[" & ".join(
					[vector.value_to_latex(i) for i in vector]
				) for vector in self.matrix]
			),
			string = string
		)

	def norm(self):
		if self.is_square():
			
			x = Vector.from_list([
				1 + ((-i)**i)/self.rows for i in range(self.rows)
			])

			e = Vector.from_list([
				(-1)**i * 1/(10*self.rows) 
				for i in range(self.rows)
			])

			mtx_len = (self*x).distance()
			vec_len = x.distance()

			mtx_f_len = (self*e).distance()
			vec_f_len = e.distance()

			a = mtx_len/vec_len
			b = mtx_f_len/vec_f_len

			if b == 0:
				return 1e16

			return a/b

	def cond(self):
		a = self.norm()
		b = self.inverse(only_matrix=True).norm()
		return a*b

	def maxabs(self, 
			*except_rows: list[int]
	) -> [(float, complex, int), int, int]:
	
		res_y_pos, res_x_pos, res_value = -1, -1, 0
		for y_pos, vector in enumerate(self.matrix):
			if y_pos not in except_rows:
				value, x_pos = vector.maxabs()
				if abs(value) > res_value:
					res_y_pos = y_pos
					res_x_pos = x_pos
					res_value = abs(value)

		return res_value, res_y_pos, res_x_pos 

	@staticmethod
	def multiplication(
			leftoperand: (float, "Matrix", Vector), 
			rightoperand: (float, "Matrix", Vector)
	):
		if isinstance(leftoperand, (float, int, complex)):
			leftoperand, rightoperand = rightoperand, leftoperand

		if isinstance(rightoperand, (float, int, complex)):
			return leftoperand.scale(rightoperand)

		elif isinstance(rightoperand, Matrix):
			return leftoperand.multiply(rightoperand)

		if isinstance(leftoperand, Vector):
			return rightoperand.vector_multiply(leftoperand, True)

		if isinstance(rightoperand, Vector):
			return leftoperand.vector_multiply(rightoperand)

	def __add__(self, mtx: "Matrix") -> "Matrix":
		return self.add(mtx)

	def __radd__(self, mtx: "Matrix") -> "Matrix":
		return self.__add__(mtx)

	def __mul__(self, element: (float, "Matrix")) -> "Matrix":
		return Matrix.multiplication(self, element)

	def __rmul__(self, element: (float, "Matrix")) -> "Matrix":
		return Matrix.multiplication(element, self)

	def __getitem__(self, item: int) -> Vector:
		return self.matrix[item]

	def __setitem__(self, item: int, value: Vector):
		self.matrix[item] = value

	def __iter__(self):
		for vec in self.matrix:
			yield vec

	def __abs__(self):
		return self.determinant()

	def __len__(self):
		return self.norm()

	def __str__(self) -> str:
		return f"""Matrix{self.rows}x{self.columns}({
			'; '.join([
				str(i) for i in self.matrix
			])
		})"""

	def __repr__(self) -> str:
		return f"""M{self.rows}x{self.columns}[{
			', '.join([repr(i) for i in self.matrix])
		}]"""

if __name__ == "__main__":
	# vec = Vector(4)
	# vec[0] = 1
	# # print(vec, vec[0], [i for i in vec])
	# mtx = Matrix(2, 3)
	# mtx[0][1] = 3
	# mtx[0][2] = 2
	# mtx[1][1] = 1
	# mtx[1][2] = -1
	# mtx.set_columns(4)
	# print(mtx)
	# print(mtx.transpose())

	# for i, v in enumerate(mtx):
	# 	print(i, v)

	# mtx2 = Matrix.from_list_of_lists([[2, 3, 4], [1, 0, 0]])
	# mtx3 = Matrix.from_list_of_lists([[0, 1000], [1, 100], [0, 10]])
	# print(mtx2)
	# print(mtx3)
	# print(mtx2*mtx3)
	# print(mtx3*mtx2)
	# print()

	# mtx4 = Matrix.from_list_of_lists([[3, -7, 1, 4], [1, -4, 8, -8], [-4, 1, 2, -8], [3, -3, 7, 6]])
	# print(mtx4)
	# print(abs(mtx4))

	# mtx4.row_addition(1, 3, 1)
	# print(mtx4)
	# print(abs(mtx4))

	# mtx4.row_addition(3, 0, -2)
	# print(mtx4)
	# print(abs(mtx4))

	# mtx4.row_addition(2, 1, -1)
	# print(mtx4)
	# print(abs(mtx4))

	# mtx4.swap_rows(2, 1)
	# print(mtx4)
	# print(abs(mtx4))

	# print()
	# mtx5 = Matrix.generate_random_det1_matrix(4)
	# mtx5 = mtx5*3
	# print(abs(mtx5), mtx5) 

	# print(mtx5.inverse())
	# print(type(mtx5.inverse()[0][0]), type(mtx5.inverse()[0][0][0]))
	# print()

	mtx6 = Matrix.generate_random_det1_matrix(3, no_zeros=True, minimize=True)
	print(mtx6)
	print(mtx6.inverse())
	# print(mtx6.to_latex())
	# print(mtx6[0].to_latex())
	print()

	# eigenmatrix = Matrix.from_list_of_lists([
	# 	[1, 0, 0],
	# 	[0, 5, 0],
	# 	[0, 0, 4]
	# ])

	# mtx7 = Matrix.from_list_of_lists([
	# 	[85683, 342732, 114244], 
	# 	[342732, -114244, 85683], 
	# 	[114244, 85683, -342732]
	# ])

	# print(mtx7)
	# for vector in mtx7*eigenmatrix*mtx7.transpose():
	# 	print(vector)

	from math import sqrt
	
	# mtx8 = Matrix.from_list_of_lists([
	# 	[1/1 * sqrt(1/1), 0/1 * sqrt(1/1), 0/1 * sqrt(1/1)],
	# 	[0/1 * sqrt(1/1), 1/1 * sqrt(1/1), 0/1 * sqrt(1/1)],
	# 	[0/1 * sqrt(1/1), 0/1 * sqrt(1/1), 1/1 * sqrt(1/1)]
	# ])
	# print(mtx8)
	# print(mtx8*mtx8.transpose())

	s = Vector.from_list(["x", "y", "z"])
	print(s.to_latex())