#
#   This functions takes the Rij matrix as input and returns, for a
# given order, the corresponding orbital weights for the electric and
# the magnetic contributions to the rotatory strength.
#

import numpy as np

def calc_moment_contrib(Rij, order): 
    # Compute the SVD of Rij
    U, s, Vt = np.linalg.svd(Rij, full_matrices=False)

    # The first column of U represents the left singular vector corresponding to the largest singular value
    first_left_singular_vector = U[:, order - 1]

    # The first row of Vt represents the right singular vector corresponding to the largest singular value
    first_right_singular_vector = Vt[order - 1, :]
    return [first_left_singular_vector, first_right_singular_vector]

'''
# Example of use
RijFile = 'Rij_2_1.txt'
Rij = np.loadtxt(RijFile)
order = 1

[eleOrb, magOrb] = calc_moment_contrib(Rij, order)

np.savetxt('eleOrb.txt', eleOrb, fmt = '%.8f')
np.savetxt('magOrb.txt', magOrb, fmt = '%.8f')
'''

