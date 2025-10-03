#   This function reads a molden file and returns a numpy array with the permutation matrix that correct d AO indeces and
# signs to ensure the index compability between NWChem and Multiwfn.
#   The input also includes the optional dimension of the permutation matrix (1 for 1D arrays and 2 for 2D arrays). The
# default is 1.

import numpy as np

def custom_sign(x):
    s = np.sign(x)
    s[s == 0] = 1
    return s

def make_NWChem_Multiwfn_AO_index_permutation_matrix(moldenFile, dim = 1):
    ao_index = []
    with open(moldenFile, 'r') as moldenF:
        count = -1
        for line in moldenF:
            if line.split() == []:
                continue
            else:
                if '  s  ' in line:
                    count += 1
                    ao_index.append(count)
                elif '  p  ' in line:
                    for _ in range(3):
                        count += 1
                        ao_index.append(count)
                elif '  d  ' in line:
                        ao_index.append(count + 1 + 2)
                        ao_index.append(count + 1 + 3)
                        ao_index.append(count + 1 + 1)
                        ao_index.append(-(count + 1 + 4)) # Sign correction here!
                        ao_index.append(count + 1)
                        count += 5
                elif '  f  ' in line:
                    raise ValueError("f functions not implemented yet")
                    return(None)
    if dim == 1:
        return(ao_index)
    elif dim == 2:
        signs = custom_sign(ao_index)
        eyeSign = np.eye(len(ao_index)) * signs[:, np.newaxis]
        perm_matrix = eyeSign[np.abs(ao_index)]
        return(perm_matrix)
    else:
        raise ValueError("dim has to be 1 or 2")
        return(None)