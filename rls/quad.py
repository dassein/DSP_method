try:
    from rls.matrix import Matrix
except ModuleNotFoundError:
    from matrix import Matrix

class Quad(object):
    def __init__(self, R, P, sq_sigma, mu, w_0=None):
        if isinstance(R, Matrix):
            self.R = R
        elif isinstance(R, list):
            row = len(R)
            col = len(R[0])
            if row != col:
                raise Exception("R must be n x n matrix")
            self.R = Matrix(R)
        if self.R.T() != self.R:
            raise Exception("R must by symmetric matrix")
        if len(R) != len(P):
            raise Exception("R, P must have the same length")
        self.P = P
        self.sq_sigma = sq_sigma
        self.mu = mu
        if w_0 == None:
            w_0 = [0] * len(P)
        self.w = w_0
        self.__update_grad()

    def __update_grad(self):
        temp = (Matrix([self.w]) * self.R)[0]
        self.grad = [2*(t_ - p_) for t_, p_ in list(zip(temp, self.P))]

    def train(self):
        self.w = [w_ - self.mu * grad_ for w_, grad_ in list(zip(self.w, self.grad))]
        self.__update_grad()
    
    def eval(self, w_eval=None):
        if w_eval == None:
            w_eval = self.w # default func(self.w)
        if len(w_eval) != len(self.w):
            raise Exception("w_eval and self.w have the same length")
        temp = (Matrix([w_eval]) * self.R)[0]
        temp = [temp_ - 2 * p_ for temp_, p_ in list(zip(temp, self.P))]
        return sum([temp_ * w_ for temp_, w_ in list(zip(temp,  w_eval))]) + self.sq_sigma

if __name__ == "__main__":
    R, P, sq_sigma = [[100, 5], [5, 4]], [50, 4], 100
    mu, w_0 = 0.001, [0, 0]
    quad = Quad(R, P, sq_sigma, mu, w_0)
    list_w = [w_0]
    for ind in range(500):
        quad.train()
        list_w.append( quad.w )
    list_w = list(map(list, zip(*list_w))) # transpose: (n, 2) => (2, n)
    print(quad.w)  # w*: minima point
    print(quad.eval()) # J(w*): min value
    #######################################
    # plot Trajectory of w
    #######################################
    import matplotlib.pyplot as plt 
    import numpy as np
    xlist = np.linspace(0, 0.9, 100)
    ylist = np.linspace(0, 2, 100)
    X, Y = np.meshgrid(xlist, ylist)
    row, col = len(ylist), len(xlist)
    Z = [[ quad.eval([X[n_row][n_col], Y[n_row][n_col]]) for n_col in range(col)] \
        for n_row in range(row)]
    fig, ax = plt.subplots(1, 1)
    cp = ax.contourf(X, Y, Z)
    ax.clabel(cp, colors = 'k', fmt = '%2.1f', fontsize=12)
    fig.colorbar(cp) # Add a colorbar to a plot
    ax.set_title(r'Trajectory of $w=[w_0, w_1]^T$')
    ax.set_xlabel(r'$w_0$')
    ax.set_ylabel(r'$w_1$')
    ax.plot(list_w[0], list_w[1], 'r')
    fig.savefig("../p9_23.png")
    plt.show()
    