#
#   This function uses a Fortran program to read civec binary files
# produced by NWChem. The file names and vectors read by the
# executable are hardwired within the Fortran source. 
#

import shutil
import subprocess
import os

def read_civecs(exeFile, dataFile):
    # Store the original directory
    original_dir = os.getcwd()

    # Copy the executable:
    shutil.copy(exeFile, dataFile)

    # Change to the dataFile directory:
    os.chdir(dataFile)

    # Run the executable
    subprocess.run(["./" + exeFile], check=True)
    
    # Return to the original directory
    os.chdir(original_dir)

'''
# Example of use:
exeFile = 'read_civecs.x'
dataFile = 'data_F_core/0000'
read_civecs(exeFile, dataFile)
'''
