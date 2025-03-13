#
#  This function reads NWChem standard output (specially modified
# version of NWChem for this purpose) and returns the electric dipoles
# integral matrix for a given direction ('x', 'y', or 'z').
#

import numpy as np

def get_electric_dipole_from_NWChem(fileName, direction):
    with open(fileName, 'r') as nwFile:
        muBlock = False
        done = False
        for line in nwFile:
            if muBlock: 
                i += 1
                if i == -2: 
                    columns = list(map(int, line.split()))
                if i >= 0:
                    k = 0 
                    for j in columns:
                        k += 1
                        mu[int(line.split()[0]) - 1, j - 1] = float(line.split()[k])
                        if(int(line.split()[0]) == Nbf and j == Nbf):
                            done = True
                if done:
                    return(mu)
                if i > 0:
                    if i == Nbf - 1:
                        i = -4
                if 'global array: g_dipole' in line:
                    Nbf = int(line.split(':')[2].split(',')[0])
                    mu = np.zeros((Nbf, Nbf), dtype = float)
            if 'mu_' + direction in line:
                muBlock = True
                i = -6

filename = 'plot.out'
direction = 'x'
mu_x = get_electric_dipole_from_NWChem(filename, direction)
np.savetxt('mu_x.txt', mu_x, fmt = '%.8f')

filename = 'plot.out'
direction = 'y'
mu_y = get_electric_dipole_from_NWChem(filename, direction)
np.savetxt('mu_y.txt', mu_y, fmt = '%.8f')


filename = 'plot.out'
direction = 'z'
mu_z = get_electric_dipole_from_NWChem(filename, direction)
np.savetxt('mu_z.txt', mu_z, fmt = '%.8f')

