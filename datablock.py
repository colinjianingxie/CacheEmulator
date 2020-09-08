

class DataBlock:
	def __init__(self, size, data):
		self.size = size
		self.data = int(size/8)*[data]
	def setData(self, position, value):
		self.data[position] = value
	def getSize(self):
		return self.size
	def getValue(self, position):
		return self.data[position]
	def getData(self):
		return self.data
	