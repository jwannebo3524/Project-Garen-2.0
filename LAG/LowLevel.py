import numpy as np
from MOpack import MatrixOperations as MO
#from numba import jit
class DGNlayer:
    def __init__(self,inlen,outlen,branches):
        self.NM = ((2*np.random.random((outlen,branches,inlen+1)))-1) #weights
        self.INM = ((2*np.random.random((outlen,branches,inlen+1)))-1) #inhibitory neurons
        self.BMs = (2*np.random.random((outlen,branches)))-1 #minimums for branch activation
    def Forward(self,inp):
        #print(np.shape(inp))
        inp = np.concatenate((inp,[1]))
        c = 0
        o = []
        #while(c<len(self.NM)):
       # print(np.shape(self.INM))
        vals = MO.mvMult2(self.INM,inp)
        #print("yee")
        #print(np.shape(vals))
        zss = np.sum(vals,axis = 2)
        zss = np.transpose(zss,(1,0))
       # print(np.shape(zss))
        Actives = (zss >= self.BMs)
       # print('1')
        ws = np.sum(MO.mvScalarMult2(self.NM,Actives),axis = 1)
       # print('2')
            #print(np.shape(ws))
        o = np.sum(MO.mvMult(ws,inp),axis = 1)
            #c += 1
        self.NM = np.nan_to_num(self.NM)
        return np.nan_to_num(np.array(o))
    def Backward(self,DeDos,inp,L):
        inp = np.concatenate((inp,[1]))
        c = 0
        o = []
        while(c<len(self.NM)):
            DeDo = DeDos[c]
            self.Backprop(DeDo,c,inp,L)
            c += 1
    def Backprop(self,DeDo,z,inp,L):
        #DeDo*DoDw = DeDw
        #DoDw = I*g
        Actives = (np.sum(MO.mvMult(self.INM[z],inp),axis = 1) >= self.BMs[z])
       # print(np.shape(Actives))
        #print(np.shape(DeDo))
       # print(DeDo)
       # print(np.shape(DeDo))
        DeDw = np.outer((DeDo*Actives),inp)
       # print(np.shape(self.NM[z]))
        #print(np.shape(L))
        self.NM[z] += np.nan_to_num(-1*L*DeDw)
    def Save(self,file):
        np.save(file+"DgnNm.npy",self.NM)
        np.save(file+"DgnInm.npy",self.INM)
        np.save(file+"DgnBms.npy",self.BMs)
    def Load(self,file):
        self.NM = np.load(file+"DgnNm.npy")
        self.INM = np.load(file+"DgnInm.npy")
        self.BMs = np.load(file+"DgnBms.npy")

        
class DGN3layernet:
    def __init__(self,inlen,outlen,branches):
        hlen = outlen #otherwise backprop fails
        self.One = DGNlayer(inlen,hlen,branches)
        self.Two = DGNlayer(hlen,hlen,branches)
        self.Three = DGNlayer(hlen,outlen,branches)
    def Forward(self,inp):
        o1 = self.One.Forward(inp)
        o2 = self.Two.Forward(o1)
        o3 = self.Three.Forward(o2)
        return o3
    def Backward(self,DeDos,inp,L):
        o1 = self.One.Forward(inp)
        o2 = self.Two.Forward(o1)
        #o3 = self.Three.Forward(o2)
        
        self.One.Backward(DeDos,inp,L)
        self.Two.Backward(DeDos,o1,L)
        self.Three.Backward(DeDos,o2,L)
    def Save(self,file):
        self.One.Save(file+"Layer1")
        self.Two.Save(file+"Layer2")
        self.Three.Save(file+"Layer3")
    def Load(self,file):
        self.One.Load(file+"Layer1")
        self.Two.Load(file+"Layer2")
        self.Three.Load(file+"Layer3")

class Memory:
    def __init__(self,vl,units):
        self.VL = vl
        self.Memory = np.zeros((units,vl))
        self.Allo = np.zeros(units)
        self.Timelike = np.zeros(units)
        self.LastInd = -1
        self.LastRecalls = np.zeros(units)
    def Enter(self,vector):
        z = np.argmin(self.Allo)
        self.Memory[z] = vector
        self.Allo[z] = 100
        self.Timelike[z] = self.LastInd
        if(z in self.Timelike):
            k, = np.where(self.Timelike==z)
            self.Timelike[k] = -1
        self.LastInd = z
    def GetTimelikePositions(self):
        li = self.LastRecalls
        out = np.zeros(len(self.LastRecalls))
        c = 0
        while(c<len(li)):
            out[int(self.Timelike[c])] += li[c]
            c += 1
        return out
    def Recall(self,key,C):
        sqdiffs = np.sum(np.power(MO.mvSub(self.Memory,key),2),axis = 1)
        wsqds = sqdiffs/np.sum(sqdiffs)
        timelikeList = self.GetTimelikePositions()
        weights = (wsqds*C) + (timelikeList*(1-C)) #fixed (?) - timelike not integrated correctly
        self.LastRecalls = weights
        recalled = np.sum(MO.mvScalarMult(self.Memory,weights),axis = 0)
        self.Allo += (weights-0.01)
        return recalled
    def Backwards(self,DeDos,out,Ws,key,C,DIFF,SUM): # diff is wsqds-timelikeList
        DeDms = np.outer(Ws,DeDos)
        DeDws = MO.mvMult(self.Memory,DeDos)
        DeDC = (DIFF)*DeDws
        DeDsqds = (1/SUM)*C*DeDws
        DeDti = (1-C)*DeDws
        DeDm = DeDsqrds*2*MO.mvSub(self.Memory,key)
        DeDk = np.sum(DeDm*(-1),axis = 0)
        return DeDC,DeDm,DeDk
    def Save(self,file):
        np.save(file+"MemMain.npy",self.Memory)
        np.save(file+"MemAllo.npy",self.Allo)
        np.save(file+"MemTimelike.npy",self.Timelike)
    def Load(self,file):
        self.Memory = np.load(file+"MemMain.npy")
        self.Allo = np.load(file+"MemAllo.npy")
        self.Timelike = np.load(file+"MemTimelike.npy")
        
