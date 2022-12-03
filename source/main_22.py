import pl
import numpy as np
from uuid import uuid4

def main():
	try:
		with open("tmp/temps_resolution_ex2_"+str(uuid4())+".dat","w") as f:
			for n in range(5,26,5):
				mesures = []
				for i in range(10):
					mesures.append(pl.solve_partage_eq(n,5*n)[2])
					print(n,str(i+1)+"/10",mesures[-1])
				
				f.write(str(n)+" "+str(np.mean(mesures))+'\n')
	except IOError as err:
	    print(err.errno)
	    print(err.strerror)
	    return 1

	return 0

if __name__ == '__main__':
	main()