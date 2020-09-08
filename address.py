
class Address:
	def __init__(self, address, block_size, num_sets):
		self.address = address 
		self.block_size = block_size
		self.num_sets = num_sets
	
	def get_address(self):
		return self.address
		
	def get_block_number(self):
		#return int(self.address % self.num_blocks)
		return int(self.address/(self.block_size//8))

	def get_block_offset(self):
		#return int(self.get_block_number() % (self.block_size//8))
		return int(self.address % (self.block_size//8))

	def get_block_tag(self):
		return int(self.get_block_number()/self.num_sets)

	def get_block_index(self):
		return int(self.get_block_number() % self.num_sets)
