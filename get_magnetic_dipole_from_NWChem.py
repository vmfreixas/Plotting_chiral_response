#
#  This function reads NWChem standard output (specially modified
# version of NWChem for this purpose) and returns the magnetic dipoles
# integral matrix for a given direction ('x', 'y', or 'z').
#

import numpy as np

def get_magnetic_dipole_from_NWChem(fileName, direction):
    if direction == 'x':
        xyz = '1'
    if direction == 'y':
        xyz = '2'
    if direction == 'z':
        xyz = '3'
    with open(fileName, 'r') as nwFile:
        mBlock = False
        done = False
        for line in nwFile:
            if mBlock:
                i += 1
                if i == -2: 
                    columns = list(map(int, line.split()))
                if i >= 0:
                    k = 0 
                    for j in columns:
                        k += 1
                        m[int(line.split()[0]) - 1, j - 1] = float(line.split()[k])
                        if(int(line.split()[0]) == Nbf and j == Nbf):
                            done = True
                if done:
                    return(m)
                if i == Nbf - 1:
                    i = -4
            if '-- patch: e-dipve' in line and line.split(',')[-1].split(']')[0] == xyz:
                Nbf = int(line.split(':')[2].split(',')[0])
                m = np.zeros((Nbf, Nbf), dtype = float)
                mBlock = True
                i = -4

filename = 'plot.out'
direction = 'x'
m_x = get_magnetic_dipole_from_NWChem(filename, direction)
np.savetxt('m_x.txt', m_x, fmt = '%.8f')

filename = 'plot.out'
direction = 'y'
m_y = get_magnetic_dipole_from_NWChem(filename, direction)
np.savetxt('m_y.txt', m_y, fmt = '%.8f')

filename = 'plot.out'
direction = 'z'
m_z = get_magnetic_dipole_from_NWChem(filename, direction)
np.savetxt('m_z.txt', m_z, fmt = '%.8f')


