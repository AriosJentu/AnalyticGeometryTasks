import random
s = "\\item \\( \\displaystyle \\va = \\bracs{{{}, {}, {}}}, ~ \\vb = \\bracs{{{}, {}, {}}} \\);"

def f(n):
	p = [random.randint(-10, 10) for i in range(2*n)]
	chs = [chr(65+random.randint(0, 25)) for i in range(2)]
	q = [chs[i//(n+1)] if i%(n+1) == 0 else p[i-((i+n+1)//(n+1))] for i in range(2*n+2)]
	return s.format(*q)

def g(n):
	p = [random.randint(-10, 10) for i in range(n)]
	return s.format(*p)

for i in range(20):
	print(g(6))