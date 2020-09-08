from datablock import *
from address import *

import math


class Ram:
	def __init__(self, cpu, num_blocks, block_size, num_elements):
		self.num_blocks = num_blocks
		self.block_size = block_size
		self.cpu = cpu
		self.data = []
		self.num_elements = num_elements

		for i in range(num_blocks):
			temp_data_block = DataBlock(block_size, None)
			self.data.append(temp_data_block)




	def setDouble(self, address, value):
		block_num = address.get_block_number()
		#print("num blocks is %d and block_num is %d" %(self.num_blocks, block_num))
		block_offset = address.get_block_offset()
		#print("Attempting to add to datablock[%d] and  internal position[%d] = %.1f" % (block_num, block_offset, value))
		#print("Address:   %d    Block number: %d    Offset number: %d   " % (address.get_address(), block_num, block_offset))

		self.data[block_num].setData(block_offset, value)
		


	def getBlock(self, address):
		block_num = address.get_block_number()
		return self.data[block_num]


	def get_total_size(self):
		return 8 * self.num_elements

		#return self.num_blocks * self.block_size

	def print_ram(self):
		counter = 0
		temp_stuff = []

		for datablock in self.data:
			for i in range(int(self.block_size/8)):
				temp_stuff.append(datablock.getValue(i))
		print(temp_stuff)
		print("Num blocks ", self.num_blocks)
		#print("Total number of elements in RAM: " + str(len(temp_stuff)))
		#print("Total number of unique elements in RAM: " + str(len(set(temp_stuff))))
		#print(temp_stuff)
	
		

		