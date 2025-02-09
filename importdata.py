import numpy as np

def getValues(run_number):
    cpmEta, cpmPhi, cpmVal, efxEta, efxPhi, efxVal, _, r2, _ = np.loadtxt(f"data/roimatches_{run_number}.txt").transpose()
    # Data defect in run 427885 requires recalculating r2
    if run_number == 427885:
        for i in range(len(cpmEta)):
            r2[i] = (cpmEta[i] - efxEta[i])**2 + (cpmPhi[i] - efxPhi[i])**2
    return cpmEta, cpmPhi, cpmVal, efxEta, efxPhi, efxVal, r2
