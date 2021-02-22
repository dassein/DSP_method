'''
define fraction: numerator, denominator
'''
try:
    from iir_filter.poly import Poly, Polyz, Iterable
except ModuleNotFoundError:
    from poly import Poly, Polyz, Iterable

class Frac(object):
    def __init__(self, *args):
        """
        Create a Poly in one of three ways:
        f = Frac([1, 2], [2, 3])
        f = Frac([1, 2], poly1)  # poly1 = Poly([1, 2, 3])
        """
        super(Frac,self).__init__()
        if len(args)==2:
            num = args[0]
            den = args[1]
            if isinstance(num, Poly):                # copy constructor
                pass
            elif isinstance(num, Iterable):    # from sequence  elif isinstance(val, collections.Iterable):
                num = Poly(num)
            else:                                          # from single scalar
                raise Exception("Frac init fails")
            if isinstance(den, Poly):                # copy constructor
                pass
            elif isinstance(den, Iterable):    # from sequence  elif isinstance(val, collections.Iterable):
                den = Poly(den)
            else:                                          # from single scalar
                raise Exception("Frac init fails")
            self.num = num
            self.den = den
        elif len(args)==1 and isinstance(args[0], Frac):
            self.num = args[0].num
            self.den = args[0].den
        else:                                             
            raise Exception("Frac init fails")
    def __call__(self, val):
        if self.den(val) < 1e-7:
            raise Exception("pole at " + str(val))
        return self.num(val) / self.den(val)
    def __str__(self):
        return "[ " + "( " + str(self.num) + " ) / ( " + str(self.den) + " )" + " ]"
    def __mul__(self, val):
        "Return self*val"
        num = self.num
        den = self.den
        if isinstance(val, Frac):
            num = num * val.num
            den = den * val.den
        elif isinstance(val, Poly):
            num = num * val
        elif isinstance(val, (int, float, bool)):
            num = num * val
        else:
            raise Exception("multiplier is wrong")
        return self.__class__(num, den)
    def __rmul__(self, val):
        "Return val*self"
        return self*val
    def __repr__(self):
        return self.__str__()
        # return "{0}({1}, {2})".format(self.__class__.__name__, self.num.coeffs, self.den.coeffs)
    def simplify(self):
        if self.den == Poly([0]):
            raise Exception("denominator cannot be 0")
        if isinstance(self.den, Polyz):
            factor = 1 / self.den.coeffs[0]  # 1 + z^(-1) + ...
        else:
            factor = 1 / self.den.coeffs[-1] # s^n + s^(n-1) + ...
        self.num = self.num * factor
        self.den = self.den * factor
    def subs(self, val):
        list_coef_num = self.num.coeffs
        list_coef_den = self.den.coeffs
        deg_num = len(list_coef_num) - 1
        deg_den = len(list_coef_den) - 1
        deg = max(deg_num, deg_den)
        num_val, den_val = val.num, val.den
        num_new, den_new = num_val.__class__([0]), den_val.__class__([0])
        for ind, coef in enumerate(list_coef_num):
            num_new = num_new + coef * (num_val ** ind) * (den_val ** (deg-ind))
        for ind, coef in enumerate(list_coef_den):
            den_new = den_new + coef * (num_val ** ind) * (den_val ** (deg-ind))
        # self.num = num_new
        # self.den = den_new
        # self.simplify()
        Frac_new = self.__class__(num_new, den_new)
        Frac_new.simplify()
        return Frac_new


def convert_s2z(frac, f_sample):
    frac_subs = Frac(2*f_sample*Polyz([1, -1]), Polyz([1, 1]))
    return frac.subs(frac_subs)


if __name__ == "__main__":
    f1 = Frac([2, 3], [1, 2])
    print(f1)
    f2 = 3 * f1 * 5
    print(f2)
    print(f1 * f2)
    print(repr(f1 * f2))
    f3 = f1 * f2
    f3.simplify()
    print(f3)
    f4 = Frac([1], [1, 0.7654, 1])
    f4_new = f4.subs(Frac(Polyz([0, 1]), Polyz([2.3946e4])))
    print(f4_new)
    f5 = Frac(f4_new)
    print(f5)

    f6 = Frac([0, 1], [1.9656e4, 1])
    print(f6)
    f6_new = f6.subs(Frac(16e3 * Polyz([1, -1]), Polyz([1, 1])))
    print(f6_new)
    print(convert_s2z(f6, 8e3))
