import pl
import numpy as np

def main():
	"""
	Code utilisé dans la question 2.1
	"""
	n = 3
	p = 6
	U = np.array([[325,225,210,115,75,50],\
				  [325,225,210,115,75,50],\
				  [325,225,210,115,75,50]])
	w1 = [3,2,1]
	w2 = [10,3,1]
	
	o1, a1, _ = pl.solve_partage_eq(n,p,U,w1)
	print("Pour w=(3,2,1) on a : f(x)=",o1,"\nEt l'affectation :\n",a1)
	o2, a2, _ = pl.solve_partage_eq(n,p,U,w2)
	print("\nPour w=(10,3,1) on a : f(x)=",o2,"\nEt l'affectation :\n",a2)
	o3, a3, _ = pl.solve_partage_ut(n,p,U)
	print("\nPour la maximisation de la moyenne on a : f(x)=",o3,"\nEt l'affectation :\n",a3)

	return 0

if __name__ == '__main__':
	main()