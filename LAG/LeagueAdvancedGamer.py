import numpy as np
from MOpack import MatrixOperations as MO
import LowLevel as LL
#League Advanced Gamer (LAG or LAGer) primary decision system

#Depends on LowLevel.py and MOpack.py

#technical overveiw:
#the overall archetecture technically falls under the DNC catergory, but
#the main network's archetecture is complex, to say the least- it is
#composed of many smaller networks, which predict distributions of reward
#for both internal and external actions. The actions are scored based on these
#distributions. The reward predictors are trained using distributional TD
#learning, which also means it (theoretically) has the capacity to generalize
#and learn even when it is not recieving feedback. The reward predictors are
#DGNs (dendric gated networks), which (theoretically) migitates catistrophic
#forgetting and speeds up training.

#UPDATE:
#to reduce required computaional resources, there are several large networks
#predicting reward for entire state vector, rather than a bunch of smaller nets.

#the actions (both internal and external) are strictly binary, which is
#inconvinent for several reasons but ultimitly simplifies the algorithim,
#and allows it to better compare predicted rewards.


#do NOT feed image input into class, preprocess first with autoencoder and/or convultional network
#Has memory systems, so experience replay based training tequneqies will be inconsistent or fail to work altogether


#Params:
# 0- length of mutable state
# 1- networks per digit in mutble state
# 2- width of each network
# 3- branches per net
# 4- width of total state
# 5- input length
# 6- memory key length
# 7- memory max length
# 8- output length
class LAG:
    def __init__(self,params,LsParams,Personality,file):
        self.Params = params
        self.mSL = self.Params[0]
        self.NpS = self.Params[1]
        self.Nw = self.Params[2]
        self.File = file
        self.LsP = LsParams
        self.Networks = []
        c2 = 0
        while(c2<self.NpS):
            a = LL.DGN3layernet(self.Params[4],self.Params[0]*2,self.Params[3])
            self.Networks.append(a)
            c2 += 1

        self.Memory = LL.Memory(self.Params[6],self.Params[7])

        self.State = np.zeros(self.Params[4])

        self.t1s = []
        self.t0s = []
        self.pRes = []
        self.Res = []
        self.postMstates = []
        self.Personality = Personality
    def InputUpdate(self,inp):
        self.State[:self.Params[5]] = inp
    def GetMutableState(self):
        return self.State[self.Params[5]+self.Params[6]:]
    def SetMutableState(self,inp):
        self.State[self.Params[5]+self.Params[6]:] = inp
    def StateUpdate(self):
        data = self.State
        c2 = 0
        t1 = []
        t0 = []
        while(c2<self.NpS):
            v = self.Networks[c2].Forward(data)
            t1.append(v[:self.Params[0]])
            t0.append(v[self.Params[0]:])
            c2 += 1
        Plist = self.Personality
        means = np.sum(t1,axis = 0)/len(t1)
        mins = np.nanmin(t1,axis = 0)
        maxs = np.nanmax(t1,axis = 0)
        scrs1 = (Plist[0]*mins)+(Plist[1]*means)+(Plist[2]*maxs)
        pRe1 = means
        means = np.sum(t0,axis = 0)/len(t0)
        mins = np.nanmin(t0,axis = 0)
        maxs = np.nanmax(t0,axis = 0)
        scrs0 = (Plist[0]*mins)+(Plist[1]*means)+(Plist[2]*maxs)
        pRe0 = means
        self.SetMutableState(scrs1 > scrs0)
        mstate = self.GetMutableState()
        pRe = ((mstate*pRe1)+((1-mstate)*pRe0))/len(mstate)
        return t1,t0,pRe1,pRe0,pRe
    def SetMemory(self,v):
        self.State[self.Params[5]:self.Params[5]+self.Params[6]] = v
    def getMemoryVec(self):
        return self.State[self.Params[5]+(2*self.Params[6]):self.Params[5]+(3*self.Params[6])]
    def MemoryUpdate(self):
        key = self.State[self.Params[5]+self.Params[6]:self.Params[5]+2*self.Params[6]]
        mode = self.State[-1]
        mode = (mode/2)+1
        if(mode>1):
            mode = 1
        elif(mode<0):
            mode = 0
        rec = self.Memory.Recall(key,mode)
        self.SetMemory(rec)
        self.Memory.Enter(self.getMemoryVec())
    def Backprop(self,preMstate,t1,t0,postMstate,re,L):
        c = 0
        t1 = np.array(t1)
        t0 = np.array(t0)
        Mstate = self.GetMutableState()
        t1DeDo = ((t1-re)*Mstate)
        t0DeDo = ((t0-re)*(1-Mstate))
        DeDos = np.concatenate((t1DeDo,t0DeDo),axis = 1)
      #  print(np.shape(DeDos))
        c2 = 0
        self.LsP = np.array(self.LsP)
        while(c2<self.NpS):
            #print(np.shape(re))
            #print(np.shape(L))
            #print(np.shape(self.LsP))
            learn = L*((self.LsP[0,c2]*re)+self.LsP[1,c2])
           # print(np.shape(learn))
            self.Networks[c2].Backward(DeDos[c2],preMstate,learn)
            c2 += 1
        
                
    def Update(self,Obs,re,null,gamma,learn,MAX,dist,override,supr,imitate,negRe):
        self.InputUpdate(Obs)
        b = self.State
        t1,t0,pRe1,pRe0,pRe = self.StateUpdate()
        if(null):
            re = np.sum(pRe)/len(pRe)
            if(supr):
                if(imitate):
                    self.SetOutput(override)
                    self.Backprop(b,t1,t0,self.State,re,learn)
                    self.Backprop(b,t1,t0,1-self.State,negRe,learn)
                else:
                    self.SetOutput(override)
        self.postMstates.append(self.State)
        self.MemoryUpdate()
        self.t1s.append(t1)
        self.t0s.append(t0)
        self.pRes.append(pRe)
        self.Res.append(re)
        if(len(self.t1s)>MAX):
            self.t1s.pop(0)
            self.t0s.pop(0)
            self.pRes.pop(0)
            self.Res.pop(0)
            self.postMstates.pop(0)
        if(learn>0):
            tReC = re
            c = 1
            glearn = learn
            while((c<dist)&((c+1)<len(self.t1s))):
                tReC = tReC+self.Res[-c]
                glearn = glearn*gamma
                self.Backprop(self.postMstates[-(c+1)],self.t1s[-c],self.t0s[-c],self.postMstates[-c],tReC,glearn)
                c += 1
    def GetOutput(self):
        return self.State[(-1*self.Params[8])-1:-1]
    def SetOutput(self,v):
        self.State[(-1*self.Params[8])-1:-1] = v
    def Save(self):
        self.Memory.Save("LAGnet"+self.File)
        c = 0
        c2 = 0
        while(c2<self.NpS):
            ID = self.File+"LAGnet"+str(c2)
            self.Networks[c2].Save(ID)
            c2 += 1
    def Load(self):
        self.Memory.Load("LAGnet"+self.File)
        c = 0
        c2 = 0
        while(c2<self.NpS):
            ID = self.File+"LAGnet"+str(c2)
            self.Networks[c2].Load(ID)
            c2 += 1
    
        
        
        
        
