import random
#R : number of racks
#S : Slots per rack (Same for all racks)
#U : Unavailable slots
#M : Number of servers to place
R = 42
S = 10
M = 15
U = 12
P = 2


#Todo: Eliminate redundancy
def generateServ():
    size= random.randint(1,S)
    capacity = random.randint(1,21)
    return size, capacity

def generateIndispo(R, S):
    x = random.randint(0,S)
    y = random.randint(0,R)
    return x, y

def generateTest(racks=R, slots=S, unavailable=U, servers=M, pools=P):
        file = open('test.in', 'w')
        line = str(racks)+" "+str(slots)+" "+str(unavailable)+" "+str(pools)+ " "+ str(servers)+"\n"
        file.write(line)
        
        for i in range(U):
            x,y = generateIndispo(R,S)
            file.write(str(y)+" "+str(x)+"\n")
        
        for i in range(R):
            size,capacity = generateServ()
            file.write(str(size)+" "+str(capacity)+"\n")
            
        file.close()

generateTest()
