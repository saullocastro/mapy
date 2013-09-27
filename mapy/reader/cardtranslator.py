import mapy
from mapy.reader import *
from mapy.model import *
def card2dict(inputcard, inputsolvername, outputsolvername = 'generic'):            
    """
    Returns a tranlated output card, given the solver name and inputcard.
    If no output solver name is given the 'generic' one is used as default.
    """
    outputcard={}
    cardname = inputcard['card']
    trans = translator( inputsolvername )[1]
    outputcard['entryclass'] = trans[ cardname ]['entryclass']
    for oldkey in inputcard.keys():
        if oldkey.find('blank') > -1: continue
        newkey = trans[cardname][oldkey]
        outputcard[newkey] = inputcard[oldkey]
    if outputsolvername <> 'generic':
        inputcard = outputcard
        outputcard = {}
        cards = translator(outputsolvername)[0]
        trans = translator(outputsolvername)[1]
        for entry in cards[cardname]:
            if entry.find('blank') > -1: 
                outputcard[entry] = entry
                continue
            outputcard[entry]=inputcard[trans[cardname][entry]]
    return outputcard    

def translator(solvername):
    """
    Returns all configured cards and tranlator dictionary for a given 
    solver name.
    """
    if solvername.lower()=='nastran':
        cards={
            'CORD1R':['card','cida','g1a','g2a','g3a','cidb','g1b','g2b','g3b'],
            'CORD2R':['card','cid','rid','a1','a2','a3','b1','b2','b3','blank1',
              'blank2','c1','c2','c3'],
            'CORD1C':['card','cida','g1a','g2a','g3a','cidb','g1b','g2b','g3b'],
            'CORD2C':['card','cid','rid','a1','a2','a3','b1','b2','b3','blank1',
              'blank2','c1','c2','c3'],
            'CORD1S':['card','cida','g1a','g2a','g3a','cidb','g1b','g2b','g3b'],
            'CORD2S':['card','cid','rid','a1','a2','a3','b1','b2','b3','blank1',
              'blank2','c1','c2','c3'],
            'GRID':['card','id','cp','x1','x2','x3','cd','ps','seid'],
            'MAT1':['card','mid','e','g','nu','rho','a','tref','ge','blank1',
              'blank2','st','sc','ss','mcsid'],
            'MAT8':['card','mid','e1','e2','nu12','g12','g1z','g2z','rho','blank1',
              'blank2','a1','a2','tref','xt','xc','yt','yc','s','blank3',
              'blank4','ge','f12','strn'],
            'PROD':['card','pid','mid','a','j','c','nsm'],
            'CROD':['card','eid','pid','g1','g2'],
            'PBAR':['card','pid','mid','a','i1','i2','j','nsm','blank1',
              'blank2','blank3','c1','c2','d1','d2','e1','e2','f1','f2',
              'blank3','blank4','k1','k2','i12'],
            'CBAR':['card','eid','pid','ga','gb','x1','x2','x3','offt',
              'blank1','blank2','pa','pb','w1a','w2a','w3a',
              'w1b','w2b','w3b'],
            'PCOMP':['card','pid','z0','nsm','sb','ft','tref','ge','lam',
              'blank1', 'blank2','mid___list___2___4', 't___list___3___4',
              'theta___list___4___4'],
            'LOAD':['card','sid','s', 'scales___list___4___2',
              'loads___list___5___2'],
            'PSHELL':['card','pid','mid1','t','mid2','12i/t**3','mid3','ts/t',
              'nsm','blank1','blank2','z1','z2','mid4'],
            'CTRIA3':['card','eid','pid','g1','g2','g3','theta_or_mcid',
                'zoffs'],
            'CQUAD4':['card','eid','pid','g1','g2','g3','g4','theta_or_mcid',
                'zoffs'],
            'FORCE':['card','sid', 'g', 'cid', 'f', 'n1', 'n2', 'n3'],
            'FORCE1':['card','sid', 'g', 'f', 'g1', 'g2'],
            'MOMENT':['card','sid', 'g', 'cid', 'f', 'n1', 'n2', 'n3'],
            'SPC':['card','sid', 'g1', 'c1', 'd1', 'g2', 'c2', 'd2']
              }
        trans_out={
            'CORD1R':{'entryclass':mapy.model.coords.CoordR, 'card':'card',
                'cida':'ida', 'g1a':'g1a' ,'g2a':'g2a', 'g3a':'g3a',
                'cidb':'idb', 'g1b':'g1b', 'g2b':'g2b', 'g3b':'g3b'},
            'CORD2R':{'entryclass':mapy.model.coords.CoordR, 'card':'card',
                'cid':'id', 'rid':'rcid',
                'a1':'a1', 'a2':'a2', 'a3':'a3',
                'b1':'b1', 'b2':'b2', 'b3':'b3',
                'c1':'c1', 'c2':'c2', 'c3':'c3'},
            'CORD1C':{'entryclass':mapy.model.coords.CoordC, 'card':'card',
                'cida':'ida', 'g1a':'g1a' ,'g2a':'g2a', 'g3a':'g3a',
                'cidb':'idb', 'g1b':'g1b', 'g2b':'g2b', 'g3b':'g3b'},
            'CORD2C':{'entryclass':mapy.model.coords.CoordC, 'card':'card',
                'cid':'id', 'rid':'rcid',
                'a1':'a1', 'a2':'a2', 'a3':'a3',
                'b1':'b1', 'b2':'b2', 'b3':'b3',
                'c1':'c1', 'c2':'c2', 'c3':'c3'},
            'CORD1S':{'entryclass':mapy.model.coords.CoordS, 'card':'card',
                'cida':'ida', 'g1a':'g1a' ,'g2a':'g2a', 'g3a':'g3a',
                'cidb':'idb', 'g1b':'g1b', 'g2b':'g2b', 'g3b':'g3b'},
            'CORD2S':{'entryclass':mapy.model.coords.CoordS, 'card':'card',
                'cid':'id', 'rid':'rcid',
                'a1':'a1', 'a2':'a2', 'a3':'a3',
                'b1':'b1', 'b2':'b2', 'b3':'b3',
                'c1':'c1', 'c2':'c2', 'c3':'c3'},
            'GRID':{'entryclass':mapy.model.grids.Grid, 'card':'card', 'id':'id',
                'cp':'rcid', 'x1':'x1' ,'x2':'x2', 'x3':'x3',
                'cd':'ocid', 'ps':'perm_cons', 'seid':'seid'},
            'MAT1':{'entryclass':mapy.model.materials.matiso.MatIso, 
                'card':'card', 'mid':'id', 'e':'e', 'g':'g', 'nu':'nu',
                'rho':'rho', 'a':'a', 'tref':'tref', 
                'ge':'damp', 'st':'st', 'sc':'sc', 'ss':'ss',
                'mcsid':'mcsid'},
            'MAT8':{'entryclass':mapy.model.materials.matiso.MatLamina, 
                'card':'card', 'mid':'id', 'e1':'e1', 'e2':'e2', 'nu12':'nu12',
                'g12':'g12', 'g1z':'g13', 'g2z':'g23', 'rho':'rho',
                'a1':'a1', 'a2':'a2', 'a3':'a3', 'tref':'tref',
                'xt':'st1', 'xc':'sc1', 'yt':'st2', 'yc':'sc2', 's':'ss12',
                'ge':'damp', 'f12':'NOT', 'strn':'strn' },
            'PROD':{'entryclass':mapy.model.properties.prop1d.PropRod, 
                'card':'card', 'pid':'id', 'mid':'mid', 'a':'a', 'j':'j',
                'c':'c', 'nsm':'nsm'},
            'CROD':{'entryclass':mapy.model.elements.elem1d.ElemRod, 
                'card':'card', 'eid':'id', 'pid':'pid', 'g1':'g1', 'g2':'g2'},
            'PBAR':{'entryclass':mapy.model.properties.prop1d.PropBar,
                'card':'card', 'pid':'id', 'mid':'mid', 'a':'a', 'i1':'i1',
                'i2':'i2', 'i12':'i12', 'j':'j', 'nsm':'nsm', 'c1':'a1', 
                'd1':'a2', 'e1':'a3', 'f1':'a4', 'c2':'b1', 'd2':'b2', 
                'e2':'b3', 'f2':'b4', 'k1':'ka', 'k2':'kb'},
            'CBAR':{'entryclass':mapy.model.elements.elem1d.ElemBar,
                'card':'card', 'eid':'id', 'pid':'pid', 'ga':'g1', 'gb':'g2',
                'x1':'x1', 'x2':'x2', 'x3':'x3', 'offt':'offt','pa':'pa',
                'pb':'pb', 'w1a':'w1a', 'w2a':'w2a', 'w3a':'w3a', 'w1b':'w1b',
                'w2b':'w2b', 'w3b':'w3b'},
            'PCOMP':{'entryclass':mapy.model.properties.prop2d.PropShellComp,
                 'card':'card', 'pid':'id', 'z0':'z0',
                 'nsm':'nsm', 'sb':'sbmat', 'ft':'ft',
                 'tref':'tref', 'ge':'dampc', 'lam':'lam', 
                 'mid___list___2___4':'midlist', 't___list___3___4':'tlist',
                 'theta___list___4___4':'thetalist'},
            'LOAD':{'entryclass':mapy.model.loads.Load, 'card':'card', 
                'sid':'id', 's':'scale_overall', 
                'scales___list___4___2':'scales',
                'loads___list___5___2':'loads'},
            'PSHELL':{'entryclass':mapy.model.properties.prop2d.PropShell, 
                'card':'card', 'pid':'id', 'mid1':'mid', 't':'t', 
                'mid2':'mid2', '12i/t**3':'12i/t**3', 'mid3':'mid3',
                'ts/t':'ts/t', 'nsm':'nsm', 'z1':'fiberdistbot', 
                'z2':'fiberdisttop'},
            'CTRIA3':{'entryclass':mapy.model.elements.elem2d.ElemTria3,
                'card':'card', 'eid':'id', 'pid':'pid', 'g1':'g1', 'g2':'g2',
                'g3':'g3', 'theta_or_mcid':'theta_or_mcid', 'zoffs':'zoffs'},
            'CQUAD4':{'entryclass':mapy.model.elements.elem2d.ElemQuad4, 
                'card':'card', 'eid':'id', 'pid':'pid', 'g1':'g1', 'g2':'g2',
                'g3':'g3', 'g4':'g4', 'theta_or_mcid':'theta_or_mcid', 
                'zoffs':'zoffs'},
            'FORCE':{'entryclass':mapy.model.loads.Force, 'card':'card', 
                'sid':'id', 'g':'gridid', 'cid':'cid', 'f':'f', 'n1':'x1',
                'n2':'x2', 'n3':'x3'},
            'FORCE1':{'entryclass':mapy.model.loads.Force, 'card':'card',
                'sid':'id', 'g':'gridid', 'f':'f', 'g1id':'g1id',
                'g2id':'g2id'},
            'MOMENT':{'entryclass':mapy.model.loads.Moment, 'card':'card', 
                'sid':'id', 'g':'gridid', 'cid':'cid', 'f':'f', 'n1':'x1',
                'n2':'x2', 'n3':'x3'},\
            'SPC':{'entryclass':mapy.model.constraints.SPC, 'card':'card', 
                'sid':'id', 'g1':'gridid', 'c1':'dof', 'd1':'displ',
                'g2':'g2', 'c2':'c2', 'd2':'d2' }
            }
    return [cards, trans_out]
       
