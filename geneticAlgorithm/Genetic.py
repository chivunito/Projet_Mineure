from deap import base, creator
from geneticAlgorithm.geneticMethod import *

def createToolbox(knapSacks, servers):
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)
    toolbox = base.Toolbox()

    toolbox.register("attr_bool", generateRandom, 0, len(knapSacks) - 1, 1)
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=len(servers))
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", evaluate, servers, knapSacks)
    # toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mate", validCrossover, servers=servers, knapSackList=knapSacks)
    # toolbox.register("mutate", tools.mutFlipBit, indpb=0.1)
    # toolbox.register("mutate", mutNewKnapSack,knapSackLen=len(knapSack)-1,prbFlip=0.2)
    toolbox.register("mutate", mutNewKnapSack, knapSackLen=len(knapSacks) - 1, prbFlip=0.5)
    toolbox.register("select", tools.selTournament, tournsize=3)
    return toolbox

def sortServers(servers,lambdaFunction):
    newServers=sorted(servers,key=lambdaFunction)
    return newServers

if __name__=="__main__":
    problem = Multiple_knapsack("Sources_Files/dc.in")
    # problem = Multiple_knapsack("Sources_Files/dcEasy.in")
    knapsacks = problem.flat()
    servers = problem.servers
    #
    servers=sorted(problem.servers,key=lambda x:-x[1]/x[0])
    servers=sorted(problem.servers,key=lambda x:-x[1])
    toolbox=createToolbox(knapsacks,servers)

    ind1,ind2=toolbox.population(2)
    toolbox.mate(ind1,ind2)

    pop = toolbox.population(n=30)
    # pop, logbook = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.8, ngen=2, verbose=True)
    # bestList = tools.selBest(pop, k=10)[0]
    res,res2=toolbox.mate(pop[0],pop[1])

    print(toolbox.evaluate(res))