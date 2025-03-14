#
# This function writes a molden_file taking as input:
# - xyz_file: A '.xyz' file with the coordinates
# - basis_file: A '.basis' file with the basis set block
# - ao_weights: A numpy array with the weights
#

import numpy as np

def read_xyz_make_first_molden_block(xyzFile):
    angstrom = 1.0 / 0.529177  # Conversion factor to atomic units
    element_map = {'H': 1, 'C': 6, 'F': 9, 'Cl': 17}  # Atomic number mapping    
    with open(xyzFile, 'r') as xyzF:
        oLines = []
        oLines.append('[Molden Format]\n[Atoms] AU\n')
        for i, line in enumerate(xyzF, start=-1):  # Start from -1 to skip first two lines
            if i < 1:
                continue  # Skip first two lines of XYZ file
            parts = line.split()
            element = parts[0]
            index = i  # Adjust index to match required numbering
            atomic_number = element_map.get(element, 0)  # Get atomic number, default to 0 if unknown
            x, y, z = (float(parts[j]) * angstrom for j in range(1, 4))  # Convert coordinates
            # Formatting to match the required output:
            oLine = f"{element:>3} {index:>5} {atomic_number:>3} {x:>16.10f} {y:>16.10f} {z:>16.10f}\n"
            oLines.append(oLine)
    return oLines

def read_basis_block_from_template(moldenTemplate):
    with open(moldenTemplate, 'r') as templateFile:
        block2 = []
        read = False
        for line in templateFile:
            if '[GTO]' in line:
                read = True
            if read:
                block2.append(line)
            if '[9G]' in line:
                return block2

def make_third_block(weights):
    oLines = []
    oLines.append('[MO]\nSym= a\nEne= -0.0\nSpin= Alpha\nOccup=        2.00000000000000\n')
    for i, w in enumerate(weights, start=1):
        oLines.append(f"{i:>6}    {w: .16f}\n")
    return oLines

def make_molden(xyzFile, templateFile, weights, moldenFile):
    with open(xyzFile, 'r') as xyz:
        i = 0
        atoms = []
        for line in xyz:
            i += 1
            if i >= 3:
                atoms.append(line.split()[0])
    with open(moldenFile, 'w') as moldenFile:
        block1 = read_xyz_make_first_molden_block(xyzFile)
        for lines in block1:
            moldenFile.write(lines)
        block2 = read_basis_block_from_template(templateFile)
        for lines in block2:
            moldenFile.write(lines)
        for w in weights:
            block3 = make_third_block(w)
            for lines in block3:
                moldenFile.write(lines)
'''
# Example of use:
xyzFile = 'data_F_core/0000/geometry.xyz'
templateFile = 'pbe0.molden'
RijFile = 'data_F_core/0000/Rij_2_1.txt'
Rij = np.loadtxt(RijFile)
weights = np.diagonal(Rij)
moldenFile = 'data_F_core/0000/Rij_SVD_1.molden'
make_molden(xyzFile, templateFile, [weights, weights], moldenFile)
'''
    
'''
# Building basis block from basis file
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
'''
