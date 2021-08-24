import numpy as np

"""
Algorytm obliczający pozycję obiektu/urządzenia mobilnego
wykorzystując przy tym odległości do urządzeń statycznych
"""


def OLSAlgorythm(passive_units_xy, passive_units_dist):
    delta_z = np.array([100.0, 100.0, 100.0, 100.0]).T
    estimated_pos = np.array([1, 2])
    d_est = np.zeros(4)
    h_matrix = np.array([[0., 0.], [0., 0.], [0., 0.], [0., 0.]])
    checking_norm_value = 1

    for iterator in range(0, 4):
        d_est[iterator] = (((passive_units_xy[iterator][0] - estimated_pos[0]) ** 2 + (
                passive_units_xy[iterator][1] - estimated_pos[1]) ** 2)) ** 0.5

    while checking_norm_value > 0.01:
        for iterator in range(0, 4):
            delta_z[iterator] = (d_est[iterator] - passive_units_dist[iterator])
            h_matrix[iterator][0] = (-(passive_units_xy[iterator][0] - estimated_pos[0])) / (
                    ((passive_units_xy[iterator][0] - estimated_pos[0]) ** 2 + (
                            passive_units_xy[iterator][1] - estimated_pos[1]) ** 2) ** 0.5)
        for iterator in range(0, 4):
            h_matrix[iterator][1] = (-(passive_units_xy[iterator][1] - estimated_pos[1])) / (
                    ((passive_units_xy[iterator][0] - estimated_pos[0]) ** 2 + (
                            passive_units_xy[iterator][1] - estimated_pos[1]) ** 2) ** 0.5)
        delta_x_est = np.linalg.inv(h_matrix.T.dot(h_matrix))
        delta_x_est = delta_x_est.dot(h_matrix.T).dot(delta_z)
        checking_norm_value = np.linalg.norm(delta_x_est)
        estimated_pos = estimated_pos - delta_x_est
        active_unit_location = [estimated_pos[0], estimated_pos[1]]
        for iterator in range(0, 4):
            d_est[iterator] = (((passive_units_xy[iterator][0] - active_unit_location[0]) ** 2) + (
                    (passive_units_xy[iterator][1] - active_unit_location[1]) ** 2)) ** 0.5
            pass
        estimated_pos = active_unit_location
    return active_unit_location
