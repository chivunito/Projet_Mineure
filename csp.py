from Multiple_knapsack import Multiple_knapsack
from docplex.cp.model import CpoModel

from config import setup
setup(Presolve='On', Workers='Auto')

# Build the Mutltiple_Knapsack problem according to a source file ( given a filePath )
problem = Multiple_knapsack("Sources_Files/test20x100.in")
mdl = CpoModel()

#x is the list of serv attributions, containing the indices of the rack
#for example: [2, 3, 2, 42, 12, -1] is a list of 5 servers that are respectively contained by the rack 2, 3, 2 and so on
#thus we ensure that a server is placed at best once.
#servers at len(flat()) aren't slotted
flat = problem.flat()
servsAttribList = mdl.integer_var_list(len(problem.servers), 0, len(flat), "x")

loads = mdl.integer_var_list(len(flat) + 1, name="load")

mdl.add(mdl.pack(loads, servsAttribList,
                 [srv[0] for srv in problem.servers]))

for i in range(len(flat)):
    mdl.add(loads[i] <= flat[i])
    
profits = mdl.integer_var_list(len(flat) + 1, name="profit")

mdl.add(mdl.pack(profits, servsAttribList,
                 [srv[1] for srv in problem.servers]))

mdl.add(mdl.maximize(mdl.sum(profits[:-1])))

sol = mdl.solve(TimeLimit=300, TimeMode='CPUTime', SearchType='Restart', SequenceInferenceLevel='Extended')
print("\n--------\n")
print("Total CPU Power available:", sum(sol[p] for p in profits[:-1]))
print("Server distributions: {}/{}".format(
    sum(sol[x] != len(flat) for x in servsAttribList),
    len(problem.servers)))
