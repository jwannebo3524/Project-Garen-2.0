import numpy as np
from MOpack import MatrixOperations as MO
import LowLevel as LL

class ImageAutoEncoder4layer:
    def __init__(self,Dims,Filts,Strides):
        self.One = LL.Convo(Dims[0],3,Filts[0])
        self.Two = LL.Convo(Dims[1],Filts[0],Filts[1])
        self.Three = LL.Convo(Dims[2],Filts[1],Filts[2])
       # self.Four = LL.Convo(Dims[3],Filts[2],Filts[3])

       # self.Five = LL.Deconvo(Dims[3],Filts[2],Filts[3])
        self.Six = LL.Deconvo(Dims[2],Filts[1],Filts[2])
        self.Seven = LL.Deconvo(Dims[1],Filts[0],Filts[1])
        self.Eight = LL.Deconvo(Dims[0],3,Filts[0])
        self.Strides = Strides
    def ConvForward(self,image):
        #print(np.shape(image))
        Strides = self.Strides
        self.ExImage = image
        o1 = self.One.Forward(image,Strides[0])
        self.Exo1 = o1
        o2 = self.Two.Forward(o1,Strides[1])
        self.Exo2 = o2
        o3 = self.Three.Forward(o2,Strides[2])
        self.Exo3 = o3
        #o4 = self.Four.Forward(o3,Strides[3])
        #self.Exo4 = o4
        return o3
    def DeconvForward(self,data):
        Strides = self.Strides
        #d1 = self.Five.Forward(self.Exo3,data,Strides[3])
        #self.Ld1 = d1
        d2 = self.Six.Forward(self.Exo2,data,Strides[2])
        self.Ld2 = d2
        d3 = self.Seven.Forward(self.Exo1,d2,Strides[1])
        self.Ld3 = d3
        d4 = self.Eight.Forward(self.ExImage,d3,Strides[0])
        self.Ld4 = d4
        return d4
    def FullForward(self,image):
        o4 = self.ConvForward(image)
        out = self.DeconvForward(o4)
        return out
    def ConvBackward(self,DeDos):
        S = self.Strides
        #DeDos = self.Four.Backward(self.Exo3,S[3],DeDos,self.Exo4)
        DeDos = self.Three.Backward(self.Exo2,S[2],DeDos,self.Exo3)
        DeDos = self.Two.Backward(self.Exo1,S[1],DeDos,self.Exo2)
        DeDos = self.One.Backward(self.ExImage,S[0],DeDos,self.Exo1)
    def DeconvBackward(self,DeDos):
        S = self.Strides
        DeDos = self.Eight.Backward(self.Ld3,S[0],DeDos,self.Ld4)
        DeDos = self.Seven.Backward(self.Ld2,S[1],DeDos,self.Ld3)
        DeDos = self.Six.Backward(self.Exo3,S[2],DeDos,self.Ld2)
        #DeDos = self.Five.Backward(self.Exo4,S[3],DeDos,self.Ld1)
        return DeDos
    def Cycle(self,image):
        pred = self.FullForward(image)
        DeDos = (pred-image)
        err = np.sum(np.power(DeDos,2))
        DeDos = self.DeconvBackward(DeDos)
        self.ConvBackward(DeDos)
        return err
    def Update(self,learn):
        self.One.Network.Update(learn)
        self.Two.Network.Update(learn)
        self.Three.Network.Update(learn)
       # self.Four.Network.Update(learn)
        
       # self.Five.Network.Update(learn)
        self.Six.Network.Update(learn)
        self.Seven.Network.Update(learn)
        self.Eight.Network.Update(learn)
    def Save(self,file):
        self.One.Network.Save(file+"AutonetL1")
        self.Two.Network.Save(file+"AutonetL2")
        self.Three.Network.Save(file+"AutonetL3")
      #  self.Four.Network.Save(file+"AutonetL4")
        
       # self.Five.Network.Save(file+"AutonetL5")
        self.Six.Network.Save(file+"AutonetL6")
        self.Seven.Network.Save(file+"AutonetL7")
        self.Eight.Network.Save(file+"AutonetL8")
    def Load(self,file):
        self.One.Network.Load(file+"AutonetL1")
        self.Two.Network.Load(file+"AutonetL2")
        self.Three.Network.Load(file+"AutonetL3")
      #  self.Four.Network.Load(file+"AutonetL4")
        
     #   self.Five.Network.Load(file+"AutonetL5")
        self.Six.Network.Load(file+"AutonetL6")
        self.Seven.Network.Load(file+"AutonetL7")
        self.Eight.Network.Load(file+"AutonetL8")
    
        
