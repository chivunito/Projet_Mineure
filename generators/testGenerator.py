import random
#R : number of racks
#S : Slots per rack (Same for all racks)
#U : Unavailable slots
#M : Number of servers to place



#Todo: Eliminate redundancy
def generateServ(lenMax):
    size= random.randint(1,lenMax)
    capacity = random.randint(1,21)
    return size, capacity

def generateIndispo(R, S):
    x = random.randint(0,R-1)
    y = random.randint(0,S-1)
    return x, y

def generateTest(fileName,racks, slots, unavailable, servers, pools=1):
    with open("../Sources_Files/"+fileName+str(racks)+"x"+str(slots)+".in",'w') as file :
        line = str(racks)+" "+str(slots)+" "+str(unavailable)+" "+str(pools)+ " "+ str(servers)+"\n"
        file.write(line)

        for i in range(unavailable):
            x,y = generateIndispo(racks,slots)
            file.write(str(x)+" "+str(y)+"\n")

        for i in range(servers):
            size,capacity = generateServ(slots)
            file.write(str(size)+" "+str(capacity)+"\n")


if __name__=="__main__":
    racks=20
    slots=100
    generateTest("test",racks=racks,slots=slots,unavailable=racks*2,servers=racks*slots,pools=1)
