import time
def rebuild(self):
    #########################################################
    # Grid <--> CoordSys loops
    print time.ctime() + ' started  - rebuilding grids and coordsys'
    # first processing basic grids and coordsys 
    for grid in self.griddict.values():
        if grid.rcid == 0 or grid.rcid == '':
            grid.rebuild()
    loop = True
    if loop:
        all_done = 0
        while all_done < 3:
            all_done += 1 
            for grid in self.griddict.values():
                if not grid.rebuilded:
                    if grid.check_to_rebuild():    
                        grid.rebuild()
                        if all_done > 0:
                            all_done = 0
            for coord in self.coorddict.values():
                if not coord.rebuilded:
                    if coord.check_to_rebuild():
                        coord.rebuild()
                        if all_done > 0:
                            all_done = 0

    print time.ctime() + ' finished - rebuilding grids and coordsys'
    #########################################################
    for prop in self.propdict.values():
        prop.rebuild()
    print time.ctime() + ' finished - rebuilding properties'
    print time.ctime() + ' started  - rebuilding elements'
    for elem in self.elemdict.values():
        elem.rebuild()
    print time.ctime() + ' finished - rebuilding elements'
    print time.ctime() + ' started  - rebuilding subcases'
    for sub in self.subcases.values():
        sub.rebuild()
    print time.ctime() + ' finished - rebuilding subcases'
    print time.ctime() + ' started  - rebuilding load entities'
    for load in self.loaddict.values():
        load.rebuild()
        load.add2grid() 
    print time.ctime() + ' finished - rebuilding load entities'
    print time.ctime() + ' started  - rebuilding constraints'
    for cons in self.consdict.values():
        cons.add2grid(self)
    print time.ctime() + ' finished - rebuilding constraints'

