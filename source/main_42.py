import pl
import numpy as np

def main():
	"""
	Code utilisé dans la question 4.2
	"""
	n = 2
	w = (2,1)
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

	l, c ,_ = pl.solve_prc_rob(G,n,'a','g',w)

	print("Le chemin robuste renvoyé est",c,"et a pour coût",l)

	return 0

if __name__ == '__main__':
	main()