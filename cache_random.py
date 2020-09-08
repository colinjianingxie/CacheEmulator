from datablock import *
from random import randrange
from cpu import *

class Cache_Random:
	def __init__(self, cpu, num_sets, block_size, n_associativity):
		self.num_sets = num_sets
		self.n_associativity = n_associativity
		self.block_size = block_size
		#self.cache_blocks = num_sets * [None]
		self.cache_blocks = []

		for i in range(num_sets): 
			self.cache_blocks.append(n_associativity*[None])

		self.cpu = cpu
		
		#print("BEFORE:")

	def setDouble(self, address, value):

		input_block_index = address.get_block_index()
		input_block_tag = address.get_block_tag()

		retrieved_set = self.cache_blocks[input_block_index]
		#print("Attempting to put into set ", input_block_index)
		# self.data[block_num].setData(block_offset, value)

		# WHEN STORING DOUBLE
		# CHECK IF THE BLOCK IS NONE
		# 	IF NONE, Get the block from RAM and store it there
		# 	Count as compulsory miss
		# If there's a block inside already
		# 	Copy the block associated with the double from the ram and store it inside the cache block

		block_is_in_cache = False

		none_block_num = -1


		for i in range(self.n_associativity): #going through the blocks in the set
			retrieved_set_block = retrieved_set[i]		
			if retrieved_set_block == None:
				#print("There exists a none block in set %d for block %d " % (input_block_index, i))
				none_block_num = i
			else:
				# (addr, block)
				# 0 = addr
				# 1 = actual block
				#print("RETRIEVED BLOCK: ", retrieved_block)
				if retrieved_set_block[0].get_block_tag() == input_block_tag:
					self.cpu.write_hits += 1
					block_is_in_cache = True
					retrieved_set[i][0] = address #change address of block, last accsesed address
					retrieved_set[i][1].setData(address.get_block_offset(), value) #change value of datablock
					#print("After a hit, my datablock is: ", retrieved_set[i][1].getData())
					break
			
		
		if block_is_in_cache == False: #block is not in cache


			ram_block = self.cpu.ram.getBlock(address)
			#print("Retrieved ram block ", ram_block.getData())
			
			self.cpu.write_misses += 1
			if none_block_num != -1: #IF THERE EXISTS A NONE BLOCK, JUST STICK IT IN THERE
				retrieved_set[none_block_num] = [address, ram_block]
				
			else:	#IF EVERYTHING IS FILLED, NEED TO USE REPLACEMENT POLICY
				
				self.setBlock(address, ram_block)



	def getDouble(self, address):
		#What's eing passed in
		input_block_index = address.get_block_index()	
		input_block_tag = address.get_block_tag()

		#What's currently in cache
		retrieved_set = self.cache_blocks[input_block_index]


		block_is_in_cache = False
		none_block_num = -1
	
		for i in range(self.n_associativity): #going through the blocks in the set
			retrieved_block = retrieved_set[i]		
			if retrieved_block == None:
				none_block_num = i
			else:
				# (addr, block)
				# 0 = addr
				# 1 = actual block
				#print("RETRIEVED BLOCK: ", retrieved_block)
				#print("Block tag is {} and retrievd block tag is {}".format(input_block_tag, retrieved_block[0].get_block_tag()))
				if retrieved_block[0].get_block_tag() == input_block_tag:
					self.cpu.read_hits += 1
					return retrieved_block[1].getValue(address.get_block_offset())
			
		

		if block_is_in_cache == False: #Block is not in cache
			
			ram_block = self.cpu.ram.getBlock(address)

			if none_block_num != -1: #IF THERE EXISTS A NONE BLOCK, JUST STICK IT IN THERE
				retrieved_set[none_block_num] = [address, ram_block]

			else:	#IF EVERYTHING IS FILLED, NEED TO USE REPLACEMENT POLICY
				self.cpu.read_misses += 1
				self.setBlock(address, ram_block)

			return ram_block.getValue(address.get_block_offset())



	def setBlock(self, address, datablock):
		block_index = address.get_block_index()

		index = randrange(self.n_associativity)
		self.cache_blocks[block_index][index] = [address, datablock]


	def getBlock(self, address):
		block_index = address.get_block_index()
		return self.cache_blocks[block_index][1]

	def print_cache(self):
		print("Number of blocks: ", len(self.cache_blocks))


		for i in range(self.num_sets):
			print("Set Number %d" % (i))
			for j in range(self.n_associativity):
				if(self.cache_blocks[i][j] == None):
					print("None found at [%d][%d]" % (i,j))
				else:
					print(self.cache_blocks[i][j][0], self.cache_blocks[i][j][1].getData())
			print("-----")




