try:
    from rls.matrix import Matrix, Eye
except ModuleNotFoundError:
    from matrix import Matrix, Eye

class Rls(object):
    def __init__(self, delta, lambda_, N):
        self.delta = delta
        self.lambda_ = lambda_
        self.N = N
        self.Q = self.delta * Eye(self.N)
        self.w = [0] * self.N
        self.X = [0] * self.N
        # No need for initialization
        self.k = [0] * self.N # lambda_, Q(n-1), X(n)
        self.alpha = 0   # alpha(n) := d(n) - w(n-1) * X(n)
        # optional: e(n) := d(n) - y(n) = d(n) - w(n) * X(n)
        self.y = 0
        self.e = 0

    def __update_X(self, x): # __func(): private method
        self.X = [x] + self.X[:-1] # update X(n)

    def train(self, x, d): 
        self.__update_X(x) 
        self.P = (Matrix([self.X]) * self.Q)[0]
        self.factor_k = 1 / (self.lambda_ + sum([p_ * x_ for (p_, x_) in list(zip(self.P, self.X))]))
        self.k = [self.factor_k * p_ for p_ in self.P]
        self.factor_Q = (1 / self.lambda_)
        self.Q = self.factor_Q * (self.Q - self.factor_k * (Matrix([self.P]).T() * Matrix([self.P])) )
        self.alpha = d - sum([w_ * x_ for (w_, x_) in list(zip(self.w, self.X))])
        self.w = [w_ + self.alpha * k_ for (w_, k_) in list(zip(self.w, self.k))]
        # optional: e(n) := d(n) - y(n) = d(n) - w(n) * X(n)
        self.y = sum([w_ * x_ for (w_, x_) in list(zip(self.w, self.X))])
        self.e = d - self.y
        

    def predict(self, list_x):
        # remain: w, X, y; other set init
        self.Q, self.k, self.alpha, self.e = self.delta * Eye(self.N), [0] * self.N, 0, 0
        list_y = []
        for x in list_x:
            self.__update_X(x)
            self.y = sum([w_ * x_ for (w_, x_) in list(zip(self.w, self.X))])
            list_y.append(self.y)
        return list_y



if __name__ == "__main__":
    from math import sin, cos, pi
    import numpy as np
    import matplotlib.pyplot as plt
    #############################################################################
    T = 5e3
    length = 50000   
    noise_ord = 0.3 * np.random.randn( length ) # Generate Gaussian noise
    list_x = [n for n in noise_ord]
    noise = [0] * 6  + [n for n in noise_ord[:-6]]
    list_d = [sin(2 * pi * ind/T) + noise[ind] for ind in range(length)]
    list_y, list_e = [], []
    N = 11
    # not work: print("threshold of lambda = ", 1-1/(2*N) )
    rls = Rls(delta=2, lambda_=0.9998, N=N) # 0.9998
    rls.X = list_x[N-2::-1] + [0]   
    for x, d in list(zip(list_x[N-1:], list_d[N-1:])):
        rls.train(x, d)
        list_y.append(rls.y)
        list_e.append(rls.e)     
    plt.plot(list_d[N-1:], 'r-')
    plt.plot(list_e, 'k-')
    plt.show()
    import sys
    sys.path.append("./")
    from iir_filter.fft1d import plot_spectrum, fft
    plot_spectrum(list_d, 30e3, path_fig="./d(n).png", str_title="original d(n)")
    plot_spectrum(list_e, 30e3, path_fig="./e(n).png", str_title="filtered e(n)")
    print(rls.Q, '\n')
    print(rls.w)
    # del list_d, list_e, list_x, noise, noise_ord, rls
    #############################################################################  
    # T = 10
    # length = 1000
    # list_x = [sin((2*pi/T)*ind) for ind in range(length)]
    # list_d = [cos((2*pi/T)*ind) for ind in range(length)]
    # list_y, list_e = [], []
    # N = 5 
    # rls = Rls(delta=2, lambda_=0.999, N=N)
    # rls.X = list_x[N-2::-1] + [0]
    # for x, d in list(zip(list_x[N-1:], list_d[N-1:])):
    #     rls.train(x, d)
    #     list_y.append(rls.y)
    #     list_e.append(rls.e)
    # plt.plot(list_d[N-1:], 'r-')
    # plt.plot(list_e, 'k-')
    # plt.show()
    # print(rls.Q, '\n')
    # print(rls.w)
