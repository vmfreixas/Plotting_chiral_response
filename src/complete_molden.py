import numpy as np

def complete_molden(moldenTemplate, moldenOutput, wR):
    moldenLines = []
    with open(moldenTemplate, 'r') as mFile:
        for lines in mFile:
            moldenLines.append(lines)
            if 'Occup=' in lines:
                break
    with open(moldenOutput, 'w') as mFile:
        for lines in moldenLines:
            mFile.write(lines)
        for i, wAO in enumerate(wR):
            mFile.write(f"{i + 1:6d}   {wAO: .16f}\n")
    return None