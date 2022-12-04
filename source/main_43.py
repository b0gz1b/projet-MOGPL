import pl
import numpy as np
from uuid import uuid4
from matplotlib import pyplot as plt

def main():
	n = 2
	m = 12
	tl = 500
	ws = [w_alpha(i,n) for i in range(1,6)]
	
	mesures = np.zeros((len(ws),20,2))
	
	for i in range(20):
		t = np.random.randint(1,101,size=(12,2))
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
	plt.figure()
	for i in range(len(mesures)):
		plt.figure()
		plt.plot(*mesures[i].T,'o')
		plt.ylabel('$t^1$')
		plt.xlabel('$t^2$')
		plt.xlim((np.min(mesures[:,:,0])-3, np.max(mesures[:,:,0])+3))
		plt.ylim((np.min(mesures[:,:,1])-3, np.max(mesures[:,:,1])+3))
		plt.title("Durées sur 20 instances aléatoires pour w("+str(i+1)+")")
		plt.savefig('tmp/ex43_w_'+str(i+1)+'_'+str(uuid4())+'.png')
	return 0

def w_alpha(alpha,n):
	return [((n-i+1)/n)**alpha-((n-i)/n)**alpha for i in range(1,n+1)]

def t_chemin_s(G,c,s):
	return np.sum([G[u][v][s] for u,v in c])


if __name__ == '__main__':
	main()