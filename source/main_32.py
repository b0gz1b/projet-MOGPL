import pl
import numpy as np
from uuid import uuid4

def main():
	try:
		with open("tmp/temps_resolution_ex3_"+str(uuid4())+".dat","w") as f:
			for n in [2,5,10,100]:
				for p in [5,10,15,20]:
					mesures = []
					for i in range(10):
						tl = 500
						fail = 0
						t = pl.solve_selection_eq(n,p,time_limit=tl)[2]
						while t >= tl:
							fail += 1
							print("Time limit exceeded -> nouvelle mesure")
							t = pl.solve_selection_eq(n,p,time_limit=tl)[2]
						mesures.append(t)
						print(n,p,str(i+1)+"/10",mesures[-1])
					
					f.write(str(n)+" "+str(p)+" "+str(np.mean(mesures))+" "+str(fail)+'\n')
	except IOError as err:
	    print(err.errno)
	    print(err.strerror)
	    return 1

	return 0

if __name__ == '__main__':
	main()