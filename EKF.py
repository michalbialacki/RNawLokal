import numpy as np

def initialize_predict(anchor_coor = np.array([[0, 0], [4, 0], [4, 5], [0, 5]]), position = np.array((1, 1)).transpose()):
    # init
    P_0 = np.array([[0.1, 0], [0, 0.1]])
    P_prev = P_0.copy()
    F = np.array([[1, 0], [0, 1]])
    Q = np.array([[0.05, 0], [0, 0.05]])
    R = np.diag(np.diag([0.1, 0.1, 0.1, 0.1]))  # utworzy macierz diagonalną o wymiarach 4x4
    H = np.zeros((4, 2))
    h_mat = np.zeros(4)

    for index in range(0,4):
        h_mat[index] = np.sqrt((position[0] - anchor_coor[index, 0]) ** 2 + (position[1] - anchor_coor[index, 1]) ** 2)


    # Jacobian

    for col in range(0, 2):  # kolumny
        for row in range(0, 4):  # wiersze
            H[row, col] = (position[col] - anchor_coor[row, col]) / (np.sqrt((position[0] - anchor_coor[row, 0]) ** 2 + (position[1] - anchor_coor[row, 1]) ** 2))

    # Predict
    x_hat = F.dot(position)
    P_pred = F.dot(P_prev).dot(np.linalg.inv(F)) + Q


    return h_mat,P_pred,H,R,Q,F,x_hat

def update(obs = [2.15, 4.22, 4.87, 0.8],
           h_mat = [0,1,2,4],
           H = np.zeros((4,4)),
           P_pred = np.zeros((2,2)),
           R = np.zeros((4,4)),
           x_hat = np.zeros((2,2))):

    # Update
    innov = obs - h_mat
    S=np.matmul(np.matmul(H,P_pred),H.transpose()) + R
    K = np.matmul(np.matmul(P_pred,H.transpose()),np.linalg.inv(S))
    P_up = (np.eye(2)-(np.matmul(K,H))).dot(P_pred)
    position = x_hat + np.matmul(K,innov)
    print(position)

    return position,P_up


if __name__ == '__main__':

    """
    Dla funkcjonalnosci kodu, przyjmuję wartości pomiarów wykonane przez stację mobilną jako [2.15, 4.22, 4.87, 0.8]
    W ostateczniej wersji programu/aplikacji, pomiary odległości będą pobierane z UM z czestotliwoscia zadana do UM 
    i przekazywane do tej klasy jako argument podczas jej wywołania.
    """

    pomiar_UWB = np.array([2.15, 4.22, 4.87, 0.8])
    position = np.array((1, 1)).transpose()
    (h_mat, P_pred, H, R, Q, F, x_hat) = initialize_predict()
    while(pomiar_UWB is not None):
        (h_mat,P_pred,H,R,Q,F,x_hat) = initialize_predict(position, P_up)
        position,P_up = update(h_mat=h_mat,H=H,P_pred=P_pred,R=R,x_hat=x_hat)