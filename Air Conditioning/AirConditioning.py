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
        self.ComputeQue = []
    def Retrive2Coincidences(self,struct):
        potentialStructs = []
        anchors = []
        c = 0
        while(c<len(struct.Symbols)):
            z = self.M.getClass(struct.Symbols[c])
            try:
                assert z == False
                print("<-SYSTEM ERROR-> Nonexistant symbol in struct sent to Retrive2Coincidences()")
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
        return potentialStructs,anchors    #keep in mind classes- subsets of symbols- symbols too? - assosciations between them - use classes to generalize easier. Don't forget repeated relations/ substitution proceure!!!
    def Embed2Coincidences(self,struct):
        library = self.M.getClass("Library")
        try:
            strid = getattr(library,"IDOF"+struct.Hash())
        except:
            self.M.writeAttribute("Library","IDOF"+struct.Hash(),getattr(library,"Last")+1)
            self.M.writeAttribute("Library","Last",getattr(library,"Last")+1)
        c = 0
        while(c<len(struct.Symbols)):
            z = self.M.getClass(struct.Symbols[c])
            try:
                assert z == False
                print("<-SYSTEM ERROR-> Nonexistant symbol in struct sent to Embed2Coincidences()")
            except:
                c2 = 0
                while(c2<len(struct.Symbols)):
                    try:
                        if(not c2 == c):
                            structures = getattr(z,"ConincidencesWith"+struct.Symbols[c2])
                            if not strid in structures:
                                self.M.writeAttribute(struct.Symbols[c],"ConincidencesWith"+struct.Symbols[c2],structures.append(strid))
                    except:
                        try:
                            self.M.writeAttribute(struct.Symbols[c],"ConincidencesWith"+struct.Symbols[c2],[strid])
                        except:
                            pass
                    c2 += 1

#UUUUUUUUUUUUUUUUUUUUGGGGGGGGGGGGGGGGGGGGGGGGGGGGGHHHHHHHHHHHHHHHHHHHHHHHHHH WHYYYYYYYYYYYYYYYY

