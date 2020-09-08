Programmed in: Python 3

This project is to emulate what a cache does for matrix x matrix multiplication.

Libraries needed to run:
- pip3 install llist
- pip3 install argparse (if its not already included)



Files included in this project:

- address.py: 			address class
- algorithms.py: 		algorithms that will be used to test (daxpy, mxm, mxm_blocked)
- cache_fifo.py:		Cache that has a FIFO replacement policy
- cache_lru.py: 		Cache that has an LRU replacement policy
- cache_random.py:		Cache that has a random replacement policy
- cache_sim.py: 		Cache simulator (example on how to run below)
- correctness.py: 		Used for 2.1 (to test correctness)
- cpu.py: 				CPU class
- datablock.py: 		Datablock class
- ram.py: 				Ram class



To test correctness, go to Terminal/CMD prompt: python3 correctness.py

To run the emulator: python3 cache_sim.py (insert flags) 

FLAGS allowed:
-c: 	size of cache in bytes			(default 65536)
-b: 	size of datablock in bytes		(default 64)
-n:		n-way associativity of cache 	(default 2)
-r: 	replacement policy				(default LRU) - can be: LRU, FIFO, random
-a: 	algorithm to simulate			(default mxm_block) - can be: mxm_block, mxm, daxpy
-d: 	dimension of vector/matrix		(default 480)
-p: 	enable printing					(default 0) - can be: 0, 1
-f: 	blocking factor					(default 32)


An example run: python3 cache_sim.py -a mxm_block -c 512 -r random -p








