import numpy as np
#from numba import jit

class MatrixOperations:
    #@jit(nopython=True)
    def mvSub(m,v):
        c = 0
        o = []
        while(c<len(m)):
            o.append(m[c]-v)
            c += 1
        return o
   # @jit(nopython=True)
    def mvMult(m,v):
        c = 0
        o = []
        while(c<len(m)):
            o.append(np.multiply(m[c],v))
            c += 1
        return o
  #  @jit(nopython=True)
    def mvMult2(m,v):
        c = 0
        o = []
        while(c<len(m[0])):
            #print('!!')
            o.append(np.multiply(m[:,c],v))
            c += 1
        return o
   # @jit(nopython=True)
    def mvScalarMult2(m,v):
        c = 0
        o = []
        while(c<len(m)):
            c2 = 0
            partial = []
            while(c2<len(m[0])):
                partial.append(np.multiply(m[c,c2],v[c,c2]))
                c2 += 1
            o.append(partial)
            c += 1
        return o
   # @jit(nopython=True)
    def mvScalarMult(m,v):
        c = 0
        o = []
        while(c<len(m)):
            o.append(np.multiply(m[c],v[c]))
            c += 1
        return o
            
