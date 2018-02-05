from deap import base, creator,algorithms
from geneticAlgorithm.geneticMethod import *
from DataCenter import *
import networkx

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

def scoreModel(servers,knapsacks,cxpb=0.1,mutpb=0.1,popSize=50,nGen=50,verbose=False):
    toolbox = createToolbox(knapsacks, servers)

    # Create Statistics
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("min", np.min)
    stats.register("max", np.max)

    pop = toolbox.population(n=popSize)
    pop, logbook = algorithms.eaSimple(pop, toolbox, cxpb=cxpb, mutpb=mutpb, ngen=nGen, verbose=verbose, stats=stats)
    best = tools.selBest(pop, 1)[0]
    score=toolbox.evaluate(best)
    gen, avg, min_, max_ = logbook.select("gen", "avg", "min", "max")
    return gen,max_,best,score

if __name__=="__main__":
    problem = Multiple_knapsack("Sources_Files/test10x50.in")
    # problem = Multiple_knapsack("Sources_Files/test5x10.in")
    # problem = Multiple_knapsack("Sources_Files/dcEasy.in")
    # problem.plot()
    knapsacks = problem.flat()
    servers = problem.servers
    # servers=sorted(problem.servers,key=lambda x:-x[1])
    print("Place disponible : ",problem.shape[0]*problem.shape[1]-len(problem.indispo))

    popSize=10
    nGen=100
    maxDico={}

    scoreModel(servers, knapsacks, cxpb=0.1, mutpb=0.2)

    # for mutpb in np.linspace(0.05,0.9,10):
    #     maxDico[mutpb]=scoreModel(servers,knapsacks,cxpb=0.1,mutpb=mutpb)

    plt.plot(gen, avg, label="average")
    # plt.plot(gen, min_, label="minimum")
    # plt.plot(gen, max_, label="maximum")
    # plt.xlabel("Generation")
    # plt.ylabel("Fitness")
    # plt.legend(loc="lower right")
    # plt.show()



    # best=tools.selBest(pop,1)[0]
    # best=np.array(best)
    # servers=np.array(servers)
    # # print(servers[best])
    # serveurRetenus=servers[best>-1]
    # print(sum(serveurRetenus[:,0]))
    # print(sum(serveurRetenus[:,1]))
