from math import cos, acos, pi
class Freq_track(object):
    def __init__(self, mu, r, theta_0=pi/2):
        self.mu = mu # learning rate
        self.r = r
        self.c = cos(theta_0)
        self.X = [0, 0, 0] # x(n), x(n-1), x(n-2)
        self.Y = [0, 0]    # y(n-1), y(n-2)
        self.Beta = [0, 0] # beta := dy/dc; beta(n-1), beta(n-2)
        # optional: coeffs for x(n), y(n)
        self.coef_x = [1, -2 * self.c, 1]
        self.coef_y = [2 * self.r * self.c , - self.r * self.r]
        self.coef_x_beta = [0, -2, 0]
        self.coef_y_beta = [2 * self.r, 0]
    def get_theta(self):
        return acos(self.c)
    def __update_X(self, x): # __func(): private method
        self.X = [x] + self.X[:-1] # update X(n)
    def __update_Y_Beta(self, y, beta):
        self.Y = [y] + self.Y[:-1]
        self.Beta = [beta] + self.Beta[:-1]
    def __clip_c(self):
        if self.c > 1:
            self.c = 1
        elif self.c < -1:
            self.c = -1
    def __update_coef(self):
        self.coef_x = [1, -2 * self.c, 1]
        self.coef_y = [2 * self.r * self.c , - self.r * self.r]
        self.coef_x_beta = [0, -2, 0]
        self.coef_y_beta = [2 * self.r, 0]
    def train(self, x):
        self.__update_X(x) 
        # calc old y(n), beta(n)
        y_old = sum([coef_ * x_ for coef_, x_ in list(zip(self.coef_x, self.X))]) \
            + sum([coef_ * y_ for coef_, y_ in list(zip(self.coef_y, self.Y))])
        beta_old = sum([coef_ * x_ for coef_, x_ in list(zip(self.coef_x_beta, self.X))]) \
            + sum([coef_ * y_ for coef_, y_ in list(zip(self.coef_y_beta, self.Y))]) \
            + sum([coef_ * b_ for coef_, b_ in list(zip(self.coef_y, self.Beta))])
        # update self.c := cos(theta)
        self.c = self.c - 2 * self.mu * y_old * beta_old
        self.__clip_c()
        self.__update_coef()
        # calc new y(n), beta(n) with new self.c
        y = sum([coef_ * x_ for coef_, x_ in list(zip(self.coef_x, self.X))]) \
            + sum([coef_ * y_ for coef_, y_ in list(zip(self.coef_y, self.Y))])
        beta = sum([coef_ * x_ for coef_, x_ in list(zip(self.coef_x_beta, self.X))]) \
            + sum([coef_ * y_ for coef_, y_ in list(zip(self.coef_y_beta, self.Y))]) \
            + sum([coef_ * b_ for coef_, b_ in list(zip(self.coef_y, self.Beta))])
        self.__update_Y_Beta(y, beta)


if __name__ == "__main__":
    from math import sin
    import matplotlib.pyplot as plt
    fs, f = 8000, 1000
    N = 10 * fs # 10 second duration
    list_x = [sin(2*pi * (f/fs) * ind) for ind in range(N)]
    #######################################################
    mu, r, theta_0 = 7e-4, 0.95, pi/2
    freq_track = Freq_track(mu=mu, r=r, theta_0=theta_0)
    list_freq = []
    for x in list_x:
        freq_track.train(x)
        omega = freq_track.get_theta()
        list_freq.append( fs * omega / (2 * pi) )
    #######################################################
    fig = plt.figure()
    plt.plot(list_freq)
    plt.xlabel("Time index n")
    plt.ylabel("Frequency (Hz)")
    plt.title(r"Frequency tracking: $f=f_s \times \frac{\theta}{2\pi}$")
    ax = plt.gca()
    ax.set_xlim([0, N])
    plt.grid()
    plt.tight_layout()
    fig.savefig("../p9_28.png")
    plt.show()
    #######################################################