#
#   This script calculates the matrix R_ij, with the information of the 
# contributions to the rotatory strength from the electric dipole of AO
# "i" and the magnetic dipole from AO "j".
#

import numpy as np
import time
import torch
from datetime import timedelta
from get_civecs_from_data import get_civecs_from_data
from get_MO_matrix_from_NWChem import get_MO_matrix_from_NWChem
from calc_TDM import calc_TDM
from get_electric_dipole_from_NWChem import get_electric_dipole_from_NWChem
from get_magnetic_dipole_from_NWChem import get_magnetic_dipole_from_NWChem  

nwFile = 'plot.out'
dataFile = 'civecs.data'

#Reading MO matrix
mo = get_MO_matrix_from_NWChem(nwFile)

#Reading CI for a given root
root = 1
ci1 = get_civecs_from_data(dataFile, root)

#Calculating TDM
tdmNP = calc_TDM(mo, ci1)

#Reading dipoles:
muxNP = get_electric_dipole_from_NWChem(nwFile, 'x')
muyNP = get_electric_dipole_from_NWChem(nwFile, 'y')
muzNP = get_electric_dipole_from_NWChem(nwFile, 'z')
mxNP = get_magnetic_dipole_from_NWChem(nwFile, 'x')
myNP = get_magnetic_dipole_from_NWChem(nwFile, 'y')
mzNP = get_magnetic_dipole_from_NWChem(nwFile, 'z')

#Calculating R_ij
print('Building dipolesT tensor')
start = time.time()
# With NumPy:
Rij = np.einsum('ij,kl,ji,lk->ik', muxNP, mxNP, tdmNP, tdmNP) + np.einsum('ij,kl,ji,lk->ik', muyNP, myNP, tdmNP, tdmNP) + np.einsum('ij,kl,ji,lk->ik', muzNP, mzNP, tdmNP, tdmNP)
np.savetxt('Rij.txt', Rij, fmt = '%.8f')

# With Torch:
#mux = torch.from_numpy(muxNP).float()
#muy = torch.from_numpy(muyNP).float()
#muz = torch.from_numpy(muzNP).float()
#mx = torch.from_numpy(mxNP).float()
#my = torch.from_numpy(myNP).float()
#mz = torch.from_numpy(mzNP).float()
#tdm = torch.from_numpy(tdmNP).float()
#device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
#mux = mux.to(device)
#muy = muy.to(device)
#muz = muz.to(device)
#mx = mx.to(device)
#my = my.to(device)
#mz = mz.to(device)
#tdm = tdm.to(device)
#Rij = torch.einsum('ij,kl,ji,lk->ik', mux, mx, tdm, tdm) + torch.einsum('ij,kl,ji,lk->ik', muy, my, tdm, tdm) + torch.einsum('ij,kl,ji,lk->ik', muz, mz, tdm, tdm)
#np.savetxt("Rij_torch.txt", Rij.cpu().numpy(), fmt="%.8f", delimiter=" ")

end = time.time()
excecution_time = end - start
print('done in ' + str(timedelta(seconds = excecution_time)))

