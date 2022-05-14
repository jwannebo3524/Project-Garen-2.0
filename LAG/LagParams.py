import numpy as np
class Params:
    def __init__(self):
        inpL = 1950
        STATELEN = inpL+100+30
        self.p = [100,3,10,3,STATELEN,inpL,30,5000,27]
        self.Lp = [[1,0,-1],[1,1,1]]
        self.Pe = [2,2,1]
        self.aD = [16,4,2]
        self.aF = [20,45,65]
        self.aS = [16,4,2]
        self.g = 0.975
        
