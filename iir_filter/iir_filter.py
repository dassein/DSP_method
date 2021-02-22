try:
    from iir_filter.frac import Frac
    from iir_filter.poly import Polyz
except ModuleNotFoundError:
    from frac import Frac
    from poly import Polyz

def iir_filter(list_input, H_z): # H_z = ( \sum b_k * z^{-k} ) / ( \sum a_k * z^{-k} )
    A = H_z.den.coeffs # a_k
    B = H_z.num.coeffs # b_k
    A = [-elem for ind, elem in enumerate(A[1:])] # - a_k
    len_A, len_B = len(A)+1, len(B)
    buffer_length = max(len_A, len_B)
    W = [0] * buffer_length
    list_output = [0] * len(list_input)
    for ind, x in enumerate(list_input): # x[n]
        W[0] = sum([a*w for a, w in list(zip(A, W[1:len_A]))]) + x # w[n] = -\sum a_k * w[n-k] + x[n]
        list_output[ind] = sum([b*w for b, w in list(zip(B, W[0:len_B]))]) # y[n] = \sum b_k * w[n-k]
        W[1:] = W[0:-1] # update w[n]
    return list_output

if __name__ == "__main__":
    H_z = Frac(Polyz([1, -1]), Polyz([1, 1])) # H_z = (1 - z^{-1}) / (1 + z^{-1})
    print(H_z)
    list_input = [1, 2, 3, 4, 5, 6, 7] # x[n]
    list_output = iir_filter(list_input, H_z) # y[n]
