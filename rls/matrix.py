class Matrix(object):
    def __init__(self, matrix_):
        self.matrix = matrix_

    def __repr__(self):
        return str(self.matrix)

    def __eq__(self, other):
        if isinstance(other, Matrix):
            if self.matrix == other.matrix:
                return True
            return False
        return self.matrix == other

    def __ne__(self, other):
        if isinstance(other, Matrix):
            if self.matrix != other.matrix:
                return True
            return False
        return self.matrix != other

    def __pos__(self):
        return self

    def __neg__(self):
        return self * -1

    def __call__(self, *args):
        matrix_ = self.matrix
        for i in args:
            matrix_ = matrix_[i]

        return matrix_

    def __getitem__(self, item):
        return self.matrix[item]

    def __len__(self):
        return len(self.matrix)

    def __add__(self, other):

        add_ = [[p1 + p2 for p1, p2 in zip(self.matrix[i], other[i])]
                for i in range(len(other))]
        return Matrix(add_)

    def __sub__(self, other):

        sub_ = [[p1 - p2 for p1, p2 in zip(self.matrix[i], other[i])]
                for i in range(len(other))]

        return Matrix(sub_)

    def __mul__(self, other):
        if isinstance(other, Matrix):
            mul_ = [[0] * len(other.matrix[0]) for i in range(len(self.matrix))]

            if len(self.matrix[0]) != len(other.matrix):
                raise Exception('length of matrix A line different than length of matrix B column')

            for i in range(len(self.matrix)):
                for j in range(len(other.matrix[0])):
                    for k in range(len(self.matrix[0])):
                        mul_[i][j] += self.matrix[i][k] * other.matrix[k][j]
        else:
            mul_ = [[p * other for p in self.matrix[i]]
                    for i in range(len(self.matrix))]

        return Matrix(mul_)

    def __truediv__(self, other):
        if isinstance(other, Matrix):
            div_ = [[]]
            print('Division between matrix not implemented yet')
        elif isinstance(other, (int, float)):
            if other == 0 or other == 0.:
                raise Exception("divisor can not be 0")
            div_ = [[p / other for p in self.matrix[i]]
                    for i in range(len(self.matrix))]
            return Matrix(div_)
        else:
            raise Exception("Divisio datatype should be int or float")

    def __rmul__(self, other):
        return self * other
    
    def __pow__(self, order):
        if not isinstance(order, int):
            raise Exception("Matrix pow order should be integer")
        if order <= 0:
            raise Exception("Matrix pow order should be greater than 0")
        if order == 1:
            return self
        else:
            return self.__pow__(order-1) * self

    def __int__(self):
        int_ = [[int(p) for p in self.matrix[i]]
                for i in range(len(self.matrix))]
        return Matrix(int_)

    def __float__(self):
        return self * 1.

    def __str__(self):
        str_ = ''
        max_column = [0] * len(self.matrix[0])

        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                size = len(str(self.matrix[i][j]))
                if size > max_column[j]:
                    max_column[j] = size  # pego o numero com maior numero de caracteres na coluna

        for i in range(len(self.matrix)):
            line = ''
            for j in range(len(self.matrix[i])):
                size = max_column[j] - len(str(self.matrix[i][j]))
                line += ' ' * (size+1)  # coloco um espaco a mais para que nao fique junta da ','
                line += str(self.matrix[i][j])
                line += ','
            str_ += '[' + line[1:-1] + ']\n'  # tiro o primeiro espaco para que fique alinhado com o '[' e a ultima ','

        return str_[:-1]
    
    def T(self): # transpose
        m = self.matrix
        transpose_ = list(map(list, zip(*m)))
        return Matrix(transpose_)


