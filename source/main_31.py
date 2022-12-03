import pl
import numpy as np

def main():
	n = 2
	p = 4
	c = [40,50,60,50]
	U = np.array([[19,6,17,2],\
				  [2,11,4,18]])
	w1 = [2,1]
	w2 = [10,1]
	
	o1, a1, _ = pl.solve_selection_eq(n,p,c,U,w1)
	print("Pour w=(2,1) on a : f(x)=",o1,"\nEt la sélection :\n",a1)
	o2, a2, _ = pl.solve_selection_eq(n,p,c,U,w2)
	print("\nPour w=(10,1) on a : f(x)=",o2,"\nEt la sélection :\n",a2)
	o3, a3, _ = pl.solve_selection_ut(n,p,c,U)
	print("\nPour la maximisation de la moyenne on a : f(x)=",o3,"\nEt la sélection :\n",a3)

	return 0

if __name__ == '__main__':
	main()