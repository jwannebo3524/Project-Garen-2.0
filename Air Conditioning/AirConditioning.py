import meta
#not done at all
#To handle complexity symbolicly and flexibly
class AirConditioning:
    def __init__(self,directory="auto"):
        self.directory = directory
        self.M = meta.meta(directory)
        z = self.M.getClass("Library")   #make sure there is a 'library' file, to hold structures. If not, create one.
        if(z==False):
            self.M.writeBlank("Library")
    def Retrive2Coincidences(self,struct):
        potentialStructs = []
        anchors = []
        c = 0
        while(c<len(struct.Symbols)):
            z = self.M.getClass(struct.Symbols[c])
            try:
                assert z == False
                print("<-SYSTEM ERROR-> Nonexistant symbol in struct sent to ForwardChain()")
            except:
                c2 = c+1
                while(c2<len(struct.Symbols)):
                    try:
                        structures = getattr(z,"ConincidencesWith"+struct.Symbols[c2])
                        potentialStructs.append(structures)
                        anchors.append([struct.Symbols[c],struct.Symbols[c2]])
                    except:
                        pass
                    c2 += 1
        return potentialStructs    #keep in mind classes- subsets of symbols- symbols too? - assosciations between them - use classes to generalize easier. Don't forget repeated relations/ substitution proceure!!!
    def Embed2Coincidences(self,struct):
        