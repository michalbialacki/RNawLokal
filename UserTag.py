import numpy as np
import ExtendedKalmanFilter

"""
Algorytm obliczający pozycję obiektu/urządzenia mobilnego
wykorzystując przy tym odległości do urządzeń statycznych
"""


class MobileTag:
    estimated_pos = np.array([1, 2])
    active_unit_pos = []
    EKF = ExtendedKalmanFilter.EKF()
    EKF_result = np.array([])
    EKF_error = np.array([])

    def __init__(self, passive_units_xy, passive_units_dist):
        self.passive_units_xy = passive_units_xy
        self.passive_units_dist = passive_units_dist
        EKF = ExtendedKalmanFilter.EKF()
        EKF.set_anchors(np.array(self.passive_units_xy))

    def __str__(self):
        return f"User's position {self.active_unit_pos}"

    def OLSAlgorythm(self):
        delta_z = np.array([100.0, 100.0, 100.0, 100.0]).T
        d_est = np.zeros(4)
        h_matrix = np.array([[0., 0.], [0., 0.], [0., 0.], [0., 0.]])
        checking_norm_value = 1

        for iterator in range(0, 4):
            d_est[iterator] = (((self.passive_units_xy[iterator][0] - self.estimated_pos[0]) ** 2 + (
                    self.passive_units_xy[iterator][1] - self.estimated_pos[1]) ** 2)) ** 0.5

        while checking_norm_value > 0.01:
            for iterator in range(0, 4):
                delta_z[iterator] = (d_est[iterator] - self.passive_units_dist[iterator])
                h_matrix[iterator][0] = (-(self.passive_units_xy[iterator][0] - self.estimated_pos[0])) / (
                        ((self.passive_units_xy[iterator][0] - self.estimated_pos[0]) ** 2 + (
                                self.passive_units_xy[iterator][1] - self.estimated_pos[1]) ** 2) ** 0.5)
            for iterator in range(0, 4):
                h_matrix[iterator][1] = (-(self.passive_units_xy[iterator][1] - self.estimated_pos[1])) / (
                        ((self.passive_units_xy[iterator][0] - self.estimated_pos[0]) ** 2 + (
                                self.passive_units_xy[iterator][1] - self.estimated_pos[1]) ** 2) ** 0.5)
            delta_x_est = np.linalg.inv(h_matrix.T.dot(h_matrix))
            delta_x_est = delta_x_est.dot(h_matrix.T).dot(delta_z)
            checking_norm_value = np.linalg.norm(delta_x_est)
            self.estimated_pos = self.estimated_pos - delta_x_est
            active_unit_location = [self.estimated_pos[0], self.estimated_pos[1]]
            for iterator in range(0, 4):
                d_est[iterator] = (((self.passive_units_xy[iterator][0] - active_unit_location[0]) ** 2) + (
                        (self.passive_units_xy[iterator][1] - active_unit_location[1]) ** 2)) ** 0.5
                pass
            self.estimated_pos = active_unit_location
        return round(active_unit_location[0], 3), round(active_unit_location[1], 3)

    def EKFAlgorythm(self):
        anchors = np.array(self.passive_units_xy)
        EKF =  self.EKF
        EKF.set_anchors(anchors)
        meas = np.array(self.passive_units_dist).reshape((4,1))
        state, error = EKF.predict(anchors)
        self.EKF.update(meas=meas, err_cov_mat_pred=error, state_pred=state)
        temp = self.EKF.show_results()
        return EKF.show_results()


if __name__ == '__main__':
    """
    Testowanie poprawności działania algorytmu, mechanizmu tworzenia klasy
    """

    lista_wsp = [[0.0, 0.0], [4.0, 0.0], [4.0, 5.0], [0.0, 5.0]]
    lista_odl = [0.74, 3.21, 6.52, 5.56]
    uzytkownik = MobileTag(lista_wsp, lista_odl)
    uzytkownik.active_unit_pos = uzytkownik.OLSAlgorythm()
    print(uzytkownik)
