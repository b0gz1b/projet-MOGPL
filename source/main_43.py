import pl
import numpy as np
from uuid import uuid4
from matplotlib import pyplot as plt

def main():
	"""
	Code utilisé dans la question 4.3
	"""
	n = 2
	m = 12
	tl = 500
	ws = [w_alpha(i,n) for i in range(1,6)]
	
	mesures = np.zeros((len(ws),20,2))
	
	for i in range(20):
		t = np.random.randint(1,1501,size=(12,2))
		G = {'a':{'b':t[0],\
				  'c':t[1],\
				  'd':t[2]},\
			 'b':{'c':t[3],\
				  'd':t[4],\
				  'e':t[5]},\
			 'c':{'e':t[6],\
				  'f':t[7]},\
			 'd':{'c':t[8],\
				  'f':t[9]},\
			 'e':{'g':t[10]},\
			 'f':{'g':t[11]},\
			 'g':{}}
		for j in range(len(ws)):
			_,c,_ = pl.solve_prc_rob(G,n,'a','g',ws[j])
			mesures[j,i,0] = t_chemin_s(G,c,0)
			mesures[j,i,1] = t_chemin_s(G,c,1)

	lt = np.min(mesures)
	ut = np.max(mesures)

	idf = str(uuid4())

	for i in range(len(mesures)):
		plt.figure()
		plt.plot(*mesures[i].T,'o')
		plt.ylabel('$t^1$')
		plt.xlabel('$t^2$')
		evo = i
		while evo > 0:
			for j in range(len(mesures[evo])):
				if np.any(mesures[evo][j]!=mesures[evo-1][j]):
					plt.plot(*mesures[evo-1][j].T,marker='o',color='grey',alpha=np.exp(evo-i-0.3))
					plt.arrow(*mesures[evo-1][j].T,*(mesures[evo][j]-mesures[evo-1][j]).T,color='grey',alpha=np.exp(evo-i-0.3))
			evo -= 1
		plt.xlim((lt*0.85, ut*1.15))
		plt.ylim((lt*0.85, ut*1.15))
		plt.title("Durées sur 20 instances aléatoires pour w("+str(i+1)+")")
		plt.savefig('tmp/ex43_w_'+str(i+1)+'_'+idf+'.png')
	return 0

def w_alpha(alpha,n):
	return [((n-i+1)/n)**alpha-((n-i)/n)**alpha for i in range(1,n+1)]

def t_chemin_s(G,c,s):
	return np.sum([G[u][v][s] for u,v in c])


if __name__ == '__main__':
	main()