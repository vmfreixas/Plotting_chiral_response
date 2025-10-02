import numpy as np
from src.make_NWChem_Multiwfn_AO_index_permutation_matrix import make_NWChem_Multiwfn_AO_index_permutation_matrix

def make_Rw(elecX, elecY, elecZ, magX, magY, magZ, moldenTemplate):
    rr = np.outer(elecX, magX) + np.outer(elecY, magY) + np.outer(elecZ, magZ)
    rrSym = (rr + rr.T) / 2
    #Correcting the AO indices to ensure the index compability between NWChem and Multiwfn
    dim = 2
    permMatrix = make_NWChem_Multiwfn_AO_index_permutation_matrix(moldenTemplate, dim)
    rrSymCorrected = permMatrix.T @ rrSym @ permMatrix
    return rrSymCorrected.sum(axis = 0)
