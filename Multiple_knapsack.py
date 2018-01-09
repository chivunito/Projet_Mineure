import numpy as np
import matplotlib.pyplot as plt
from enum import Enum


""" Multiple_knapsack (class) :  
Pour représenter le problème on utilise une matrice (racks x slots) d'integer. Une slot est représenté par : 
    - -1 si la case est indisponible
    - 0 si la case est disponible
    - 1 si il y'a un serveur placé
on associe à un KnapSack son score, c'est à dire la puissance de calcul présente sur l'ensemble de la matrice 
"""

class State(Enum):
    EMPTY = 0
    SERVER = 1
    UNAVAILABLE = -1

class Multiple_knapsack:
    def __init__(self, filePath):
        self.filePath = filePath
        self.score = 0
        self.placedServers={}
        self.fileToProblem()

    def fileToProblem(self):
        fileList = []
        with open(self.filePath, "r") as file:
            for line in file:
                liste = line.replace("\n", "").split(" ")
                liste = [int(x) for x in liste]
                fileList.append(liste)
        self.racks, self.slots, nbIndispos, self.pools, nbServers = fileList.pop(0)
        self.shape=(self.racks,self.slots)
        self.matrix = np.zeros((self.racks, self.slots))

        self.indispo = fileList[:nbIndispos]
        for rowIndispo, colIndispo in self.indispo:
            self.matrix[rowIndispo][colIndispo] = -1

        self.servers = fileList[nbIndispos:]

    def placeServer(self,origin, server):
        size, puissance = server

        # Using Slices
        matrix=self.matrix[origin[0]:origin[0]+1,origin[1]:origin[1]+size]
        slice=matrix[0]
        if np.count_nonzero(slice)==0 and len(slice)==size:
            self.matrix[origin[0]:origin[0] + 1, origin[1]:origin[1] + size]=1
            self.score+=puissance
            self.placedServers[origin]=server
            self.servers.remove(server)
        else :
            print("Impossible de placer le serveur")

    def removeServer(self,origin,server=None):
        server=self.placedServers[origin]
        size,puissance=server
        self.score-=puissance
        self.matrix[origin[0]:origin[0] + 1, origin[1]:origin[1] + size]=0
        self.servers.append(server)
        del self.placedServers[origin]

    def getState(self, row, col):
        """ Return true if the coordinate is available
        """
        value=self.matrix[row, col]
        if value == -1:
            return State.UNAVAILABLE
        elif value == 0 :
            return State.EMPTY
        else:
            return State.SERVER

    def flat(self):
        knapSackList=[]
        for row in self.matrix :
            index=list(np.argwhere(row==-1))
            if len(index)>0:
                index=[x[0] for x in index]
                index.insert(0,-1)
                index.append(self.slots)
                for start,end in zip(index[:-1],index[1:]):
                    sackSize=end-start-1
                    if sackSize>0 :
                        knapSackList.append(sackSize)
            else :
                knapSackList.append(self.slots)
        return knapSackList

    def __getitem__(self, key):
        return self.matrix[key]

    def __str__(self):
        string = "Multiple_knapsack_Problem ("+str(self.racks)+"racks,"+str(self.slots)+"slots)\n"
        string +="Puissance totale "+str(self.score)+", serveurs placés : "+str(len(self.placedServers)) +"\n"
        for origin,server in self.placedServers.items() :
            string+="   "+str(origin)+": size "+str(server[0])+" puissance : "+str(server[1])
        return string

    def plot(self):
        plt.imshow(self.matrix)
        plt.show()


if __name__ == "__main__":
    problem = Multiple_knapsack("Sources_Files/dc.in")

    # # Build the Mutltiple_Knapsack problem according to a source file ( given a filePath )
    # problem = Multiple_knapsack("Sources_Files/dcEasy.in")
    #
    # # Retrieving server List ( remaining one to place on the matrix )
    # print(problem.servers)
    #
    # # Accessing the Matrix
    # # print(problem.matrix.shape)
    # # print(problem.matrix[0])  #  Print first line
    # # print(problem.matrix[0, 0])  #  Print first case
    #
    # # Return the state given the coordinate     EMPTY = 0    SERVER = 1    UNAVAILABLE = -1
    # print(problem.getState(1, 0))
    #
    # # Plot the game
    # # problem.plot()
    #
    # # Place a server on the matrix
    # origin=(0,1)
    # problem.placeServer(origin,problem.servers[0])
    # # Now we can print the servers on the racks :
    # print(problem.placedServers)
    # # the remaining one are :
    # print(problem.servers)
    #
    # problem.plot()
    #
    # # Summary on the problem :
    # print(problem)

