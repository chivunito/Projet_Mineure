from PLNE import PLNE
import numpy as np

list_inputs = ["Sources_Files/test5x10.in"]
for one_input in list_inputs:
	aaa=PLNE()
	aaa.read_file(one_input)
	print(aaa.nb_servers)
	aaa.solve()
	print("%.3f" %(aaa.score))
	print(aaa.sizes_server)
	print(aaa.result)
	print("Amount of servers palced:\t%d" %sum(sum(x) for x in aaa.result) )
	a = np.array(aaa.result)
	b = np.array(aaa.sizes_server)
	print("Amount of slots allocated:\t%d" %sum(sum(b*a)))
	print("\n\n ----------------------------------- \n\n")

