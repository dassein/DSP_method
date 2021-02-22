from rls.lms import Lms
from rls.rls import Rls
def convert(L, n):
    if isinstance(L, (float, int)):
        return round(L, n)
    list_new = []
    for elem in L:
        list_new.append(convert(elem, n))
    return list_new

def print_approx(L, n=6):
    L_new = convert(L, n)
    print(L_new)

list_x = [2, -4, 4, -2]
list_d = [1, -1, 0, 1]
#####################
# RLS adaptive filter
#####################
delta, lambda_, N = 1, 0.96, 2
rls = Rls(delta, lambda_, N) # initial w = [0, ..., 0]
list_y, list_e, list_alpha, list_w,  = [], [], [], [[0] * N]
for x, d in list(zip(list_x, list_d)):
    rls.train(x, d)
    list_y.append(rls.y)
    list_e.append(rls.e)
    list_alpha.append(rls.alpha)
    list_w.append(rls.w)
    print_approx(rls.Q)
    print_approx(rls.k)
print('\n')
print_approx(list_y)
print_approx(list_e)
print_approx(list_alpha)
print_approx(list_w)
print('\n')