def OLSAlgorythm(passiveUnitsXYs , passiveUnitsDist):
    # This is a sample Python script.
    import numpy as np

    # Press Shift+F10 to execute it or replace it with your code.
    # Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

    #passiveUnitsXYs = np.array([[0.0, 0.0], [4.0, 0.0], [4.0, 5.0], [0.0, 5.0]])
    #passiveUnitsDist = np.array([0.74, 3.21, 6.52, 5.56])
    delta_z = np.array([100.0, 100.0, 100.0, 100.0]).T
    estimatedPos = np.array([1, 2])
    d_est = np.zeros(4)
    H = np.array([[0., 0.], [0., 0.], [0., 0.], [0., 0.]])
    checkingNormValue = 1

    for iterator in range(0, 4):
        d_est[iterator] = (((passiveUnitsXYs[iterator][0] - estimatedPos[0]) ** 2 + (
                passiveUnitsXYs[iterator][1] - estimatedPos[1]) ** 2)) ** 0.5

    while checkingNormValue > 0.01:
        for iterator in range(0, 4):
            delta_z[iterator] = (d_est[iterator] - passiveUnitsDist[iterator])
            H[iterator][0] = (-(passiveUnitsXYs[iterator][0] - estimatedPos[0])) / (
                        ((passiveUnitsXYs[iterator][0] - estimatedPos[0]) ** 2 + (
                                passiveUnitsXYs[iterator][1] - estimatedPos[1]) ** 2) ** 0.5)
        for iterator in range(0, 4):
            H[iterator][1] = (-(passiveUnitsXYs[iterator][1] - estimatedPos[1])) / (
                        ((passiveUnitsXYs[iterator][0] - estimatedPos[0]) ** 2 + (
                                passiveUnitsXYs[iterator][1] - estimatedPos[1]) ** 2) ** 0.5)
        delta_x_est = np.linalg.inv(H.T.dot(H))
        delta_x_est = delta_x_est.dot(H.T).dot(delta_z)
        checkingNormValue = np.linalg.norm(delta_x_est)
        estimatedPos = estimatedPos - delta_x_est
        activeUnitLocation = [estimatedPos[0], estimatedPos[1]]
        for iterator in range(0, 4):
            d_est[iterator] = (((passiveUnitsXYs[iterator][0] - activeUnitLocation[0]) ** 2) + (
                        (passiveUnitsXYs[iterator][1] - activeUnitLocation[1]) ** 2)) ** 0.5
            pass
        estimatedPos = activeUnitLocation
    return activeUnitLocation