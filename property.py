import string
from parser.qe_io_dict import *

from setting import Setting

class Property(Setting):
    def __init__(self, fname=None):
        Setting.__init__(self, fname)

    def getTotalEnergy(self):
        'Extract total energy value from pwscf output'
        #read Espresso output into memory:
        pwscfOut = read_file(self.pwscfOutput)
        key = find_key_from_marker_string(pwscfOut, '!', 'total energy')
        words = string.split(pwscfOut[key])
        return [float(words[4])]
    
    def getSinglePhonon(self):
        'Obtain a list of phonon modes from output generated by dynmat.x'
        dynmatOut = read_file(self.dynmatOutput)
        keyStart = find_key_from_marker_string(dynmatOut, '#', 'mode')
        modeNum = 1
        key = keyStart + 1
        words = string.split(dynmatOut[key])
        modes = []
        while words[0]	 == str(modeNum):
            modes.append( float(words[1]) )
            key = key + 1
            modeNum = modeNum + 1
            words = string.split(dynmatOut[key])
        return modes
        
    def getLatticeParameters(self):
        'Extract lattice parameters after pwscf geometry optimization'
        def vectorLength(v):
            from math import sqrt
            s = 0.0
            for val in v: s = s + val**2
            return sqrt( s )
        pwscfOut = read_file(self.pwscfOutput)
        key_a_0 = find_key_from_string(pwscfOut, 'lattice parameter (a_0)')
        a_0 = float( string.split( pwscfOut[key_a_0] )[4] )
        keyEnd = max( find_all_keys_from_marker_string(pwscfOut, '!', 'total energy') )
        keyCellPar = find_key_from_string_afterkey(pwscfOut, keyEnd, \
                                                  'CELL_PARAMETERS (alat)') + 1
        a =  vectorLength( [ float(valstr) for valstr in string.split( pwscfOut[keyCellPar] ) ] )
        b =  vectorLength( [ float(valstr) for valstr in string.split( pwscfOut[keyCellPar+1] ) ] )
        c =  vectorLength( [ float(valstr) for valstr in string.split( pwscfOut[keyCellPar+2] ) ] )                
        return [a*a_0, b*a_0, c*a_0]
        
    def getMultiPhonon(self):        
        ''' Obtain a list of phonon modes and eigen vectors from output generated \
             by matdyn.x'''
        from parser.matdyn import matdyn
        return matdyn( matdynModes )
     
