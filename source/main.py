import gurobipy as gp

def main():
	exemple = gp.Model("Exemple 1")
	r1 = exemple.addVar(vtype=C,name="r1")
	return 0

if __name__ == '__main__':
	main()