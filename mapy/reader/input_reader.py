import mapy
from mapy.reader import *
global tempcard
def addfield(tempcard, field, value):
    found = False	
    field = float(field)
    field += 1
    for k in tempcard.keys():
        if k.find('___') > -1:
            entrynum = float(k.split('___')[2])
            step = float(k.split('___')[3])
            found = False
            if (field - entrynum)/step == 0 or (field - entrynum)/step == 1:
                found = True
                tempcard[k].append(value)    
                break
def fieldsnum(line):
    if line.find(',') == -1:
        line = line.split('\n')[0]
        num = len(line)/8
        # the operator below gived the rest of the division
        if len(line) % 8. > 0.:
            num = num + 1
    else:
        num = len(line.split(','))
    return num

class InputFile:
    """ 
    Input file containing a FEM model bulk

    """
    def __init__(self, abspath, solvername='nastran'):
        self.abspath = abspath
        self.solvername = solvername
        list_cards_translator = translator( self.solvername )
        self.cards = list_cards_translator[0]
        self.translator = list_cards_translator[1]
        self.readfile()
        self.createdata()
        self.memorycleanup()

    def readfile(self):
        if os.path.isfile(self.abspath):
            datfile = open(self.abspath, 'r')
        else:
            raise 'Input file : %s was not found!' % self.abspath
        self.lines = datfile.readlines()
        datfile.close()

    def memorycleanup(self):
        self.lines = None

    def createdata(self):
        #
        self.data = [] 
        #
        for i in range(len(self.lines)):
            line = self.lines[i]
            if line.strip()[0] == '$':
                continue
            if line.find(',') > -1:
                numfields = fieldsnum(line)
                fields = [i.strip() for i in line.split(',')]
            else:
                numfields = fieldsnum(line)
                fields = [line[(0 + i * 8):(8 + i * 8)].strip()\
		         		  for i in range(numfields)]
            if (fields[0].find('+') > -1 or fields[0] == '' or \
                fields[0] == '        ') and validentry == True:
                countentry += 1
            elif fields[0] in self.cards:
                validentry = True
                countentry = 0
                currcard = fields[0]
                cardfieldsnum = len(self.cards[currcard])
                try: 
                    if len(tempcard) > 0: 
                        self.data.append(tempcard)    
                except NameError:
                    pass
                tempcard = {}
                listentries = None
            else:
                validentry = False
                countentry = 0
            if validentry == True or countentry > 0:
                blanknum = 10 - numfields
                for field_i in range(numfields):
                    field_j = field_i + 10 * countentry  			
                    fieldvalue = fields[field_i] 
                    if (field_j + 1) <= cardfieldsnum:
                        fieldname = self.cards[currcard][field_j] 
                        if fieldname.find('___') > -1:    
                            tempcard[fieldname] = [fieldvalue]
                        else:    
                            tempcard[fieldname] = fieldvalue
                    else:
                        addfield(tempcard, field_i, fieldvalue)
                
                #FIXME the for below was commented because it aimed to blank the
                #fields... they are simply ignored in the
                #mapy.reader.user_setattr method, using the given 'blank' flag
                #for blank_field_i in range(blanknum):
                #    tmp = blank_field_i + numfields
                #    if (tmp + 1) <= cardfieldsnum:
                #        tempcard[self.cards[currcard][tmp]] = ''
        try: 
            if len(tempcard) > 0: 
                self.data.append(tempcard)    
        except NameError:
            pass
