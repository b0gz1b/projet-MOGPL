import gurobipy as gp
from gurobipy import GRB

def main():
	"""
	Code utilisé dans la question 1.2
	"""
	L = [4,7,1,3,9,2]
	Lk = []
	for k in range(1,len(L)+1):
		Ds = gp.Model("Dual "+str(k))
		Ds.Params.outPutFlag = 0
		Ds.modelSense=GRB.MAXIMIZE
		b = Ds.addVars(len(L),obj=-1,vtype=GRB.CONTINUOUS,name="b")
		r = Ds.addVar(obj=k,lb=-1*GRB.INFINITY,vtype=GRB.CONTINUOUS,name="r")
		c = Ds.addConstrs((r - b[i] <= L[i] for i in range(len(L))),name='c')
		Ds.optimize()
		Lk.append(Ds.ObjVal)
	print(Lk)
	return 0

if __name__ == '__main__':
	main()