class Eye(Matrix):
    def __init__(self, *args):
        if len(args) == 1:
            if (not isinstance(args[0], int) ) or args[0] <= 0:
                raise Exception("row and col must be positive number")
            col = args[0]
        if len(args) == 2:
            if (not ( isinstance(args[0], int) and isinstance(args[1], int) ) ) \
                or args[0] <= 0 or args[1] <= 0:
                raise Exception("row and col must be positive number")
            col = args[1]
        row = args[0]
        def f(n_row, n_col):
            if n_col != n_row:
                return 0
            else:
                return 1
        matrix_ = [[f(n_row, n_col) for n_col in range(col)] \
                    for n_row in range(row)]
        self.matrix = matrix_
    def __pow__(self, order):
        return super(Eye, self).__pow__(order)

class Ones(Matrix):
    def __init__(self, *args):
        if len(args) == 1:
            if (not isinstance(args[0], int) ) or args[0] <= 0:
                raise Exception("row and col must be positive number")
            col = args[0]
        if len(args) == 2:
            if (not ( isinstance(args[0], int) and isinstance(args[1], int) ) ) \
                or args[0] <= 0 or args[1] <= 0:
                raise Exception("row and col must be positive number")
            col = args[1]
        row = args[0]
        matrix_ = [[1 for n_col in range(col)] \
                 for n_row in range(row)]
        self.matrix = matrix_
    def __pow__(self, order):
        return super(Eye, self).__pow__(order)

class Zeros(Matrix):
    def __init__(self, *args):
        if len(args) == 1:
            if (not isinstance(args[0], int) ) or args[0] <= 0:
                raise Exception("row and col must be positive number")
            col = args[0]
        if len(args) == 2:
            if (not ( isinstance(args[0], int) and isinstance(args[1], int) ) ) \
                or args[0] <= 0 or args[1] <= 0:
                raise Exception("row and col must be positive number")
            col = args[1]
        row = args[0]
        matrix_ = [[0 for n_col in range(col)] \
                 for n_row in range(row)]
        self.matrix = matrix_
    def __pow__(self, order):
        return super(Eye, self).__pow__(order)


if __name__ == "__main__":
    matrix = Matrix([[1, 2],
                    [3, 4]])

    matrix2 = Matrix([[132, 43],
                    [2, -1334343]])

    print('print matrix:', '\n', matrix, '\n')
    print('print matrix:', '\n', matrix2, '\n')
    print('negation operator:', '\n', -matrix, '\n')
    print('add matrix:', '\n', matrix + matrix2, '\n')
    print('mul matrix by a number:', '\n', matrix * 2, '\n')
    print('matrix multiplication:', '\n', matrix * matrix2, '\n')
    print('div matrix by a integer:', '\n', matrix / 2, '\n')
    print('div matrix by a by a float:', '\n', matrix / 2.)
    print('pow matrix by positive pow order', '\n', matrix ** 3)
    print(matrix)
    matrix[0][1] = 1.5
    print(matrix, '\n')
    print(Eye(2, 3), '\n')
    print(Eye(2, 2) ** 3, '\n')
    print(Zeros(2, 3) * Ones(3, 2), '\n')
    print(Matrix([[1, 2]]).T() * Matrix([[3, 4, 5]]))
    '''
    Addition	p1 + p2	p1.__add__(p2)
    Subtraction	p1 - p2	p1.__sub__(p2)
    Multiplication	p1 * p2	p1.__mul__(p2)
    Power	p1 ** p2	p1.__pow__(p2)
    Division	p1 / p2	p1.__truediv__(p2)
    Floor Division	p1 // p2	p1.__floordiv__(p2)
    Remainder (modulo)	p1 % p2	p1.__mod__(p2)
    Bitwise Left Shift	p1 << p2	p1.__lshift__(p2)
    Bitwise Right Shift	p1 >> p2	p1.__rshift__(p2)
    Bitwise AND	p1 & p2	p1.__and__(p2)
    Bitwise OR	p1 | p2	p1.__or__(p2)
    Bitwise XOR	p1 ^ p2	p1.__xor__(p2)
    Bitwise NOT	~p1	p1.__invert__()
    '''