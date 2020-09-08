from algorithms import *
import math
import argparse
from llist import dllist, dllistnode


def main():
	
	#flags = {'-c': 65536, '-b': 64, '-n': 1, '-r': 'LRU', '-a': 'mxm_block', '-d': 480, '-p': 1, '-f': 32}


	parser = argparse.ArgumentParser(description='A cache simulator')
	parser.add_argument("-c", default=65536, help="Cache size")
	parser.add_argument("-b", default=64, help="Block size")
	parser.add_argument("-n", default=2, help="Set Associativity")
	parser.add_argument("-r", default='LRU', help="Replacement Policy")
	parser.add_argument("-a", default='mxm_block', help="algorithm simulated")
	parser.add_argument("-d", default=480, help="Dimension of matrix or vector size")
	parser.add_argument("-p", action='store_true', help="Print")
	parser.add_argument("-f", default=32, help="blocking factor")

	args = parser.parse_args()
	cache_size = int(args.c)
	block_size = int(args.b)
	associativity = int(args.n)
	policy = args.r
	alg = args.a
	dimension = int(args.d)
	p = int(args.p)
	factor = int(args.f)

	print(args)

	if(alg == 'mxm'):
		#mxm
		matrix_multiply(cache_size, block_size, associativity, policy, dimension, p)
	elif(alg == 'daxpy'):
		daxpy(cache_size, block_size, associativity, policy, dimension, p)
	else:
		matrix_multiply_blocking(cache_size, block_size, associativity, policy, dimension, factor, p)




main()