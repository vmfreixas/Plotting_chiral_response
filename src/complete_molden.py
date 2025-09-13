import numpy as np

RijFile = 'Rij_2_1.txt'
Rij = np.loadtxt(RijFile) 
Rii = np.diag(Rij)
with open('pbe0.molden', 'a') as mFile:
    i = 0
    for r in Rii:
        i += 1
        mFile.write('\t' + str(i) + '\t' + str(r) + '\n')

    
