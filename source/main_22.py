import pl
import numpy as np
from uuid import uuid4

def main():
	try:
		with open("output/temps_resolution_ex2_"+str(uuid4())+".dat","w") as f:
			for n in range(5,21,5):
				f.write(str(n)+" "+str(np.mean([pl.solve_partage_eq(n,5*n)[2] for _ in range(10)]))+'\n')
	except IOError as err:
	    print(err.errno)
	    print(err.strerror)
	    return 1

	return 0

if __name__ == '__main__':
	main()