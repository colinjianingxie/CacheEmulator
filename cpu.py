from address import *
from cache_random import *
from cache_fifo import *
from cache_lru import *
from ram import *
import math

class CPU:
	def __init__(self, cache_size=65536, block_size=64, n_associativity=2, replacement_policy="LRU", algorithm="mxm_block", dimension=480, printing=0, blocking=32):
		self.cache_size = cache_size
		self.block_size = block_size
		self.n_associativity = n_associativity
		self.replacement_policy = replacement_policy
		self.algorithm = algorithm
		self.dimension = dimension
		self.printing = printing
		self.blocking = blocking




		self.num_blocks = int(cache_size/block_size)
		self.num_sets = int(cache_size/(n_associativity*block_size))

		self.instruction_count = 0
		self.read_hits = 0
		self.read_misses = 0
		self.write_hits = 0
		self.write_misses = 0

		if replacement_policy == "random":
			self.cache = Cache_Random(self, self.num_sets, block_size, n_associativity)
		elif replacement_policy == "FIFO":
			self.cache = Cache_FIFO(self, self.num_sets, block_size, n_associativity)
		elif replacement_policy == "LRU":
			capacity = int(block_size/8)
			self.cache = Cache_LRU(self, self.num_sets, block_size, n_associativity)

		if algorithm is not "daxpy":
			self.ram = Ram(self, math.ceil(dimension*dimension*3*8/block_size), block_size, dimension*dimension*3)
		else:
			self.ram = Ram(self, math.ceil(3*dimension*8/block_size), block_size, dimension * 3)


	def get_inputs(self):
		input_str = "INPUTS===================================================================\n \
		Ram Size = " + str(self.ram.get_total_size()) + "\n \
		Cache Size = " + str(self.cache_size) + "\n \
		Block Size = " + str(self.block_size) + "\n \
		total blocks in cache = " + str(self.num_blocks) + "\n \
		Cache Size = " + str(self.cache_size) + "\n \
		Cache Size = " + str(self.cache_size) + "\n \
		Cache Size = " + str(self.cache_size) + "\n \
		Cache Size = " + str(self.cache_size) + "\n \
		Cache Size = " + str(self.cache_size) + "\n \
		"

	def print_inputs(self):

		print("INPUTS===================================================================")
		print("Ram Size =                     %d bytes" % (self.ram.get_total_size()))
		print("Cache Size =                   %d bytes" % (self.cache_size))
		print("Block Size =                   %d bytes" % (self.block_size))
		print("Total Blocks in Cache =        %d" % (self.num_blocks))
		print("Associativity =                %d" % (self.n_associativity))
		print("Number of Sets =               %d" % (self.num_sets))
		print("Replacement Policy =           %s" % (self.replacement_policy))
		print("Algorithm =                    %s" % (self.algorithm))
		print("MXM Blocking Factor =          %d" % (self.blocking))
		print("Matrix or Vector dimennsion =  %d" % (self.dimension))
		
	def print_results(self):
		print("RESULTS===================================================================")
		print("Instruction count = %d" % (self.instruction_count))
		print("Read hits =         %d" % (self.read_hits))
		print("Read misses =       %d" % (self.read_misses))
		print("Read miss rate =    %.2f" % (100.0*self.read_misses/(self.read_misses + self.read_hits)))
		print("Write hits =        %d" % (self.write_hits))
		print("Write misses =      %d" % (self.write_misses))
		print("Write miss rate =   %.2f" % (100.0*self.write_misses/(self.write_misses + self.write_hits)))
	def storeDouble(self, cpu, address, value):
		#Store value into RAM
		double_address = Address(address, self.block_size, self.num_sets)

		#self.cache.setDouble(double_address, value)
		#print("TRYING TO STORE value %.1f at address %d" % (value, address))


		self.ram.setDouble(double_address, value)
		self.cache.setDouble(double_address, value)



		self.instruction_count += 1
	
	def loadDouble(self, address):
		self.instruction_count += 1
		double_address = Address(address, self.block_size, self.num_sets)
		return self.cache.getDouble(double_address)

	def multDouble(self, value1, value2):
		self.instruction_count += 1
		return value1 * value2
	def addDouble(self, value1, value2):
		self.instruction_count += 1
		return value1 + value2

	

