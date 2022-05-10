import numpy as np
import pandas as pd


class EKF:
    np.set_printoptions(precision=2)
    jacobian = np.zeros((4, 4))  # H
    T = 0.1  # okres probkowania
    S = 0.00001  # widmowa gestosc mocy // zmieniac rzędem wielkości// sprawdzac przy zakretach
    state_vect_input = np.array([.01, .1, .01, .1]).reshape((4, 1))  # wektor stanu
    err_cov_mat_input = np.diag([100, 8.3, 100, 8.3])
    R = np.diag([0.01, 0.01, 0.01, 0.01])  # m. kowariancji bledow pomiarowych
    trans_mat = np.array([[1, T, 0, 0], [0, 1, 0, 0], [0, 0, 1, T],
                          [0, 0, 0, 1]])  # macierz tranzycyjna
    h_mat = np.zeros((4, 1))
    Q = np.array([[((S * (T ** 3)) / 3), ((S * (T ** 2)) / 2), 0, 0], [((S * (T ** 2)) / 2), (S * T), 0, 0],
                  [0, 0, ((S * (T ** 3)) / 3), ((S * (T ** 2)) / 2)],
                  [0, 0, ((S * (T ** 2)) / 2), (S * T)]])  # m. kow. zaklocen
    anchor_coor = np.array([[0, 0], [4, 0], [0, 5], [4, 5]])

    def __init__(self):
        pass

    def set_anchors(self, new_coors = np.array([[0, 0], [4, 0], [0, 5], [4, 5]])):
        self.anchor_coor = new_coors


    def get_jacobian(self,
                     anchor_coor = anchor_coor):
        # obliczanie jakobianu
        jacobian = self.jacobian.copy()
        h_mat = self.h_mat.copy()
        for col in range(0, 2):
            for row in range(0, 4):
                h_mat[row, 0] = np.sqrt(
                    ((anchor_coor[row, 0] - self.state_vect_input[0]) ** 2) + (
                            (anchor_coor[row, 1] - self.state_vect_input[2]) ** 2))
                jacobian[row, col * 2] = -(anchor_coor[row, col] - self.state_vect_input[col * 2]) / np.sqrt(
                    ((anchor_coor[row, 0] - self.state_vect_input[0]) ** 2) + (
                            (anchor_coor[row, 1] - self.state_vect_input[2]) ** 2))
        self.jacobian = jacobian
        self.h_mat = h_mat


    def predict(self, passive_XYs = anchor_coor):
        state = self.state_vect_input
        cov = self.err_cov_mat_input
        state_vect_pred = self.trans_mat @ state  # 4x4
        err_cov_mat_pred = self.trans_mat @ cov @ self.trans_mat.transpose() + self.Q  # 4x4
        self.get_jacobian(passive_XYs)
        return state_vect_pred, err_cov_mat_pred

    def update(self,
               meas=np.array([[0.74], [3.21], [5.56], [6.52]]),
               err_cov_mat_pred = err_cov_mat_input,
               state_pred = state_vect_input):
        self.S = self.jacobian @ err_cov_mat_pred @ self.jacobian.transpose() + self.R
        gain_mat = err_cov_mat_pred @ self.jacobian.transpose() @ np.linalg.inv(self.S)
        err_cov_mat_up = (np.eye(4, 4) - (gain_mat @ self.jacobian)) @ err_cov_mat_pred
        state_vect_up = state_pred + (gain_mat @ (meas - self.h_mat))
        self.state_vect_input = state_vect_up
        self.err_cov_mat_input = err_cov_mat_up

    def show_results(self):
        return self.state_vect_input
