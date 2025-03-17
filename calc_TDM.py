#
# This function returns the TDM from the MO and CI vectors.
#

import numpy as np

def calc_TDM(mo, ci1, ci2 = ''):
    if ci2 != '':
        (Nocc, Nvir) = ci1.shape
        tdmMO = np.zeros((Nocc + Nvir, Nocc + Nvir), dtype = float)
        tdmMO[:Nocc, Nocc:] = ci1
        return mo @ tdmMO @ mo.T
    else:
        (Nocc, Nvir) = ci1.shape
        tdmMO = np.zeros((Nocc + Nvir, Nocc + Nvir), dtype = float)
        tdmMO[:Nocc, :Nocc] = -1.0 * ci1 @ ci2.T
        tdmMO[Nocc:, Nocc:] = ci1.T @ ci2
        return mo @ tdmMO @ mo.T
