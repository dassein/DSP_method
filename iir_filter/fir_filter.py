'''
difference equation
y(n) = x(n) + x(n-1) + ... + x(n-N+1)
'''
try:
    from iir_filter.poly import Polyz
except ModuleNotFoundError:
    from poly import Polyz

def fir_filter(in_put, list_filter): 
    if isinstance(list_filter, list):
        pass
    elif isinstance(list_filter, Polyz):
        list_filter = list_filter.coeffs
    else:
        raise Exception("list_filter should be list or Polyz")
    length = len(in_put)
    N = len(list_filter)
    list_filter_flip = list(reversed(list_filter))
    out_put = []
    for index in range(length):
        if index + 1 < N:
            list_coef = list_filter_flip[N-1-index: ]
            list_input = in_put[0: index+1] # length: index+1
            out_put.append(sum([coef * item for (coef, item) in list(zip(list_coef, list_input))]))
        else:
            list_input = in_put[index-N+1: index+1] # length: N
            out_put.append(sum([coef * item for (coef, item) in list(zip(list_filter_flip, list_input))]))
    return out_put


if __name__ == "__main__":
    in_put = [1, 2, 3, 4, 5]
    list_filter = [2, 3, 1]
    out_put = fir_filter(in_put, list_filter)
    print(out_put)