class BasicNeuralLayer:
    def __init__(self,inlen,outlen):
        self.NM = ((2*np.random.random((outlen,inlen+1)))-1)
        self.DeDws = []
    def Sigmoid(self,v):
        return np.nan_to_num(np.exp(v)/(1+np.exp(v)))
    def Forward(self,inp):
        inp = np.nan_to_num(inp)
        self.NM = np.nan_to_num(self.NM)
        return self.Sigmoid(np.sum(MO.mvMult(self.NM,np.concatenate((inp,[1]))),axis = 1))
    def Backward(self,DeDo,inp,out):
        DeDo = DeDo*(1-out)*(out)
        inp = inp
        DoDw = self.NM
        DeDw = MO.mvScalarMult(DoDw,DeDo)
        self.DeDws.append(np.array(DeDw,dtype = np.float32))
        DeDi = np.sum(np.outer(DeDo,inp),axis = 0)
        return DeDi
    def Update(self,learn):
        avgDeDw = np.sum(self.DeDws,axis = 0)/len(self.DeDws)
        self.NM += np.nan_to_num((-1)*(learn)*avgDeDw)
        self.DeDws = []
    def Save(self,file):
        np.save(file+"BnlNm.npy",np.array(self.NM,dtype = np.float16))
    def Load(self,file):
        self.NM = np.array(np.load(file+"BnlNm.npy"),dtype = np.float64)

class Convo:
    def __init__(self,dim,dep,filts):
        self.Dim = dim
        self.Network = BasicNeuralLayer(dim*dim*dep,filts)
    def Forward(self,image,stride):
        print(np.shape(image))
        image = np.array(image)
        c = 0
        d = self.Dim
        out = []
        while(c+d<=len(image)):
            partial = []
            c2 = 0
            while(c2+d<=len(image[0])):
                data = np.array(image[c:c+d,c2:c2+d])
                data = data.flatten()
                partial.append(self.Network.Forward(data))
                c2 += stride
            out.append(partial)
            c += stride
        return out
    def Backward(self,image,stride,DeDos,aout):
        image = np.array(image)
        DeDos = np.array(DeDos)
        aout = np.array(aout)
        c = 0
        d = self.Dim
        out = np.zeros(np.shape(image))
        while(c+d<=len(image)):
            c2 = 0
            while(c2+d<=len(image[0])):
                data = np.array(image[c:c+d,c2:c2+d])
                datashape = np.shape(data)
                data = data.flatten()
                DeDi = self.Network.Backward(DeDos[int(c/stride),int(c2/stride)],data,aout[int(c/stride),int(c2/stride)])
                out[c:c+d,c2:c2+d] = np.reshape(DeDi,(datashape))
                c2 += stride
            c += stride
        return out

class Deconvo:
    def __init__(self,dim,dep,filts):
        self.Dim = dim
        self.Network = BasicNeuralLayer(filts,dim*dim*dep)
        self.Dep = dep
    def Forward(self,eximage,data,stride):
        c = 0
        d = self.Dim
        out = np.zeros(np.shape(eximage))
        while(c<len(data)):
            partial = []
            c2 = 0
            while(c2<len(data[0])):
                frame = np.reshape(self.Network.Forward(data[c][c2]),(self.Dim,self.Dim,self.Dep))
                out[(c*stride):(c*stride)+d,c2*stride:(c2*stride)+d] = frame
                c2 += 1
            c += 1
        print(np.shape(out))
        return out
    def Backward(self,data,stride,DeDos,aout):
        data = np.array(data)
        c = 0
        print(np.shape(DeDos))
        d = self.Dim
        out = np.zeros(np.shape(data))
        while(c<len(data)):
            c2 = 0
            while(c2<len(data[0])):
                dedos = np.array(DeDos[(c*stride):(c*stride)+d,c2*stride:(c2*stride)+d]).flatten()
                sout = np.array(aout[(c*stride):(c*stride)+d,c2*stride:(c2*stride)+d]).flatten()
                out[c][c2] = self.Network.Backward(dedos,data[c,c2],sout)
                c2 += 1
            c += 1
        return out

class VaribleWeightNeuralLayer:
    def __init__(self,inlen,olen,act):
        self.tNM = np.zeros((olen,inlen+1))
        self.Clen = (olen*(inlen+1))
        self.Activation = act.F
        self.BActi = act.B
    def Forward(self,inp,cont):
        inp = np.concatenate((inp,[1]))
        self.tNM = cont
        totals = MO.mvMult(self.tNM,inp)
        return self.Activation(totals)
    def Backward(self,DeDos,inp,out,cont):
        inp = np.concatenate((inp,[1]))
        DeDos = self.BActi(DeDos)
        DeDws = MO.mvScalarMult(cont,DeDos)
        DeDi = np.sum(np.outer(DeDos,inp),axis = 0)
        return DeDis[:-1],DeDws
    
            

                
