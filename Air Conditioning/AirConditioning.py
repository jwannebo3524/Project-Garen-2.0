import meta
#not done at all
#To handle complexity symbolicly and flexibly
class AirConditioning:
    def __init__(self,directory="auto"):
        self.directory = directory
        self.M = meta.meta(directory)
    def ForwardChain(struct): #built for unordered structs, possibly with subordered stuff but not necessarily. For prediction
        c = 0
        while(c<len(struct.Symbols)):
            z = meta.meta.getClass(struct.Symbols[c])
            try:
                assert z == False
                print("<-SYSTEM ERROR-> Nonexistant symbol in struct sent to ForwardChain()")
            except:
                pass
            c2 = 0
            while(c2<len(struct.Symbols)):
                if(z.