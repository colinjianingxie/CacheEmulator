from cpu import *
import math

#FOR TESTING PURPOSES
def seq_matrix(m,n,iteration):
	result = [[0 for _ in range(n)] for _ in range(m)]
	#now, you can loop through it easily.
	for i in range(m): #outer list
		 for j in range(n): #inner list
			 result[i][j] = (i*n+j)*iteration #put it there :)
	return result
def zero_matrix(m,n):
	result = [[0 for _ in range(n)] for _ in range(m)]
	#now, you can loop through it easily.
	for i in range(m): #outer list
		 for j in range(n): #inner list
			 result[i][j] = 0 #put it there :)
	return result
def matmult(m1,m2):
	r=[]
	m=[]
	for i in range(len(m1)):
		for j in range(len(m2[0])):
			sums=0
			for k in range(len(m2)):
				sums=sums+(m1[i][k]*m2[k][j])
			r.append(sums)
		m.append(r)
		r=[]
	return m


####################



def daxpy_example():
	n = 9
	associativity = 1

	myCpu = CPU(cache_size=64*8, block_size=64, n_associativity=associativity, replacement_policy="FIFO", algorithm="daxpy", dimension=n, printing=0, blocking=8)

	
	a = list(range(0, n, 1))
	b = list(range(n, 2*n, 1))
	c = list(range(2*n, 3*n, 1))



	for i in range(n):
		myCpu.storeDouble(myCpu, a[i], i)
		myCpu.storeDouble(myCpu, b[i], 2*i)
		myCpu.storeDouble(myCpu, c[i], 0)
	
	d = 3
	for i in range(n):
		register1 = myCpu.loadDouble(a[i])
		#print(register1)
		register2 = myCpu.multDouble(d, register1)
		register3 = myCpu.loadDouble(b[i])
		register4 = myCpu.addDouble(register2, register3)
		myCpu.storeDouble(myCpu, c[i], register4)


	
	print("\n\n\n")
	myCpu.print_inputs()
	myCpu.print_results()
	print("\n\n\n")
	
	#myCpu.ram.print_ram()

	result = []
	for address in c:
		temp_register = myCpu.loadDouble(address)
		result.append(temp_register)
	print(result)


def matrix_multiply():
	n = 9
	associativity = 1

	myCpu = CPU(cache_size=64*8, block_size=64, n_associativity=associativity, replacement_policy="LRU", algorithm="mxm", dimension=n, printing=0, blocking=8)


	a = list(range(0, n*n, 1))
	b = list(range(n*n, 2*n*n, 1))
	c = list(range(2*n*n, 3*n*n, 1))



	for i in range(n*n):
		myCpu.storeDouble(myCpu, a[i], i)
		myCpu.storeDouble(myCpu, b[i], 2*i)
		myCpu.storeDouble(myCpu, c[i], 0)
	
	


   #base_addr + ith_row*len_row + col_num
	r = []
	m=[]
	for i in range(n):
		for j in range(n):
			register0=0
			for k in range(n):
				register1 = myCpu.loadDouble(a[i*n+k])
				register2 = myCpu.loadDouble(b[k*n+j])
				#print(register1)

				register3 = myCpu.multDouble(register1, register2)
				register0 = myCpu.addDouble(register0, register3)
			r.append(register0)
			myCpu.storeDouble(myCpu, c[i*n + j], register0)
		m.append(r)
		r=[]


	
	print("\n\n\n")
	myCpu.print_inputs()
	myCpu.print_results()
	print("\n\n\n")
	print(m)


# ALGORITHM RETRIEVED FROM https://stackoverflow.com/questions/40050761/python-matrix-multiplication-and-caching

def matrix_multiply_blocking(n, blocking_factor):

	n = 9
	associativity = 1

	myCpu = CPU(cache_size=64*8, block_size=64, n_associativity=associativity, replacement_policy="LRU", algorithm="mxm", dimension=n, printing=0, blocking=blocking_factor)



	#d = zero_matrix(n,n)

	a = list(range(0, n*n, 1))
	b = list(range(n*n, 2*n*n, 1))
	c = list(range(2*n*n, 3*n*n, 1))



	for i in range(n*n):
		myCpu.storeDouble(myCpu, a[i], i)
		myCpu.storeDouble(myCpu, b[i], 2*i)
		myCpu.storeDouble(myCpu, c[i], 0)


	
	#myCpu.ram.print_ram()

	
	en = int(blocking_factor * n/blocking_factor)

	for kk in range(0, en, blocking_factor):
		for jj in range(0, en, blocking_factor):
			for i in range(n):
				for j in range(jj, jj + blocking_factor):
					register0 = myCpu.loadDouble(c[i*n + j])
					#sum = c[i][j]
					for k in range(kk, kk + blocking_factor):
						register1 = myCpu.loadDouble(a[i*n + k])
						register2 = myCpu.loadDouble(b[k*n + j])
						register3 = myCpu.multDouble(register1, register2)
						register0 = myCpu.addDouble(register0, register3)
						#sum += a[i][k] * b[k][j]

					myCpu.storeDouble(myCpu, c[i*n + j], register0)
					# d[i][j] = register0
	#print(d)

	print("\n\n\n")
	myCpu.print_inputs()
	myCpu.print_results()
	print("\n\n\n")
	
	result = []
	for address in c:
		temp_register = myCpu.loadDouble(address)
		result.append(temp_register)
	print(result)

def main():
	print("####################################################################################")
	print("DAXPY Example")

	daxpy_example()
	print("####################################################################################")
	print("\n\n")
	print("####################################################################################")
	print("MxM Example")
	matrix_multiply()
	print("\n\n")
	print("####################################################################################")
	print("MxM blocked Example")
	matrix_multiply_blocking(9,3)
	print("####################################################################################")

main()