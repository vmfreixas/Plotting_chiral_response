#
#    This functions generates a cube file from a molden file by using
# Multiwfn
#

import shutil
import subprocess
import os

def make_cube(multiwfnExe, dataFile, moldenFile):
    # Multiwfn instructions as a string (each command followed by a newline)
    # 200 # Other functions (Part 2)
    # 3   # Generate cube file for multiple orbital wavefunctions
    # 1,2 # Input orbital index
    # 1   # Low quality grid
    # 1   # Output the grid data of these orbitals as separate cube files
    # 0   # Return
    # q   # Exit
    instructions = """\
    200
    3
    1,2
    1
    1
    0
    q
    """
    # Store the original directory
    original_dir = os.getcwd()

    # Change to the dataFile directory:
    os.chdir(dataFile)

    # Run Multiwfn with the provided instructions
    process = subprocess.Popen(
        [multiwfnExe, moldenFile],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True  # Ensures text mode (string input/output)
    )
    stdout, stderr = process.communicate(instructions)

    # Print any captured output (some versions of Multiwfn may print messages)
    #if stdout.strip():
    #    print("Multiwfn output:", stdout)
    #if stderr.strip():
    #    print("Errors:", stderr)
    
    # Return to the original directory
    os.chdir(original_dir)    

'''
# Example of use:
multiwfnExe = '/Applications/Multiwfn_3.7_bin_Mac/Multiwfn'
dataFile = 'data_F_core/0000'
moldenFile = 'Rij_SVD_1.molden' 
make_cube(multiwfnExe, dataFile, moldenFile)
'''

