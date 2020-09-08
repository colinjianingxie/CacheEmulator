from llist import dllist, dllistnode
from datablock import *
from cpu import *

class Cache_LRU:

    def __init__(self, cpu, num_sets, block_size, n_associativity):

        self.num_sets = num_sets
        self.n_associativity = n_associativity
        self.block_size = block_size

        self.cache_blocks = []
        self.cache_lookup_dict = []
        for i in range(num_sets): 
            empty_dict = {}
            empty_set = dllist()
            self.cache_blocks.append(empty_set)
            self.cache_lookup_dict.append(empty_dict)

        self.cpu = cpu
        self.capacity_in_set = num_sets*[n_associativity]
        self.capacity = int(block_size/8)




        #print("BEFORE:")

    def setDouble(self, address, value):

        input_block_index = address.get_block_index()
        input_block_tag = address.get_block_tag()

        retrieved_set = self.cache_blocks[input_block_index] #Returns a DLL of the set
        retrieved_lookup_set_dict = self.cache_lookup_dict[input_block_index]


        if input_block_tag in retrieved_lookup_set_dict.keys():
            self.cpu.write_hits += 1
            retrieved_dlistnode = retrieved_lookup_set_dict[input_block_tag]
            #print(retrieved_dlistnode)
            for dllnode in retrieved_set:
                if(retrieved_dlistnode == dllnode):
                    dllnode[1].setData(address.get_block_offset(), value)
        else:
            ram_block = self.cpu.ram.getBlock(address)
            self.cpu.write_misses += 1
            if(self.capacity_in_set[input_block_index] > 0): #Still more None blocks inside
                retrieved_set.appendright(dllistnode([address, ram_block]))
                retrieved_lookup_set_dict[input_block_tag] = retrieved_set.nodeat(len(retrieved_set)-1)
                self.capacity_in_set[input_block_index] -= 1

                #print("A: ", retrieved_lookup_set_dict)
            else:

                self.setBlock(address, ram_block)


    def getDouble(self, address):

        input_block_index = address.get_block_index()
        input_block_tag = address.get_block_tag()

        retrieved_set = self.cache_blocks[input_block_index] #Returns a DLL of the set
        #print(retrieved_set)
        retrieved_lookup_set_dict = self.cache_lookup_dict[input_block_index]

        if input_block_tag in retrieved_lookup_set_dict.keys():
            self.cpu.read_hits += 1

            found_node = retrieved_lookup_set_dict[input_block_tag]
            add_to_back_node = retrieved_set.remove(found_node) #Take found node
            retrieved_set.appendright(add_to_back_node) #Add to the back

            retrieved_lookup_set_dict[input_block_tag] = retrieved_set.nodeat(len(retrieved_set)-1)
            return add_to_back_node[1].getValue(address.get_block_offset())


        else:
            ram_block = self.cpu.ram.getBlock(address)
            self.cpu.read_misses += 1
            if(self.capacity_in_set[input_block_index] > 0): #Still more None blocks inside
                retrieved_set.appendright(dllistnode([address, ram_block]))
                retrieved_lookup_set_dict[input_block_tag] = retrieved_set.nodeat(len(retrieved_set)-1)
                self.capacity_in_set[input_block_index] -= 1
                
            else:
                self.setBlock(address, ram_block)
            return ram_block.getValue(address.get_block_offset())




    def setBlock(self, address, datablock):

        #NEED TO EDIT ALL THE OTHER VALUES TO -1, THEN ADD THE NEW INDEX TO THE DICTIONARY

        block_index = address.get_block_index()
        retrieved_set = self.cache_blocks[block_index]
        retrieved_lookup_set_dict = self.cache_lookup_dict[block_index]

        front_node = retrieved_set.popleft() #completely removed
        front_node_tag = front_node[0].get_block_tag()

        if front_node_tag in retrieved_lookup_set_dict: 
            del retrieved_lookup_set_dict[front_node_tag] #Delete the key/value of what's inside the dict originally
        
        retrieved_set.appendright(dllistnode([address, datablock]))
        retrieved_lookup_set_dict[address.get_block_tag()] = retrieved_set.nodeat(len(retrieved_set)-1)


    def getBlock(self, address):
        block_index = address.get_block_index()
        return self.cache_blocks[block_index][1]

    def print_cache(self):
        #print("Number of blocks: ", len(self.cache_blocks))
        #print(self.cache_blocks) 
  
        
        print(self.num_sets)
        print(self.cache_blocks)


        
        for i in range(self.num_sets):
            print("Set Number %d" % (i))
            print("Associated dictionary: ", self.cache_lookup_dict)
            for j in range(self.n_associativity):
                #print(i,j)
                print(self.cache_blocks[i][j][1].getData())
                #print(i,j)
                #print(self.cache_blocks[i][j])
                #print(self.cache_blocks[i][j][0], self.cache_blocks[i][j][1].getData())
            print("-----")
        print(len(self.cache_blocks[0]))

def get_dll(input_dll):
    temp = []
    for i in range(len(input_dll)):
        temp.append((input_dll[i][0].get_block_offset(), input_dll[i][1]))
    return temp


