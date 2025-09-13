import numpy as np

def make_Rw(elecX, elecY, elecZ, magX, magY, magZ):
    rr = np.outer(elecX, magX) + np.outer(elecY, magY) + np.outer(elecZ, magZ)
    rrSym = (rr + rr.T) / 2
    return rrSym.sum(axis = 0)
