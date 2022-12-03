import numpy as np
import gurobipy as gp
from gurobipy import GRB
import time

def solve_partage_eq(n,p,U=None,w=None):
	"""
	Résout le partage équitable au sens de la pondération w entre n individus de p objets
	dont les utilités pour chaque individus sont dans la matrice U de taille n*p
	Renvoie la valeur à l'optimum, l'affectation et le temps de résolution
	"""
	if U is None:
		U = np.random.randint(n*p*10,size=(n,p))
	if w==None:
		w = np.flip(np.sort(np.random.choice(np.arange(1,p),size=n,replace=False)))

	wp = [w[i]-w[i+1] for i in range(n-1)] + [w[n-1]]

	m = gp.Model()
	m.Params.outPutFlag = 0

	b = m.addMVar((n,n),vtype=GRB.CONTINUOUS,name="b")
	r = m.addMVar((n,),lb=-1*GRB.INFINITY,vtype=GRB.CONTINUOUS,name="r")
	x = m.addMVar((n,p),vtype=GRB.BINARY,name="r")
	
	o = m.setObjective(gp.quicksum([wp[k]*((k+1)*r[k]-gp.quicksum([b[i,k] for i in range(n)])) for k in range(n)]),GRB.MAXIMIZE)

	c1 = m.addConstrs((r[k]-b[i,k] <= gp.quicksum([U[i,j]*x[i,j] for j in range(p)]) for i in range(n) for k in range(n)),name='cb1')
	c2 = m.addConstrs((gp.quicksum(x[:,j]) == 1 for j in range(p)),name='cb2')

	start = time.time()
	m.optimize()
	end = time.time()
	
	return m.ObjVal, np.array(x.X), end-start

def solve_partage_ut(n,p,U=None):
	"""
	Résout le partage entre n individus de p objets en maximisant la moyenne des utilités de la matrice U
	Renvoie la valeur à l'optimum, l'affectation et le temps de résolution
	"""
	if U is None:
		U = np.random.randint(n*p*10,size=(n,p))

	m = gp.Model()
	m.Params.outPutFlag = 0

	x = m.addMVar((n,p),vtype=GRB.BINARY,name="r")
	
	o = m.setObjective(gp.quicksum([gp.quicksum([U[i,j]*x[i,j] for j in range(p)]) for i in range(n)])/n,GRB.MAXIMIZE)

	c = m.addConstrs((gp.quicksum(x[:,j]) == 1 for j in range(p)),name='c')

	start = time.time()
	m.optimize()
	end = time.time()
	
	return m.ObjVal, np.array(x.X), end-start