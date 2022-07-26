import AirConditioning as ac
import random

Path = "FIXTHIS"
maxPred = 0.9
TempSpace = ac.tSpace(directory = Path+'tspace')
#PermSpace = ac.pSpace(directory = Path+'pspace')
def Ingest(obj): #idk excatly what this one's going to do
    pred = TempSpace.getPred(obj)
    if(pred<maxPred or random.random()>pred): #unpredictable states need to be added to system
        Lstruct = TempSpace.getLastStruct()
      #  InStruct = getStructIn(TempSpace,obj) #why...?
        Struct = getStructIn(TempSpace,obj)
    #TODO: fix and extend this func
        
def getStructIn(space,statement): #only first order- Use edge collapse for more abstract structures
    struct = []
    structims = []
    c = 0
    while(c<len(statement)): 
        c2 = c
        while(c2<len(statement)):
            coins = space.ac.Retrive2Coincidences(statement[c],statement[c2])
            coincounts = []
            while(c3<len(coins)):
                coincounts.append(0)
                c4 = 0
                while(c4<len(coins[c3])):
                    if(coins[c3][c4] in statement):
                        coincounts[c3] += 1
                        coins[c3][c4] = "VAR"+statement.index(coins[c3][c4])
                    c4 += 1
                struct.append(coins[c3]) #scoring??
                structims.append(coincounts[-1]/len(coins))
                c3 += 1
            c2 += 1
        c += 1
    struct.append(statement)
    return struct #very basic version
def GetStructSim(struct1,struct2): #neccessary for compareing predicates
    c = 0
    while(c<len(struct)) #how to do this without it taking like quartic time???
    
    

