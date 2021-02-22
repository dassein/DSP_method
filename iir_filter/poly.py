'''
implement polynomial
'''
import collections
try:
    from collections.abc import Iterable
except ModuleNotFoundError:
    from collections import Iterable
import itertools

class Poly(object):
    def __init__(self, *args):
        """
        Create a Poly in one of three ways:

        p = Poly(poly)           # copy constructor
        p = Poly([1,2,3 ...])    # from sequence
        p = Poly(1, 2, 3 ...)    # from scalars
        """
        super(Poly,self).__init__()
        if len(args)==1:
            val = args[0]
            if isinstance(val, Poly):                # copy constructor
                self.coeffs = val.coeffs[:]
            elif isinstance(val, Iterable):    # from sequence  elif isinstance(val, collections.Iterable):
                self.coeffs = list(val)
            else:                                          # from single scalar
                self.coeffs = [val+0]
        else:                                              # multiple scalars
            self.coeffs = [i+0 for i in args]
        self.trim()

    def __add__(self, val):
        "Return self+val"
        if isinstance(val, Poly):                    # add Poly
            res = [a+b for a,b in itertools.zip_longest(self.coeffs, val.coeffs, fillvalue=0)]
        else:                                              # add scalar
            if self.coeffs:
                res = self.coeffs[:]
                res[0] += val
            else:
                res = val
        return self.__class__(res)

    def __call__(self, val):
        "Evaluate at X==val"
        res = 0
        pwr = 1
        for co in self.coeffs:
            res += co*pwr
            pwr *= val
        return res

    def __eq__(self, val):
        "Test self==val"
        if isinstance(val, Poly):
            return self.coeffs == val.coeffs
        else:
            return len(self.coeffs)==1 and self.coeffs[0]==val

    def __mul__(self, val):
        "Return self*val"
        if isinstance(val, Poly):
            _s = self.coeffs
            _v = val.coeffs
            res = [0]*(len(_s)+len(_v)-1)
            for selfpow,selfco in enumerate(_s):
                for valpow,valco in enumerate(_v):
                    res[selfpow+valpow] += selfco*valco
        else:
            res = [co*val for co in self.coeffs]
        return self.__class__(res)

    def __neg__(self):
        "Return -self"
        return self.__class__([-co for co in self.coeffs])

    def __pow__(self, y, z=None):
        if not isinstance(y, int):
            raise Exception("pow should be integer")
        if y < 0:
            raise Exception("pow should > 0")
        product = self.__class__([1])
        while y > 0:
            product = product * self
            y = y - 1
        return product

    def _radd__(self, val):
        "Return val+self"
        return self+val

    def __repr__(self):
        return "{0}({1})".format(self.__class__.__name__, self.coeffs)

    def __rmul__(self, val):
        "Return val*self"
        return self*val

    def __rsub__(self, val):
        "Return val-self"
        return -self + val

    def __str__(self):
        "Return string formatted as aX^3 + bX^2 + c^X + d"
        res = []
        for po,co in enumerate(self.coeffs):
            if co:
                if po==0:
                    po = ''
                elif po==1:
                    po = 's'
                else:
                    po = 's^'+str(po)
                res.append(str(round(co, 4))+po)  # keep showing max 4 decimal
        if res:
            res.reverse()
            return ' + '.join(res)
        else:
            return "0"

    def __sub__(self, val):
        "Return self-val"
        return self.__add__(-val)

    def trim(self):
        "Remove trailing 0-coefficients"
        _co = self.coeffs
        if _co:
            offs = len(_co)-1
            if _co[offs]==0:
                offs -= 1
                while offs >= 0 and _co[offs]==0:
                    offs -= 1
                del _co[offs+1:]


class Polyz(Poly):
    def __init__(self, *args):
        Poly.__init__(self, *args)
    def __str__(self):
        res = []
        for po,co in enumerate(self.coeffs):
            if co:
                if po==0:
                    po = ''
                elif po==1:
                    po = 'z^{-1}'
                else:
                    po = 'z^{-'+str(po)+'}'
                res.append(str(round(co, 4))+po)  # keep showing max 4 decimal
        if res:
            return ' + '.join(res)
        else:
            return "0"

if __name__ == "__main__":
    p1 = Poly([1, 2, 3])
    p2 = Poly([2, 3])
    p3 = p1 * p2
    p4 = p1 + p2
    print(p1)
    print(p2)
    print(p3)
    print(p4)
    print(repr(p4))
    print(p2 ** 3)
    p5 = Polyz([1, 2])
    print(p5)
    print(repr(p5))
    p6 = Polyz(p2 ** 3)
    print(p6)
