#
#   This function reads a '.data' file a returns the CI vector as a
# Nocc x Nvir matrix for a given root. The '.data' file is generated
# by a Fortran script that reads the binary '.civecs' files generated
# by NWChem.
#

import numpy as np

def get_civecs_from_data(fileName, root):
    matrix = []
    with open(fileName, 'r') as dataFile:
        ciBlock = False
        read = False
        i = 0
        for line in dataFile:
            if read:
                i += 1
                row = [float(x) for x in line.split()]
                matrix.append(row)
                if i == Nocc:
                    return np.array(matrix)
            if 'Root' in line and int(line.split()[1]) == root:
                ciBlock = True
            if ciBlock and 'Nocc' in line:
                Nocc = int(line.split()[1])
            if ciBlock and 'Nvir' in line:
                Nvir = int(line.split()[1])
                read = True 

fileName = 'civecs.data'
root = 1
civec = get_civecs_from_data(fileName, 19)
np.savetxt('civec_1.txt', civec, fmt = '%.8f')

