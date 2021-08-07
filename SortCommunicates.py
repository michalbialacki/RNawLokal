import numpy as np

def XYsSort(passiveUnitXYs, passiveUnitDist):
    srtdListXYs = np.array([[0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0]])
    srtdListDist = np.array([0.0, 0.0, 0.0, 0.0])
    for index in range(0, 4):
        if '0.00' in passiveUnitXYs[index][0]:
            if '0.00' in passiveUnitXYs[index][1]:
                srtdListXYs[0][0] = float(passiveUnitXYs[index][0])
                srtdListXYs[0][1] = float(passiveUnitXYs[index][1])
                srtdListDist[0] = float(passiveUnitDist[index])

            else:
                srtdListXYs[3][0] = float(passiveUnitXYs[index][0])
                srtdListXYs[3][1] = float(passiveUnitXYs[index][1])
                srtdListDist[3] = float(passiveUnitDist[index])
        else:
            if '0.00' in passiveUnitXYs[index][1]:
                srtdListXYs[1][0] = float(passiveUnitXYs[index][0])
                srtdListXYs[1][1] = float(passiveUnitXYs[index][1])
                srtdListDist[1] = float(passiveUnitDist[index])
            else:
                srtdListXYs[2][0] = float(passiveUnitXYs[index][0])
                srtdListXYs[2][1] = float(passiveUnitXYs[index][1])
                srtdListDist[2] = float(passiveUnitDist[index])
    return srtdListXYs, srtdListDist
