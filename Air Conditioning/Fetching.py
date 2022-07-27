import AirConditioning as ac
import random
import HYPER as H
# this file is slightly higher level, handling low-level learning and prediction functions.
Path = H.MAIN_DIRECTORY
maxPred = H.EMBED_MAX_PRED_SCORE
TempSpace = ac.tSpace(directory = Path+'tspace',max = H.TEMPSPACE_MAX_SYMBOLS)
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
    c = 0
    while(c<len(statement)): 
        c2 = c
        while(c2<len(statement)):
            coins,importance,anchors = space.ac.Retrive2Coincidences(statement[c],statement[c2])
            coincounts = []
            while(c3<len(coins)):
                coincounts.append(0)
                c4 = 0
                while(c4<len(coins[c3])):
                    if(coins[c3][c4] in statement):
                        coincounts[c3] += 1
                        coins[c3][c4] = "VAR"+statement.index(coins[c3][c4])
                    c4 += 1
                struct.append([coins[c3],(-coincounts[-1]-importance*0.1)/len(coins)]) #scoring??
                c3 += 1
            c2 += 1
        c += 1
    struct.sort(key = sortFunc)
    struct.append([statement,-999])
    return struct #very basic version
def sortFunc(e):
    z = e[1] #also removes importances from list. Should it? idk, but i don't have a use for them elsewhere right now, so... better not to handle an extra set of variables.
    e = e[0]
    return z
def GetStructSim(struct1,struct2): #neccessary for compareing predicates
    #USE CLIPPED STRUCTS!!!!
        #otherwise this could take wwwaaaaaayyyyyyy tooooo looooonnnnnng
    raw_sim = 0
    c = 0
    while(c<len(struct1)): #how to do this without it taking like quartic time???
                            # there must be a better way, probably by storing markers or such, but im not going to spend hours on this function.
        c2 = c
        while(c2<len(struct2)):
            c3 = 0
            while(c3<len(struct1[c])):
                c4 = 0
                while(c4<len(struct2[c2])):
                    n = 0
                    while(struct1[c][c3+n] == struct2[c2][c4+n]):
                        n += 1
                    raw_sim += n
                    c4 += 1
                c3 += 1
            c2 += 1
        c += 1
    return raw_sim/(len(struct1)*len(struct2)) #normalization. this is not done in the inner section because longer/more coincidences should be noted regardless of length in induvidual statements??? idk, might need fixing.


