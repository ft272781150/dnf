# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
# Copyright 2004 Duke University
# Written by Seth Vidal

class TransactionData:
    """Data Structure designed to hold information on a yum Transaction Set"""
    def __init__(self):
        self.flags = []
        self.vsflags = []
        self.probFilterFlags = []
        self.root = '/'
        self.pkgdict = {} # key = pkgtup, val = list of TransactionMember obj
        self.debug = 0

    def __len__(self):
        return len(self.pkgdict.values())

    def debugprint(self, msg):
        if self.debug:
            print msg
    
    def getMembers(self, pkgtup):
        """takes a package tuple and returns all transaction members matching"""
        if pkgdict.has_key(pkgtup):
            return pkgdict[pkgtup]
        else:
            return []

    def matchNaevr(self, name=None, arch=None, epoch=None, ver=None, rel=None):
        """returns the list of packages matching the args above"""
        completelist = self.pkgdict.keys()
        removedict = {}
        returnlist = []
        returnmembers = []
        
        for pkgtup in completelist:
            (n, a, e, v, r) = pkgtup
            if name is not None:
                if name != n:
                    removedict[pkgtup] = 1
                    continue
            if arch is not None:
                if arch != a:
                    removedict[pkgtup] = 1
                    continue
            if epoch is not None:
                if epoch != e:
                    removedict[pkgtup] = 1
                    continue
            if ver is not None:
                if ver != v:
                    removedict[pkgtup] = 1
                    continue
            if rel is not None:
                if rel != r:
                    removedict[pkgtup] = 1
                    continue
        
        for pkgtup in completelist:
            if not removedict.has_key(pkgtup):
                returnlist.append(pkgtup)
        
        for matched in returnlist:
            returnmembers.extend(self.pkgdict[matched])

        return returnmembers

    def add(self, txmember):
        """add a package to the transaction"""
        if not self.pkgdict.has_key(txmember.pkgtup):
            self.pkgdict[txmember.pkgtup] = []
        else:
            self.debugprint("Package: %s already in ts" % txmember.pkgtup)
        self.pkgdict[txmember.pkgtup].append(txmember)

    def remove(self, pkgtup):
        """remove a package from the transaction"""
    
    def exists(self, pkgtup):
        """tells if the pkg is in the class"""
        if self.pkgdict.has_key(pkgtup):
            if len(self.pkgdict[pkgtup]) != 0:
                return 1
        
        return 0
    
    def addInstall(self, po):
        """adds a package as an install but in mode 'u' to the ts
           takes a packages object and returns a TransactionMember Object"""
    
        txmbr = TransactionMember()
        txmbr.pkgtup = po.pkgtup()
        txmbr.current_state = 'repo'
        txmbr.output_state = 'i'
        txmbr.ts_state = 'u'
        txmbr.reason = 'user'
        txmbr.name = po.name
        txmbr.arch = po.arch
        txmbr.epoch = po.epoch
        txmbr.ver = po.ver
        txmbr.rel = po.rel
        txmbr.pkgid = po.pkgid
        txmbr.repoid = po.repoid
        self.add(txmbr)
        return txmbr

    def addTrueInstall(self, po)
        """adds a package as an install
           takes a packages object and returns a TransactionMember Object"""
    
        txmbr = TransactionMember()
        txmbr.pkgtup = po.pkgtup()
        txmbr.current_state = 'repo'
        txmbr.output_state = 'i'
        txmbr.ts_state = 'i'
        txmbr.reason = 'user'
        txmbr.name = po.name
        txmbr.arch = po.arch
        txmbr.epoch = po.epoch
        txmbr.ver = po.ver
        txmbr.rel = po.rel
        txmbr.pkgid = po.pkgid
        txmbr.repoid = po.repoid
        self.add(txmbr)
        return txmbr
    

    def addErase(self, po):
        """adds a package as an erasure
           takes a packages object and returns a TransactionMember Object"""
    
        txmbr = TransactionMember()
        txmbr.pkgtup = po.pkgtup()
        txmbr.current_state = 'installed'
        txmbr.output_state = 'e'
        txmbr.ts_state = 'e'
        txmbr.name = po.name
        txmbr.arch = po.arch
        txmbr.epoch = po.epoch
        txmbr.ver = po.ver
        txmbr.rel = po.rel
        txmbr.pkgid = po.pkgid
        txmbr.repoid = po.repoid
        self.add(txmbr)
        return txmbr

    def addUpdate(self, po, oldpo):
        """adds a package as an update
           takes a packages object and returns a TransactionMember Object"""
    
        txmbr = TransactionMember()
        txmbr.pkgtup = po.pkgtup()
        txmbr.current_state = 'repo'
        txmbr.output_state = 'u'
        txmbr.ts_state = 'i'
        txmbr.name = po.name
        txmbr.arch = po.arch
        txmbr.epoch = po.epoch
        txmbr.ver = po.ver
        txmbr.rel = po.rel
        txmbr.pkgid = po.pkgid
        txmbr.repoid = po.repoid
        txmbr.relatedto.append((oldpo.pkgtup(), 'updates'))
        self.add(txmbr)
        return txmbr

    def addObsolete(self, po, oldpo):
        """adds a package as an obsolete
           takes a packages object and returns a TransactionMember Object"""
    
        txmbr = TransactionMember()
        txmbr.pkgtup = po.pkgtup()
        txmbr.current_state = 'repo'
        txmbr.output_state = 'o'
        txmbr.ts_state = 'u'
        txmbr.name = po.name
        txmbr.arch = po.arch
        txmbr.epoch = po.epoch
        txmbr.ver = po.ver
        txmbr.rel = po.rel
        txmbr.pkgid = po.pkgid
        txmbr.repoid = po.repoid
        txmbr.relatedto.append((oldpo.pkgtup(), 'obsoletes'))
        self.add(txmbr)
        return txmbr



class TransactionMember:
    """Class to describe a Transaction Member (a pkg to be installed/
       updated/erased)."""
    
    def __init__(self):
        # holders for data
        self.pkgtup = None # package tuple
        self.current_state = None # where the package currently is (repo, installed)
        self.ts_state = None # what state to put it into in the transaction set
        self.output_state = None # what state to list if printing it
        self.isDep = 0
        self.reason = None # reason for it to be in the transaction set
        self.repoid = None # repository id (if any)
        self.name = None
        self.arch = None
        self.epoch = None
        self.ver = None
        self.rel = None
        self.process = None # 
        self.relatedto = [] # ([relatedpkgtup, relationship)]
        self.groups = [] # groups it's in
        self.pkgid = None # pkgid from the package, if it has one, so we can find it
        self.repoid = None
    
    def setAsDep(self, pkgtup):
        """sets the transaction member as a dependency and maps the dep into the
           relationship list attribute"""
        
        self.isDep = 1
        self.relatedto.append((pkgtup, 'dependson'))


    # This is the tricky part - how do we nicely setup all this data w/o going insane
    # we could make the txmember object be created from a YumPackage base object
    # we still may need to pass in 'groups', 'ts_state', 'output_state', 'reason', 'current_state'
    # and any related packages. A world of fun that will be, you betcha
    
    
    # things to define:
    # types of relationships
    # types of reasons
    # ts, current and output states
    
    # output states are:
    # update, install, remove, obsoleted
    
    # ts states are: u, i, e
    
    # current_states are:
    # installed, repo
    
    #relationships:
    # obsoletedby, updates, obsoletes, updatedby, 
    # dependencyof, dependson
    
