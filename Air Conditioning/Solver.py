import meta
import AirConditioning
import Template
# to do the solving bit. i decided to seperate it to make more organized.

class Solver:
    def __init__(self,AirConditioner):
        self.AC = AirConditioner
    def BuildHierarchy(self,struct):
        ac = self.AC
        outsyms = []
        out = Template.symbol
        c = 0
        while(c<len(struct.Symbols)):
            s = struct.Symbols[c]
            try:
                z = ac.M.getClass(s)
                try:
                    KnownSupers = z.SUPERS
                    outsyms.append(KnownSupers)  #NEEDS DOWNCHAINING TO WORK PROPERLY - don't forget. wait no doesn't need it, but could be good?
                except:
                    ac.ComputeQue.append(["fINDsUPERS",s,0.5])
            except:
                print("<-SYSTEM-> OMG WTF ARE YOU DOING NO. [symbol not found solver.buildHierarchy()]")
            c += 1
        out.Symbols = outsyms
        return out

    def AttemptAnalogy(self,struct1,struct2):
        S1 = self.BuildHierarchy(struct1)
        S2 = self.BuildHierarchy(struct2)
        #########FFFFFFFFFFFFFFFUUUUUUUUUUUUCCCCCCCCCCCKKKKKKKKKKKKKKKK

        #im doing this wrong.

