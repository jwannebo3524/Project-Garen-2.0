#work in progress this ones hard to explain
# Built like this to use hard drive instead of RAM, to handle a potentially excessively large symbol-stucture
import importlib
class meta:
    def __init__(self,directory = "auto"):
        self.path = __file__[:-7]+"/"+directory+"/"
        self.TemplateFile = "Template.py"
    def getClass(self,name): #shortcut for retreiving class associated with symbol given its name.
        z = False
        try: 
            z = importlib.import_module(self.path+name)
        except:
            pass
        return z
    def writeBlank(self,name): #write a blank class from template- for creating new symbols
        try:
            f = open(self.TemplateFile,mode='r')
            z = f.read()
            f.close()
            f = open(self.path+name,mode='w')
            f.write(z)
            f.close()
        except:
            print("<-SYSTEM ERROR-> Error encountered while copying template. In Meta.py, writeBlank()")
    def Repair(self,name): #repair a somehow damaged symbol-class. Can't fix everything, but if data is accidentaly uploaded wrong should help.
        try:
            z = self.getClass(name) #make sure class is reachable. if not make a new one.
        except:
            self.wrtieBlank(name)  
            z = self.getClass(name)

        f = open(self.path+name,'r')
        symfile = f.readlines()
        f.close()
        c = 0
        modifier = 0
        line = ""
        while not line == "#END": #go through each line and make sure every attribute has a locale attribute associated with it, and that that has the proper value.
            if not c == 0 and not line == "#END":
                try:
                    line = symfile[c]
                    x = line.split(" ")
                    try:
                        y = x[0]
                        try:
                            assert y[-6:] == "LOCALE"
                            try:
                                assert (not symfile[c+1][0][-6:] == "LOCALE") or (symfile[c+1] == "#END")
                            except:
                                symfile.pop(c+1)
                        except:
                            symfile.insert(c+1,"    "+y+"LOCALE = "+str(c)) #add proper locale
                    except:
                        symfile.pop(c) #remove unreadable lines
                            
                except:
                    symfile.insert(c,"#END")
                    line = "#END"
            c += 1
        f = open(self.path+name,'w')
        f.write("".join(symfile))
        f.close()
    def writeAttribute(self,name,attr,value): #hard- write to an attribute
        try:
            z = self.getClass(name)
            index = int(getattr(z,attr+"LOCALE"))
            
        except:
            try:
                s = getattr(z,attr)
                print("<-SYSTEM-> Nonfatal error: no locale associated with "+attr+" from "+name+".  Reparing...")
                self.Repair(name)
                print("<-SYSTEM-> Repair complete")
            except:
                f = open(self.path+name,'r')
                symfile = f.readlines()
                f.close()
                symfile.insert(-2,"    "+attr+" = "+str(value))
                symfile.insert(-2,"    "+attr+"LOCALE = "+str(len(symfile)-2))
                f = open(self.path+name,'w')
                f.write("".join(symfile))
                f.close()
class Struct: #class to hold data in nested lists with some extra attributes too. More will probably be added later to this class.
    def __init__(self,contents = None,Ordered = False,freq = 0,inLibrary=False):
        self.isStruct = True
        self.Ordered = Ordered
        self.Freq = freq
        self.data = []
        self.Symbols = []
        self.inLibrary=inLibrary        
        try:
            assert contents.isStruct == True
            self.data.append(contents)
            self.AddFrom(contents)
        except:
            try:
                assert len(contents) >= 0
                c = 0
                while(c<len(contents)):
                    self.AddFom(contents[c])
                    c += 1
                self.data = contents
            except:
                print("<-SYSTEM ERROR-> unrcognized data type added to Struct on init")
    def add(self,contents): #add sub struct
        try:
            assert contents.isStruct == True
            self.data.append(contents)
            self.AddFrom(contents)
        except:
            try:
                assert len(contents) >= 0
                c = 0
                while c<len(contents):
                    self.AddFom(contents[c])
                    self.data.append(contents[c])
                    c += 1
            except:
                print("<-SYSTEM ERROR-> attempt to add unrecognized data type to Struct")
    def AddFrom(self,struct):
        c = 0
        while(c<len(struct.Symbols)):
            self.Symbols.append(struct.Symbols) #repeats allowed for efficieny.
            c += 1
    def Hash(self):
        c = 0
        hdata = []
        while(c<len(self.data)):
            try:
                hdata.append(self.data[c].Hash())
            except:
                hdata.append(self.data[c]):
            c += 1
        return str(hdata)
            
        
class SymbolInstance: #idk i need to think about this one if its necessary or useful.
    def __substitutingFor