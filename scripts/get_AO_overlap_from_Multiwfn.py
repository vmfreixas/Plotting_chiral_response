#   This function reads the AO overlap matrix calculated by Multiwfn. The matrix is written as a lower
# triangular matrix. The input is the name of the file containing the AO overlap matrix and the
# number of basis functions. The output is the AO overlap matrix as a numpy array.

import numpy as np
def get_AO_overlap_from_Multiwfn(Nbf, fileName = "intmat.txt"):
    ao = np.zeros((Nbf, Nbf), dtype = float)
    row = 0
    with open(fileName, 'r') as intFile:
        firstLine = True
        block = False
        for line in intFile:
            if line.split() == []:
                break
            if block:
                row = int(line.split()[0]) - 1
                values = np.fromstring(" ".join(line.split()[1:]), sep=" ", dtype = float)
                for c, val in enumerate(values):
                    ao[row, cols[c]] = val
                    ao[cols[c], row] = val
            if (not firstLine) and (not block):
                cols = np.fromstring(line, sep=" ", dtype = int) - 1
                block = True
                row = 0
            if row == Nbf - 1:
                block = False
            if firstLine:
                firstLine = False
    return(ao)