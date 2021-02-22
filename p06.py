from rls.lms import Lms
from rls.rls import Rls
list_x = [-0.5, 1.2, 0.5]
list_d = [-1, 2, 1]
#####################
# LMS adaptive filter
#####################
N, mu, w_0 = 2, 0.1, [0.5, -0.5]
lms = Lms(mu, N, w_0)
list_y, list_e, list_w = [], [], [w_0]
for x, d in list(zip(list_x, list_d)):
    lms.train(x, d)
    list_y.append(lms.y)
    list_e.append(lms.e)
    list_w.append(lms.w)
print(list_y)
print(list_e)
print(list_w)
print('\n')