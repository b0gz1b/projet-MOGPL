import numpy as np
import gurobipy as gp
from gurobipy import GRB
import time

def solve_partage_eq(n,p,U,w,time_limit=None):
	"""
	Résout le partage équitable au sens de la pondération w entre n individus de p objets
	dont les utilités pour chaque individus sont dans la matrice U de taille n*p
	Renvoie la valeur à l'optimum, l'affectation et le temps de résolution
	"""

	wp = [w[i]-w[i+1] for i in range(n-1)] + [w[n-1]]
	m = gp.Model()
	# m.Params.outPutFlag = 0
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

def solve_partage_ut(n,p,U,time_limit=None):
	"""
	Résout le partage entre n individus de p objets en maximisant la moyenne des utilités de la matrice U
	Renvoie la valeur à l'optimum, l'affectation et le temps de résolution
	"""

	m = gp.Model()
	m.Params.outPutFlag = 0
	if not time_limit is None:
		m.Params.timeLimit = time_limit

	x = m.addMVar((n,p),vtype=GRB.BINARY,name="x")
	
	o = m.setObjective(gp.quicksum([gp.quicksum([U[i,j]*x[i,j] for j in range(p)]) for i in range(n)])/n,GRB.MAXIMIZE)

	c = m.addConstrs((gp.quicksum(x[:,j]) == 1 for j in range(p)),name='c')

	m.update()
	m.optimize()
	t = m.Runtime
	
	return m.ObjVal, np.array(x.X), t

def solve_selection_eq(n,p,c,U,w,time_limit=None):
	"""
	
	"""

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

def solve_selection_ut(n,p,c,U,time_limit=None):
	"""
	
	"""

	m = gp.Model()
	m.Params.outPutFlag = 0
	if not time_limit is None:
		m.Params.timeLimit = time_limit

	x = m.addMVar((p,),vtype=GRB.BINARY,name="x")
	
	o = m.setObjective(gp.quicksum([gp.quicksum([U[i,j]*x[j] for j in range(p)]) for i in range(n)])/n,GRB.MAXIMIZE)

	c = m.addConstr(gp.quicksum([x[i]*c[i] for i in range(p)]) <= 0.5*np.sum(c),name='cb2')

	m.update()
	m.optimize()
	t = m.Runtime
	
	return m.ObjVal, np.array(x.X), t

def solve_prc(G,s,a,g,time_limit=None):
	"""
	G représente le graphe par un liste d'adjacence sous forme de dictionnaire 
	qui pour chaque sommet référence la dicitionnaire des voisins et la valuation
	de l'arc dans les différents scénarios
	"""
	m = gp.Model()
	m.Params.outPutFlag = 0
	if not time_limit is None:
		m.Params.timeLimit = time_limit
	m.modelSense = GRB.MINIMIZE

	x = {}

	for u, dv in G.items():
		for v,S in dv.items():
			x[(u,v)] = m.addVar(obj=S[s],name='('+str(u)+','+str(v)+')')

	ds = m.addConstr(gp.quicksum([x[(a,v)] for v in G[a].keys()])-gp.quicksum([x[(v,a)] for v,lv in G.items() if a in lv.keys()]) == 1,name="degre_source")
	dp = m.addConstr(gp.quicksum([x[(g,v)] for v in G[g].keys()])-gp.quicksum([x[(v,g)]  for v,lv in G.items() if g in lv.keys()]) == -1,name="degre_puits")
	dg = m.addConstrs((gp.quicksum([x[(u,v)] for v in G[u].keys()])-gp.quicksum([x[(v,u)] for v,lv in G.items() if u in lv.keys()]) == 0 for u in G.keys() if u != a and u != g),name="degres_arcs")

	m.update()
	m.optimize()
	t = m.Runtime

	return m.ObjVal, [uv for (uv,xuv) in x.items() if xuv.X>0], t

def solve_prc_rob(G,n,a,g,w,time_limit=None):
	"""
	G représente le graphe par un liste d'adjacence sous forme de dictionnaire 
	qui pour chaque sommet référence la dicitionnaire des voisins et la valuation
	de l'arc dans les différents scénarios
	"""

	wp = [w[i]-w[i+1] for i in range(n-1)] + [w[n-1]]

	m = gp.Model()
	m.Params.outPutFlag = 0
	if not time_limit is None:
		m.Params.timeLimit = time_limit

	x = {}

	for u, dv in G.items():
		for v,S in dv.items():
			x[(u,v)] = m.addVar(vtype=GRB.BINARY,name='('+str(u)+','+str(v)+')')

	b = m.addMVar((n,n),vtype=GRB.CONTINUOUS,name="b")
	r = m.addMVar((n,),lb=-1*GRB.INFINITY,vtype=GRB.CONTINUOUS,name="r")

	o = m.setObjective(gp.quicksum([wp[k]*((k+1)*r[k]-gp.quicksum([b[i,k] for i in range(n)])) for k in range(n)]),GRB.MAXIMIZE)

	c1 = m.addConstrs((r[k]-b[i,k] <= -gp.quicksum([xuv*G[u][v][i] for ((u,v),xuv) in x.items()]) for i in range(n) for k in range(n)),name='cb1')

	ds = m.addConstr(gp.quicksum([x[(a,v)] for v in G[a].keys()])-gp.quicksum([x[(v,a)] for v,lv in G.items() if a in lv.keys()]) == 1,name="degre_source")
	dp = m.addConstr(gp.quicksum([x[(g,v)] for v in G[g].keys()])-gp.quicksum([x[(v,g)]  for v,lv in G.items() if g in lv.keys()]) == -1,name="degre_puits")
	dg = m.addConstrs((gp.quicksum([x[(u,v)] for v in G[u].keys()])-gp.quicksum([x[(v,u)] for v,lv in G.items() if u in lv.keys()]) == 0 for u in G.keys() if u != a and u != g),name="degres_arcs")

	m.update()
	m.optimize()
	t = m.Runtime
	
	return m.ObjVal, [uv for (uv,xuv) in x.items() if xuv.X>0], t