import pl
import numpy as np

def main():
	"""
	Code utilisé dans la question 4.1
	"""
	G = {'a':{'b':[5,3],\
			  'c':[10,4],\
			  'd':[2,6]},\
		 'b':{'c':[4,2],\
			  'd':[1,3],\
			  'e':[4,6]},\
		 'c':{'e':[3,1],\
			  'f':[1,2]},\
		 'd':{'c':[1,4],\
			  'f':[3,5]},\
		 'e':{'g':[1,1]},\
		 'f':{'g':[1,1]},\
		 'g':{}}

	l1, c1 ,_ = pl.solve_prc(G,0,'a','g')
	l2, c2 ,_ = pl.solve_prc(G,1,'a','g')

	print("Dans le scénario 1, le chemin revoyé est",c1,"et a pour coût",l1)
	print("Dans le scénario 2, le chemin revoyé est",c2,"et a pour coût",l2)

	return 0

if __name__ == '__main__':
	main()