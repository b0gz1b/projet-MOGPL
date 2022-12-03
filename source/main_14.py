import gurobipy as gp
from gurobipy import GRB

def main():
	ex1 = gp.Model("Exemple 1")
	ex1.Params.outPutFlag = 0
	b = ex1.addVars(4,vtype=GRB.CONTINUOUS,name="b")
	r = ex1.addVars(2,lb=-1*GRB.INFINITY,vtype=GRB.CONTINUOUS,name="r")
	x = ex1.addVars(5,vtype=GRB.BINARY,name="r")
	
	o = ex1.setObjective(r[0]+2*r[1]-gp.quicksum(b),GRB.MAXIMIZE)

	c1 = ex1.addConstrs((r[0] - b[i] <= 5*x[0]+6*x[1]+4*x[2]+8*x[3]+x[4] for i in range(2)),name='c1')
	c2 = ex1.addConstrs((r[1] - b[i+2] <= 3*x[0]+8*x[1]+6*x[2]+2*x[3]+5*x[4] for i in range(2)),name='c2')
	c3 = ex1.addConstr((x[0]+x[1]+x[2]+x[3]+x[4] == 3),name='c3')

	ex1.optimize()
	print(x)
	print(ex1.ObjVal)
	return 0

if __name__ == '__main__':
	main()