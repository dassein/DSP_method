try:
    from rls.matrix import Matrix, Eye
except ModuleNotFoundError:
    from matrix import Matrix, Eye


class Lms(object):
    def __init__(self, mu, N, w_0=None):
        self.mu = mu
        self.N = N
        if w_0 == None:
            w_0 = [0] * self.N
        self.w = w_0 # w(n) = w(n-1) + 2*mu * e(n) * X(n)
        self.X = [0] * self.N
        # No need for initialization
        # update w(n) <= based on e(n), X(n): 
        # e(n) := d(n) - y(n) = d(n) - w(n-1) * X(n)
        self.y = 0 # y(n) := d(n) - w(n-1) * X(n)
        self.e = 0

    def __update_X(self, x): # __func(): private method
        self.X = [x] + self.X[:-1] # update X(n)
    
    def train(self, x, d):
        self.__update_X(x) 
        self.y = sum([w_ * x_ for (w_, x_) in list(zip(self.w, self.X))])
        self.e = d - self.y
        self.w = [w_ + 2 * self.mu * self.e * x_ for (w_, x_) in list(zip(self.w, self.X))]

if __name__ == "__main__":
    from math import sin, cos, pi
    import numpy as np
    import matplotlib.pyplot as plt
    #############################################################################  
    T = 10
    length = 1000
    list_x = [sin((2*pi/T)*ind) for ind in range(length)]
    list_d = [cos((2*pi/T)*ind) for ind in range(length)]
    list_y, list_e = [], []
    eps = 0.008
    N, Px = 5, 0.5 + eps
    mu = 1 / (N * Px)
    lms = Lms(mu=mu, N=N)
    lms.X = list_x[N-2::-1] + [0]
    for x, d in list(zip(list_x[N-1:], list_d[N-1:])):
        lms.train(x, d)
        list_y.append(lms.y)
        list_e.append(lms.e)
    plt.plot(list_d[N-1:], 'r-')
    plt.plot(list_e, 'k-')
    plt.show()
    print(lms.w)
