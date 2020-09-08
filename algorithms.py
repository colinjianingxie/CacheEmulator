from cpu import *



def daxpy(c, b, n, r, ds, p):
	myCpu = CPU(cache_size=c, block_size=b, n_associativity=n, replacement_policy=r, algorithm="daxpy", dimension=ds, printing=p, blocking=8)

	
	a = list(range(0, ds, 1))
	b = list(range(ds, 2*ds, 1))
	c = list(range(2*ds, 3*ds, 1))



	for i in range(ds):
		myCpu.storeDouble(myCpu, a[i], i)
		myCpu.storeDouble(myCpu, b[i], 2*i)
		myCpu.storeDouble(myCpu, c[i], 0)
	
	
	d = 3
	for i in range(ds):
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
	if p == 1:
		result = []
		for address in c:
			temp_register = myCpu.loadDouble(address)
			result.append(temp_register)
		print(result)



	


def matrix_multiply(cacheSize, blockSize, nAssociativity, replacementPolicy, dimensionSize, p):
	n = dimensionSize
	myCpu = CPU(cache_size=cacheSize, block_size=blockSize, n_associativity=nAssociativity, replacement_policy=replacementPolicy, algorithm="mxm", dimension=dimensionSize, printing=p)


	a = list(range(0, n*n, 1))
	b = list(range(n*n, 2*n*n, 1))
	c = list(range(2*n*n, 3*n*n, 1))



	for i in range(n*n):
		myCpu.storeDouble(myCpu, a[i], i)
		myCpu.storeDouble(myCpu, b[i], 2*i)
		myCpu.storeDouble(myCpu, c[i], 0)
	
	


   #base_addr + ith_row*len_row + col_num
	for i in range(n):
		for j in range(n):
			register0=0
			for k in range(n):
				register1 = myCpu.loadDouble(a[i*n+k])
				register2 = myCpu.loadDouble(b[k*n+j])
				#print(register1)

				register3 = myCpu.multDouble(register1, register2)
				register0 = myCpu.addDouble(register0, register3)
			myCpu.storeDouble(myCpu, c[i*n + j], register0)




	if p == 1:
		print("\n\nActual result\n")
		result = []
		for address in c:
			temp_register = myCpu.loadDouble(address)
			result.append(temp_register)
		print(result)

	print("\n\n\n")
	myCpu.print_inputs()
	myCpu.print_results()
	print("\n\n\n")
	

# ALGORITHM RETRIEVED FROM https://stackoverflow.com/questions/40050761/python-matrix-multiplication-and-caching
def matrix_multiply_blocking(cacheSize, blockSize, nAssociativity, replacementPolicy, dimensionSize, blocking_factor, p):

	myCpu = CPU(cache_size=cacheSize, block_size=blockSize, n_associativity=nAssociativity, replacement_policy=replacementPolicy, algorithm="mxm_block", dimension=dimensionSize, printing=p, blocking=blocking_factor)


	n=dimensionSize
	#d = zero_matrix(n,n)

	a = list(range(0, n*n, 1))
	b = list(range(n*n, 2*n*n, 1))
	c = list(range(2*n*n, 3*n*n, 1))


	temp_c = 0
	for i in range(n*n):
		myCpu.storeDouble(myCpu, a[i], i)
		myCpu.storeDouble(myCpu, b[i], 2*i)
		myCpu.storeDouble(myCpu, c[i], 0)


	for kk in range(0, n, blocking_factor):
		for jj in range(0, n, blocking_factor):
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

	
	# for kk in range(0, dimensionSize, blocking_factor):
	# 	for jj in range(0, dimensionSize, blocking_factor):
	# 		for i in range(dimensionSize):
	# 			rI = dimensionSize*i
	# 			for j in range(jj, jj + blocking_factor):
	# 				register0 = myCpu.loadDouble(c[rI + j])
	# 				for k in range(kk, kk + blocking_factor):
	# 					register1 = myCpu.loadDouble(a[i])
	# 					register2 = myCpu.loadDouble(b[i])
	# 					register3 = myCpu.multDouble(register1, register2)
	# 					register0 = myCpu.addDouble(register0, register3)

	# 				myCpu.storeDouble(myCpu, c[rI + j], register0)
	#print(d) #d is result
	if p == 1:
		print("\n\nActual result\n")
		result = []
		for address in c:
			temp_val = myCpu.loadDouble(address)
			result.append(temp_val)
		print(result)

	print("\n\n\n")
	myCpu.print_inputs()
	myCpu.print_results()
	print("\n\n\n")


