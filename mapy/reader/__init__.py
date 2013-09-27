import os
from cardtranslator import *
from input_reader import *
def user_setattr(obj, inputs):
    for k,v in inputs.iteritems():
        if k.find('blank') > -1:
            continue
        #FIXME I removed this if below...
        #if getattr(obj, k, False) == False:
        str_test = str( v )
        if str_test.find('.') > -1 and str_test.find('mapy.') == -1:
            try:
                setattr(obj, k, float( v ) )
            except:
                print 'Exception in mapy.reader.user_setattr...'
                print 'str_test is ', str_test
                print 'v is ', v
                setattr(obj, k, v )
        elif k.find('id') > -1:
            if v == None or v == '':
               setattr(obj, k, v ) 
            else:
                setattr(obj, k, int( v ))
        else:
            setattr(obj, k, v )
        #the if was finishing here before alteration

    return obj
