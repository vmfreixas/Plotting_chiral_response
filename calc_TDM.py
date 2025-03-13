#
# This function returns the TDM from the MO and CI vectors.
#

import numpy as np

def calc_TDM(mo, ci):
    (Nocc, Nvir) = ci.shape
    tdmMO = np.zeros((Nocc + Nvir, Nocc + Nvir), dtype = float)
    tdmMO[:Nocc, Nocc:] = ci
    return mo @ tdmMO @ mo.T
