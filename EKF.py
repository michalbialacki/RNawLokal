import numpy as np
import csv

np.set_printoptions(precision=2)
jacobian = np.zeros((4, 4))  # H
T = 0.1  # okres probkowania
S = 0.01 # widmowa gestosc mocy
state_vect_input = np.array([.5, .1, .5, .1]).reshape((4, 1))  # wektor stanu
err_cov_mat_input = np.diag([100, .1, 100, .1])
R = np.diag([5, 10, 5, 10])  # m. kowariancji bledow pomiarowych
trans_mat = np.array([[1, T, 0, 0], [0, 1, 0, 0], [0, 0, 1, T],
                      [0, 0, 0, 1]])  # macierz tranzycyjna T=0.1 bo taki zakladam okres probkowania
h_mat = np.zeros((4, 1))
Q = np.array([[((S * (T ** 3)) / 3), ((S * (T ** 2)) / 2), 0, 0], [((S * (T ** 2)) / 2), (S * T), 0, 0],
              [0, 0, ((S * (T ** 3)) / 3), ((S * (T ** 2)) / 2)], [0, 0, ((S * (T ** 2)) / 2), (S * T)]])  # m. kow. zaklocen



def predictEKF(anchor_coor=np.array([[0, 0], [4, 0], [0, 5], [4, 5]]),
               state_vect_ini=state_vect_input,
               err_cov_mat_ini=err_cov_mat_input):
    # obliczanie jakobianu
    for col in range(0, 2):
        for row in range(0, 4):
            h_mat[row, 0] = np.sqrt(
                ((anchor_coor[row, 0] - state_vect_ini[0]) ** 2) + ((anchor_coor[row, 1] - state_vect_ini[2]) ** 2))
            jacobian[row, col * 2] = -(anchor_coor[row, col] - state_vect_ini[col * 2]) / np.sqrt(
                ((anchor_coor[row, 0] - state_vect_ini[0]) ** 2) + ((anchor_coor[row, 1] - state_vect_ini[2]) ** 2))

    state_vect_pred = trans_mat @ state_vect_ini  # 4x4
    err_cov_mat_pred = trans_mat @ err_cov_mat_ini @ trans_mat.transpose() + Q  # 4x4

    return state_vect_pred, err_cov_mat_pred, jacobian


def updateEKF(meas=np.array([[0.74], [3.21], [5.56], [6.52]]),
              state_vect_pred= state_vect_input,
              H_mat=jacobian,
              err_cov_mat_pred= err_cov_mat_input):
    # Update
    S = H_mat @ err_cov_mat_pred @ H_mat.transpose() + R
    gain_mat = err_cov_mat_pred @ H_mat.transpose() @ np.linalg.inv(S)
    err_cov_mat_up = (np.eye(4, 4) - (gain_mat @ H_mat)) @ err_cov_mat_pred
    temp = gain_mat @ (meas - h_mat)
    state_vect_up = state_vect_pred + (gain_mat @ (meas - h_mat))
    return state_vect_up, err_cov_mat_up


if __name__ == '__main__':

    """
    Dla funkcjonalnosci kodu, przyjmuję wartości pomiarów wykonane przez stację mobilną jako [2.15, 4.22, 4.87, 0.8]
    W ostateczniej wersji programu/aplikacji, pomiary odległości będą pobierane z UM z czestotliwoscia zadana do UM 
    i przekazywane do tej klasy jako argument podczas jej wywołania.
    """

    ######################
    lista = []
    with open('do_loop.csv', mode='r') as fp:
        passive_unit_com = csv.reader(fp)
        for value in passive_unit_com:
            try:
                temp = np.array([float(value[7]), float(value[13]), float(value[19]), float(value[25])]).reshape((4, 1))
                lista.append(temp)
            except IndexError:
                print("Index Error")

    for row in lista:
        pred, covariance, jacob = predictEKF(state_vect_ini=state_vect_input, err_cov_mat_ini=err_cov_mat_input)
        state_vect_input, err_cov_mat_input = updateEKF(meas=row, state_vect_pred=pred, H_mat=jacob,
                                                        err_cov_mat_pred=covariance)
        print(f'{state_vect_input};\n \n')

    ###########################

    #
    # pomiar_UWB = np.array([2.15, 4.22, 4.87, 0.8])
    # position = np.array((1, 1)).transpose()
    # (h_mat, P_pred, H, R, Q, F, x_hat) = initialize_predict()
    # while(pomiar_UWB is not None):
    #     (h_mat,P_pred,H,R,Q,F,x_hat) = initialize_predict()
    #     print(f'{np.matmul(H, x_hat)}')
    #     # pomiar_UWB = None
    #     # position,P_up = update(h_mat=h_mat,H=H,P_pred=P_pred,R=R,x_hat=x_hat)
