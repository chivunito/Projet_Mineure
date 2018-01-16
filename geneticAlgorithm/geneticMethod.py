import numpy as np
import random
from deap import tools


def generateRandom(borneInf=0, borneSup=0, pourcentage=0):
    """
    :param borneInf: Compris
    :param borneSup: Compris
    :param pourcentage: Pourcentage de valeur différentes de -1 ( pas dans un sac )
    :return:
    """
    if random.random() < pourcentage:
        return random.randint(borneInf, borneSup)
    else:
        return -1

def evaluate(servers, knapsack, individu):
    """
    :param size: taille des serveurs
    :param puissance: puissance des serveurs
    :param knapsack: Tailles des knapSacks
    :param individu: Liste de longueur serveurs, tel que individu[serveurID]=-1 si le serveurID n'est pas pris, à n s'il est présent dans le sac n
    :return: puissance totale qui est égale à la somme des serveurs pris
    """
    servers = np.array(servers)
    size, puissance = servers[:, 0], servers[:, 1]
    individu = np.array(individu)
    puissanceTotale = sum(puissance[individu >= 0])
    for i, capacite in enumerate(knapsack):
        poids = sum(size[individu == i])
        if poids > capacite:
            # print('poids dépassé dans knapsack',i,poids,capacite)
            # puissanceTotale-=100
            puissanceTotale = 0
    # print(puissanceTotale)
    return (puissanceTotale,)


def mutNewKnapSack(individu, knapSackLen, prbFlip):
    for i in range(len(individu)):
        if random.random() < prbFlip   and individu[i]==-1:
            individu[i] = random.randint(0, knapSackLen)
    return (individu,)


def deleteOverflow(offspring, servers, knapSackList):
    offspringCopy = np.array(offspring)
    servers = np.array(servers)
    size, puissance = servers[:, 0], servers[:, 1]
    for knapSackID, knapSackCapacity in enumerate(knapSackList):
        poids = sum(size[offspringCopy == knapSackID])
        overflow = poids - knapSackCapacity
        # print('knapID:',knapSackID,'poids',poids,'capacity',knapSackCapacity)
        while overflow > 0:
            indexServerToRemove = np.where(offspringCopy == knapSackID)[0][-1]
            offspringCopy[indexServerToRemove] = -1
            overflow -= size[indexServerToRemove]
            # print(offspring==knapSackID)
        # print(sum(size[offspring==knapSackID])-knapSackCapacity)
    for i in range(len(offspring)):
        offspring[i] = offspringCopy[i]
    return offspring


def validCrossover(ind1, ind2, servers, knapSackList):
    """
    Objectif : faire un crossover entre deux individus tout en conservant la validité du knapsack
    :param ind1:
    :param ind2:
    :param servers:
    :param knapSackList:
    :return: offspring Individu
    """
    offspring1, offspring2 = tools.cxOnePoint(ind1, ind2)
    offspring1 = deleteOverflow(offspring1, servers, knapSackList)
    offspring2 = deleteOverflow(offspring2, servers, knapSackList)
    return offspring1, offspring2


if __name__=="__main__":
    None
    # problem = Multiple_knapsack("Sources_Files/dcEasy.in")
    # ind1=[1,1,1,-1,-1]
    # ind2=[-1,-1,-1,1,1]
    # knapsack=problem.flat()
    # servers=problem.servers
    # print('knapSack',knapsack)
    # print('servers',servers)
    # of1,of2=validCrossover(ind1,ind2,servers,knapsack)
    # print(of1)
# offspring1,offspring2=validCrossover(ind1,ind2,servers,knapSack)
# # offspring1,offspring2=tools.cxOnePoint(ind1,ind2)
# print(offspring1,offspring2)

# print(np.where(offspring1==-1),evaluate(servers,knapSack,offspring2))
