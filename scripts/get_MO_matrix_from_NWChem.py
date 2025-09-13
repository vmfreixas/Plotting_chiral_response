#   This subroutines reads the molecular orbital matrix from NWChem
# standard output.

import numpy as np

def get_MO_matrix_from_NWChem(fileName, channel = 'alpha'):
    with open(fileName, 'r') as nwFile:
        alpha = False
        beta = False
        done = False
        for line in nwFile:
            if (channel == 'alpha' and alpha) or (channel == 'beta' and beta):
                i += 1
                if i == -2:
                    columns = list(map(int, line.split()))
                if i >= 0:
                    k = 0
                    for j in columns:
                        k += 1
                        MO[int(line.split()[0]) - 1, j - 1] = float(line.split()[k])
                        if(int(line.split()[0]) == Nbf and j == Nbf):
                            done = True
                if done:
                    return(MO)
                if i == Nbf - 1:
                    i = -4
            if 'global array: MO eigenvectors' in line:
                Nbf = int(line.split(':')[2].split(',')[0])
                MO = np.zeros((Nbf, Nbf), dtype = float)
                if alpha:
                    alpha = False
                    beta = True
                    i = -4
                if not(alpha):
                    alpha = True
                    i = -4
    print('"get_MO_matrix_from_NWChem" error: MO block not found!')
