#
# This function writes a molden_file taking as input:
# - xyz_file: A '.xyz' file with the coordinates
# - basis_file: A '.basis' file with the basis set block
# - ao_weights: A numpy array with the weights
#

import numpy as np

def read_xyz_make_first_molden_block(xyzFile):
    angstrom = 1.0 / 0.529177 #AU
    with open(xyzFile, 'r') as xyzF:
        oLines = []
        oLines.append('[Molden Format]\nAtoms AU\n')
        i = 0
        for line in xyzF:
            i += 1
            if i >= 3:
                if 'H' in line:
                    oLine = '\t' + line.split()[0] + '\t' + str(i - 2) + '\t1\t' + str(float(line.split()[1]) * angstrom) + '\t' + str(float(line.split()[2]) * angstrom) + '\t' + str(float(line.split()[3]) * angstrom) + '\n'
                if 'C' in line:
                    oLine = '\t' + line.split()[0] + '\t' + str(i - 2) + '\t6\t' + str(float(line.split()[1]) * angstrom) + '\t' + str(float(line.split()[2]) * angstrom) + '\t' + str(float(line.split()[3]) * angstrom) + '\n'
                if 'F' in line:
                    oLine = '\t' + line.split()[0] + '\t' + str(i - 2) + '\t9\t' + str(float(line.split()[1]) * angstrom) + '\t' + str(float(line.split()[2]) * angstrom) + '\t' + str(float(line.split()[3]) * angstrom) + '\n'
                if 'Cl' in line:
                    oLine = '\t' + line.split()[0] + '\t' + str(i - 2) + '\t17\t' + str(float(line.split()[1]) * angstrom) + '\t' + str(float(line.split()[2]) * angstrom) + '\t' + str(float(line.split()[3]) * angstrom) + '\n'
                oLines.append(oLine)
    return oLines

def read_basis_make_second_block(basisFile, atoms):
    basis = {}
    with open(basisFile, 'r') as bFile:
        current_atom = None
        shell_type = None
        for line in bFile:
            if len(line) == 0: #Skip empty lines
                continue
            if "****" in line: #Skip line with atom separator
                current_atom = None
                shell_type = None
                continue
            if len(line.split()) == 3 and line.split()[0] in ['S', 'P', 'SP', 'D', 'F']:
                shell_type = line.split()[0]
                num_functions = int(line.split()[1])
                basis[current_atom].append({'shell': shell_type, 'num_functions': num_functions, 'coeffs': []})
            elif line.split()[0] in atoms:
                current_atom = line.split()[0]
                basis[current_atom] = []
            else:
                line = line.replace('D', 'E') # Replace 'D' with 'E' for scientific notation
                coeffs = list(map(float, line.split()))
                if shell_type: # Add coefficients to the last shell
                    basis[current_atom][-1]['coeffs'].append(coeffs)
    oLines = []
    oLines.append('[GTO]\n')
    atom_index = 1
    for atom in atoms:
        oLines.append(str(atom_index) + '\t0\n')
        for shell in basis[atom]:
            oLines.append(str(shell['shell']) + '\t' + str(shell['num_functions']) + '\t0\n')
            for coeffs in shell['coeffs']:
                for coeff in coeffs:
                    oLines.append(str(coeff) + '\t')
                oLines.append('\n')
        atom_index += 1
        oLines.append('\n')
    return oLines

def make_third_block(weights):
    oLines = []
    oLines.append('[MO]\nSym= a\nEne= -0.0\nSpin= Alpha\nOccup=        2.00000000000000\n')
    i = 0
    for w in weights:
        i += 1
        oLines.append(str(i) + '\t' + str(w) + '\n')
    return oLines

xyzFile = 'geometry.xyz'
basisFile = 'helicene.basis'
# Reading atoms 
with open(xyzFile, 'r') as xyz:
    i = 0
    atoms = []
    for line in xyz:
        i += 1
        if i >= 3:
            atoms.append(line.split()[0])
print(atoms)
# Reading weights
RijFile = 'Rij_2_1.txt'
Rij = np.loadtxt(RijFile) 
Rii = np.diag(Rij)

with open('output.molden', 'w') as moldenFile:
    block1 = read_xyz_make_first_molden_block(xyzFile)
    for lines in block1:
        moldenFile.write(lines)
    block2 = read_basis_make_second_block(basisFile, atoms)
    for lines in block2:
        moldenFile.write(lines)
    block3 = make_third_block(Rii)
    for lines in block3:
        moldenFile.write(lines)
