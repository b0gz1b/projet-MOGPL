import numpy as np
import gurobipy as gp
from gurobipy import GRB
import time

def solve_partage_eq(n,p,U=None,w=None,time_limit=None):
	"""
	Résout le partage équitable au sens de la pondération w entre n individus de p objets
	dont les utilités pour chaque individus sont dans la matrice U de taille n*p
	Renvoie la valeur à l'optimum, l'affectation et le temps de résolution
	"""
	if U is None:
		U = np.random.randint(10,size=(n,p))
	if w==None:
		w = np.flip(np.sort(np.random.choice(np.arange(1,n*10),size=n,replace=False)))

	wp = [w[i]-w[i+1] for i in range(n-1)] + [w[n-1]]
	m = gp.Model()
	m.Params.outPutFlag = 0
	if not time_limit is None:
		m.Params.timeLimit = time_limit

	b = m.addMVar((n,n),vtype=GRB.CONTINUOUS,name="b")
	r = m.addMVar((n,),lb=-1*GRB.INFINITY,vtype=GRB.CONTINUOUS,name="r")
	x = m.addMVar((n,p),vtype=GRB.BINARY,name="x")
	
	o = m.setObjective(gp.quicksum([wp[k]*((k+1)*r[k]-gp.quicksum([b[i,k] for i in range(n)])) for k in range(n)]),GRB.MAXIMIZE)

	c1 = m.addConstrs((r[k]-b[i,k] <= gp.quicksum([U[i,j]*x[i,j] for j in range(p)]) for i in range(n) for k in range(n)),name='cb1')
	c2 = m.addConstrs((gp.quicksum(x[:,j]) == 1 for j in range(p)),name='cb2')

	m.update()
	m.optimize()
	t = m.Runtime
	
	return m.ObjVal, np.array(x.X), t

def solve_partage_ut(n,p,U=None):
	"""
	Résout le partage entre n individus de p objets en maximisant la moyenne des utilités de la matrice U
	Renvoie la valeur à l'optimum, l'affectation et le temps de résolution
	"""
	if U is None:
		U = np.random.randint(n*p*10,size=(n,p))

	m = gp.Model()
	m.Params.outPutFlag = 0

	x = m.addMVar((n,p),vtype=GRB.BINARY,name="x")
	
	o = m.setObjective(gp.quicksum([gp.quicksum([U[i,j]*x[i,j] for j in range(p)]) for i in range(n)])/n,GRB.MAXIMIZE)

	c = m.addConstrs((gp.quicksum(x[:,j]) == 1 for j in range(p)),name='c')

	m.update()
	m.optimize()
	t = m.Runtime
	
	return m.ObjVal, np.array(x.X), t

def solve_selection_eq(n,p,c=None,U=None,w=None,time_limit=None):
	"""
	
	"""
	if U is None:
		U = np.random.randint(10,size=(n,p))
	if w is None:
		w = np.flip(np.sort(np.random.choice(np.arange(1,n*10),size=n,replace=False)))
	if c is None:
		c = np.random.randint(500,size=p)

	wp = [w[i]-w[i+1] for i in range(n-1)] + [w[n-1]]

	m = gp.Model()
	m.Params.outPutFlag = 0
	if not time_limit is None:
		m.Params.timeLimit = time_limit

	b = m.addMVar((n,n),vtype=GRB.CONTINUOUS,name="b")
	r = m.addMVar((n,),lb=-1*GRB.INFINITY,vtype=GRB.CONTINUOUS,name="r")
	x = m.addMVar((p,),vtype=GRB.BINARY,name="x")
	
	o = m.setObjective(gp.quicksum([wp[k]*((k+1)*r[k]-gp.quicksum([b[i,k] for i in range(n)])) for k in range(n)]),GRB.MAXIMIZE)

	c1 = m.addConstrs((r[k]-b[i,k] <= gp.quicksum([U[i,j]*x[j] for j in range(p)]) for i in range(n) for k in range(n)),name='cb1')
	c2 = m.addConstr(gp.quicksum([x[i]*c[i] for i in range(p)]) <= 0.5*np.sum(c),name='cb2')

	m.update()
	m.optimize()
	t = m.Runtime
	
	return m.ObjVal, np.array(x.X), t

def solve_selection_ut(n,p,c=None,U=None):
	"""
	
	"""
	if U is None:
		U = np.random.randint(n*p*10,size=(n,p))
	if c is None:
		c = np.random.randint(500,size=p)

	m = gp.Model()
	m.Params.outPutFlag = 0

	x = m.addMVar((p,),vtype=GRB.BINARY,name="x")
	
	o = m.setObjective(gp.quicksum([gp.quicksum([U[i,j]*x[j] for j in range(p)]) for i in range(n)])/n,GRB.MAXIMIZE)

	c = m.addConstr(gp.quicksum([x[i]*c[i] for i in range(p)]) <= 0.5*np.sum(c),name='cb2')

	m.update()
	m.optimize()
	t = m.Runtime
	
	return m.ObjVal, np.array(x.X), t