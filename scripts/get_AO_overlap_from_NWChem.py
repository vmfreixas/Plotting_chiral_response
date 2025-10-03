#   This function reads the standard output from NWChem and
# returns the atomic orbital overlaps. In the NWChem input the printing
# of the atomic orbital overlap matrix has to specified (i.e. 
# "BASIS "ao basis" SPHERICAL PRINT"). In the NWChem standard the
# atomic orbital overlaps are written under the label
# "global array: Temp Over".

import numpy as np

def get_AO_overlap_from_NWChem(fileName):
    import numpy as np
    with open(fileName, 'r') as nwFile:
        AO_block = False
        read = False
        i = -4
        for line in nwFile:
            if AO_block:
                i += 1
                if i == -2:
                    cols = np.fromstring(line, dtype=int, sep=" ")
                if i >= 0:
                    k = 0
                    for j in cols:
                        k += 1
                        ao[int(line.split()[0]) - 1, j - 1] = float(line.split()[k])
                    if int(line.split()[0]) == Nbf and cols[-1] == Nbf:
                        break
                if i == Nbf - 1:
                    i = -4
            if "global array: Temp Over" in line:
                AO_block = True
                Nbf = int(line.split(':')[2].split(',')[0])
                ao = np.zeros((Nbf, Nbf), dtype = float)
    return(ao)

