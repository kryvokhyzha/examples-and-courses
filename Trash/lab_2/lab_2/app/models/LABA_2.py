import pandas as pd
import numpy as np
import scipy.optimize as optimize
from scipy.linalg import solve
from scipy.sparse.linalg import cg
from copy import deepcopy
from scipy import special
from numpy.polynomial import Polynomial as pm
from tabulate import tabulate as tb
from os import name as os_name

import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode
import plotly.offline as offline
from plotly import tools
init_notebook_mode(connected=True)


def prepare_x(x):
    x = [list(x[i]) for i in range(len(x))]
    for i in range(len(x)):
        for j in range(len(x[i])):
            x[i][j] = round(x[i][j], 4)
    return x

# Define Conjugate Gradient Method
def conjugate_gradient_method(A, b, eps):
    cgrad = np.matrix(cg(A, b, tol=eps)[0]).reshape(-1,1)
    return cgrad

# Defining all types of polinoms
def basis_sh_chebyshev(degree):
    basis = [pm([-1, 2]), pm([1])]
    for i in range(degree):
        basis.append(pm([-2, 4])*basis[-1] - basis[-2])
    del basis[0]
    return basis


def basis_sh_legendre(degree):
    basis = [pm([1])]
    for i in range(degree):
        if i == 0:
            basis.append(pm([-1, 2]))
            continue
        basis.append((pm([-2*i - 1, 4*i + 2])*basis[-1] - i * basis[-2]) / (i + 1))
    return basis


def basis_hermite(degree):
    basis = [pm([0]), pm([1])]
    for i in range(degree):
        basis.append(pm([0,2])*basis[-1] - 2 * i * basis[-2])
    del basis[0]
    return basis


def basis_laguerre(degree):
    basis = [pm([1])]
    for i in range(degree):
        if i == 0:
            basis.append(pm([1, -1]))
            continue
        basis.append(pm([2*i + 1, -1])*basis[-1] - i * i * basis[-2])
    return basis


# Function for polinom to text
class _Polynom(object):
    def __init__(self, ar, symbol = 'x',eps = 1e-15):
        self.ar = ar
        self.symbol = symbol
        self.eps = eps

    def __repr__(self):
        #joinder[first, negative] = str
        joiner = {
            (True, True):'-',
            (True, False): '',
            (False, True): ' - ',
            (False, False): ' + '
        }

        result = []
        for deg, coef in reversed(list(enumerate(self.ar))):
            sign = joiner[not result, coef < 0]
            coef  = abs(coef)
            if coef == 1 and deg != 0:
                coef = ''
            if coef < self.eps:
                continue
            f = {0: '{}{}', 1: '{}{}'+self.symbol}.get(deg, '{}{}'+ self.symbol +'^{}')
            result.append(f.format(sign, coef, deg))
        return ''.join(result) or '0'


# Solver itself
class Solve(object):

    def __init__(self,d):
        self.n = d['samples']
        self.deg = d['dimensions']
        self.filename_input = d['input_file']
        self.filename_output = d['output_file']
        self.dict = d['output_file']
        self.p = list(map(lambda x:x+1,d['degrees'])) # on 1 more because include 0
        self.weights = d['weights']
        self.poly_type = d['poly_type']
        self.splitted_lambdas = d['lambda_multiblock']
        self.eps = 1E-6
        self.norm_error=0.0
        self.error=0.0
        self.method = d['method']

    def define_data(self):
        f = open(self.filename_input, 'r')
        # all data from file_input in float
        self.datas = np.matrix([list(map(lambda x:float(x),f.readline().split())) for i in range(self.n)])
        # list of sum degrees [ 3,1,2] -> [3,4,6]
        self.degf = [sum(self.deg[:i + 1]) for i in range(len(self.deg))]

    def _minimize_equation(self, A, b):
        if self.method == 'lsq':
            return np.linalg.lstsq(A,b)[0]
        elif self.method == 'cjg':
            #print(np.linalg.det(A.T*A))
            return conjugate_gradient_method(A.T*A, A.T*b, self.eps)

    def norm_data(self):
        n,m = self.datas.shape
        vec = np.ndarray(shape=(n,m),dtype=float)
        for j in range(m):
            minv = np.min(self.datas[:,j])
            maxv = np.max(self.datas[:,j])
            for i in range(n):
                vec[i,j] = (np.array(self.datas[i,j]) - minv)/(maxv - minv)
        self.data = np.matrix(vec)

    def define_norm_vectors(self):
        X1 = self.data[:, :self.degf[0]]
        X2 = self.data[:, self.degf[0]:self.degf[1]]
        X3 = self.data[:, self.degf[1]:self.degf[2]]
        #matrix of vectors i.e.X = [[X11,X12],[X21],...]
        self.X = [X1, X2, X3]
        #number columns in matrix X
        self.mX = self.degf[2]
        # matrix, that consists of i.e. Y1,Y2
        self.Y = self.data[:, self.degf[2]:self.degf[3]]
        self.Y_ = self.datas[:, self.degf[2]:self.degf[3]]
        self.X_ = [self.datas[:, :self.degf[0]], self.datas[:,self.degf[0]:self.degf[1]],
                   self.datas[:, self.degf[1]:self.degf[2]]]

    def built_B(self):
        def B_average():
            b = np.tile((self.Y.max(axis=1) + self.Y.min(axis=1))/2,(1,self.deg[3]))
            return b

        def B_scaled():
            return deepcopy(self.Y)

        if self.weights == 0:
            self.B = B_average()
        elif self.weights ==1:
            self.B = B_scaled()
        else:
            exit('B not definded')

    def poly_func(self):
        if self.poly_type == 0:
            self.poly_f = special.eval_sh_chebyt
        elif self.poly_type == 1:
            self.poly_f = special.eval_sh_legendre
        elif self.poly_type == 2:
            self.poly_f = special.eval_laguerre
        elif self.poly_type == 3:
            self.poly_f = special.eval_hermite

    def built_A(self):
        def mA():
            m = 0
            for i in range(len(self.X)):
                m+= self.X[i].shape[1]*(self.p[i]+1)
            return m

        def coordinate(v,deg):
            c = np.ndarray(shape=(self.n,1), dtype = float)
            for i in range(self.n):
                c[i,0] = self.poly_f(deg, v[i])
            return c

        def vector(vec, p):
            n, m = vec.shape
            a = np.ndarray(shape=(n,0),dtype = float)
            for j in range(m):
                for i in range(p):
                    ch = coordinate(vec[:,j],i)
                    a = np.append(a,ch,1)
            return a
        A = np.ndarray(shape = (self.n,0),dtype =float)
        for i in range(len(self.X)):
            vec = vector(self.X[i],self.p[i])
            A = np.append(A, vec,1)
        self.A = np.matrix(A)

    def lamb(self):
        lamb = np.ndarray(shape = (self.A.shape[1],0), dtype = float)
        for i in range(self.deg[3]):
            if self.splitted_lambdas:
                boundary_1 = self.p[0] * self.deg[0]
                boundary_2 = self.p[1] * self.deg[1] + boundary_1
                lamb1 = self._minimize_equation(self.A[:, :boundary_1], self.B[:, i])
                lamb2 = self._minimize_equation(self.A[:, boundary_1:boundary_2], self.B[:, i])
                lamb3 = self._minimize_equation(self.A[:, boundary_2:], self.B[:, i])
                lamb = np.append(lamb, np.concatenate((lamb1, lamb2, lamb3)), axis=1)
            else:
                lamb = np.append(lamb, self._minimize_equation(self.A, self.B[:, i]), axis=1)
        self.Lamb = np.matrix(lamb) #Lamb in full events

    def psi(self):
        def built_psi(lamb):
            psi = np.ndarray(shape=(self.n, self.mX), dtype = float)
            q = 0 #iterator in lamb and A
            l = 0 #iterator in columns psi
            for k in range(len(self.X)): # choose X1 or X2 or X3
                for s in range(self.X[k].shape[1]):# choose X11 or X12 or X13
                    for i in range(self.X[k].shape[0]):
                            psi[i,l] = self.A[i,q:q+self.p[k]]*lamb[q:q+self.p[k], 0]
                    q+=self.p[k]
                    l+=1
            return np.matrix(psi)

        self.Psi = [] #as list because psi[i] is matrix(not vector)
        for i in range(self.deg[3]):
            self.Psi.append(built_psi(self.Lamb[:,i]))

    def built_a(self):
        self.a = np.ndarray(shape=(self.mX,0), dtype=float)
        for i in range(self.deg[3]):
            a1 = self._minimize_equation(self.Psi[i][:, :self.degf[0]], self.Y[:, i])
            a2 = self._minimize_equation(self.Psi[i][:, self.degf[0]:self.degf[1]], self.Y[:, i])
            a3 = self._minimize_equation(self.Psi[i][:, self.degf[1]:], self.Y[:, i])
            self.a = np.append(self.a, np.vstack((a1, a2, a3)),axis = 1)

    def built_F1i(self, psi, a):
            m = len(self.X) # m  = 3
            F1i = np.ndarray(shape = (self.n,m),dtype = float)
            k = 0 #point of begining columnt to multipy
            for j in range(m): # 0 - 2
                for i in range(self.n): # 0 - 49
                    F1i[i,j] = psi[i,k:self.degf[j]]*a[k:self.degf[j],0]
                k = self.degf[j]
            return np.matrix(F1i)

    def built_Fi(self):
        self.Fi = []
        for i in range(self.deg[3]):
            self.Fi.append(self.built_F1i(self.Psi[i],self.a[:,i]))

    def built_c(self):
        self.c = np.ndarray(shape = (len(self.X),0),dtype = float)
        for i in range(self.deg[3]):
            self.c = np.append(self.c, conjugate_gradient_method(self.Fi[i].T*self.Fi[i], self.Fi[i].T*self.Y[:,i],self.eps),\
                          axis = 1)

    def built_F(self):
        F = np.ndarray(self.Y.shape, dtype = float)
        for j in range(F.shape[1]):#2
            for i in range(F.shape[0]): #50
                F[i,j] = self.Fi[j][i,:]*self.c[:,j]
        self.F = np.matrix(F)
        self.norm_error = []
        for i in range(self.Y.shape[1]):
            self.norm_error.append(np.linalg.norm(self.Y[:,i] - self.F[:,i],np.inf))

    def built_F_(self):
        minY = self.Y_.min(axis=0)
        maxY = self.Y_.max(axis=0)
        self.F_ = np.multiply(self.F,maxY - minY) + minY
        self.error = []
        for i in range(self.Y_.shape[1]):
            self.error.append(np.linalg.norm(self.Y_[:,i] - self.F_[:,i],np.inf))

#Result output for Maksik


    def show_dict(self):
        res = {}

        x = np.array(self.datas[:, :self.degf[2]])
        res['Input data: X'] = prepare_x(x)

        x = np.array(self.datas[:,self.degf[2]:self.degf[3]])
        res['Input data: Y'] = prepare_x(x)

        x = np.array(self.data[:,:self.degf[2]])
        res['X normalised:'] =  prepare_x(x)

        x = np.array(self.data[:,self.degf[2]:self.degf[3]])
        res['Y normalised:'] = prepare_x(x)

        x = np.array(self.B)
        res['matrix B:'] = prepare_x(x)

        x = np.array(self.A)
        res['matrix A:'] = prepare_x(x)

        x = np.array(self.Lamb)
        res['matrix Lambda:'] = prepare_x(x)

        for j in range(len(self.Psi)):
             s = 'matrix Psi%i:' %(j+1)
             x = np.array(self.Psi[j])
             res[s] = prepare_x(x)

        x = self.a.tolist()
        res['matrix a'] = prepare_x(x)

        for j in range(len(self.Fi)):
             s = 'matrix F%i:' %(j+1)
             x = np.array(self.Fi[j])
             res[s] = prepare_x(x)


        x = np.array(self.c)
        res['matrix c:'] = prepare_x(x)

        x = np.array(self.F)
        res['Y rebuilt normalized :'] = prepare_x(x)

        x = self.F_.tolist()
        res['Y rebuilt :'] = prepare_x(x)

        res['Error normalised (Y - F)'] = [self.norm_error]

        res['Error (Y_ - F_)'] = [self.error]

        return res


    def show(self):
        text = []

        text.append('Input data: X')
        text.append(tb(np.array(self.datas[:, :self.degf[2]])))

        text.append('\nInput data: Y')
        text.append(tb(np.array(self.datas[:,self.degf[2]:self.degf[3]])))

        text.append('\nX normalised:')
        text.append(tb(np.array(self.data[:,:self.degf[2]])))

        text.append('\nY normalised:')
        text.append(tb(np.array(self.data[:,self.degf[2]:self.degf[3]])))

        text.append('\nmatrix B:')
        text.append(tb(np.array(self.B)))

        text.append('\nmatrix A:')
        text.append(tb(np.array(self.A)))

        text.append('\nmatrix Lambda:')
        text.append(tb(np.array(self.Lamb)))

        for j in range(len(self.Psi)):
             s = '\nmatrix Psi%i:' %(j+1)
             text.append(s)
             text.append(tb(np.array(self.Psi[j])))

        text.append('\nmatrix a:')
        text.append(tb(self.a.tolist()))

        for j in range(len(self.Fi)):
             s = '\nmatrix F%i:' %(j+1)
             text.append(s)
             text.append(tb(np.array(self.Fi[j])))

        text.append('\nmatrix c:')
        text.append(tb(np.array(self.c)))

        text.append('\nY rebuilt normalized :')
        text.append(tb(np.array(self.F)))

        text.append('\nY rebuilt :')
        text.append(tb(self.F_.tolist()))

        text.append('\nError normalised (Y - F)')
        text.append(tb([self.norm_error]))

        text.append('\nError (Y_ - F_))')
        text.append(tb([self.error]))

        return '\n'.join(text)

    def prepare(self):
        self.define_data()
        self.norm_data()
        self.define_norm_vectors()
        self.built_B()
        self.poly_func()
        self.built_A()
        self.lamb()
        self.psi()
        self.built_a()
        self.built_Fi()
        self.built_c()
        self.built_F()
        self.built_F_()



# Visualisation results module :)
class PolynomialBuilder(object):
    def __init__(self, solution):
        assert isinstance(solution, Solve)
        self._solution = solution
        max_degree = max(solution.p) - 1
        if solution.poly_type == 0:
            self.symbol = 'T'
            self.basis = basis_sh_chebyshev(max_degree)
        elif solution.poly_type == 1:
            self.symbol = 'P'
            self.basis = basis_sh_legendre(max_degree)
        elif solution.poly_type == 2:
            self.symbol = 'L'
            self.basis = basis_laguerre(max_degree)
        elif solution.poly_type == 3:
            self.symbol = 'H'
            self.basis = basis_hermite(max_degree)
        self.a = solution.a.T.tolist()
        self.c = solution.c.T.tolist()
        self.minX = [X.min(axis=0).getA1() for X in solution.X_]
        self.maxX = [X.max(axis=0).getA1() for X in solution.X_]
        self.minY = solution.Y_.min(axis=0).getA1()
        self.maxY = solution.Y_.max(axis=0).getA1()

    def _form_lamb_lists(self):
        """
        Generates specific basis coefficients for Psi functions
        """
        self.psi = list()
        for i in range(self._solution.Y.shape[1]):  # `i` is an index for Y
            psi_i = list()
            shift = 0
            for j in range(3):  # `j` is an index to choose vector from X
                psi_i_j = list()
                for k in range(self._solution.deg[j]):  # `k` is an index for vector component
                    psi_i_jk = self._solution.Lamb[shift:shift + self._solution.p[j], i].getA1()
                    shift += self._solution.p[j]
                    psi_i_j.append(psi_i_jk)
                psi_i.append(psi_i_j)
            self.psi.append(psi_i)

    def _transform_to_standard(self, coeffs):
        """
        Transforms special polynomial to standard
        :param coeffs: coefficients of special polynomial
        :return: coefficients of standard polynomial
        """
        std_coeffs = np.zeros(coeffs.shape)
        for index in range(coeffs.shape[0]):
            cp = self.basis[index].coef.copy()
            cp.resize(coeffs.shape)
            std_coeffs += coeffs[index] * cp
        return std_coeffs

    def _print_psi_i_jk(self, i, j, k):
        """
        Returns string of Psi function in special polynomial form
        :param i: an index for Y
        :param j: an index to choose vector from X
        :param k: an index for vector component
        :return: result string
        """
        strings = list()
        for n in range(len(self.psi[i][j][k])):
            strings.append('{0:.6f}*{symbol}{deg}(x{1}{2})'.format(self.psi[i][j][k][n], j + 1, k + 1,
                                                                   symbol=self.symbol, deg=n))
        return ' + '.join(strings)

    def _print_phi_i_j(self, i, j):
        """
        Returns string of Phi function in special polynomial form
        :param i: an index for Y
        :param j: an index to choose vector from X
        :return: result string
        """
        strings = list()
        for k in range(len(self.psi[i][j])):
            shift = sum(self._solution.deg[:j]) + k
            for n in range(len(self.psi[i][j][k])):
                strings.append('{0:.6f}*{symbol}{deg}(x{1}{2})'.format(self.a[i][shift] * self.psi[i][j][k][n],
                                                                       j + 1, k + 1, symbol=self.symbol, deg=n))
        return ' + '.join(strings)

    def _print_F_i(self, i):
        """
        Returns string of F function in special polynomial form
        :param i: an index for Y
        :return: result string
        """
        strings = list()
        for j in range(3):
            for k in range(len(self.psi[i][j])):
                shift = sum(self._solution.deg[:j]) + k
                for n in range(len(self.psi[i][j][k])):
                    strings.append('{0:.6f}*{symbol}{deg}(x{1}{2})'.format(self.c[i][j] * self.a[i][shift] *
                                                                           self.psi[i][j][k][n],
                                                                           j + 1, k + 1, symbol=self.symbol, deg=n))
        return ' + '.join(strings)

    def _print_F_i_transformed_denormed(self, i):
        """
        Returns string of F function in special polynomial form
        :param i: an index for Y
        :return: result string
        """
        strings = list()
        constant = 0
        for j in range(3):
            for k in range(len(self.psi[i][j])):
                shift = sum(self._solution.deg[:j]) + k
                raw_coeffs = self._transform_to_standard(self.c[i][j] * self.a[i][shift] * self.psi[i][j][k])
                diff = self.maxX[j][k] - self.minX[j][k]
                mult_poly = np.poly1d([1 / diff, - self.minX[j][k]] / diff)
                add_poly = np.poly1d([1])
                current_poly = np.poly1d([0])
                for n in range(len(raw_coeffs)):
                    current_poly += add_poly * raw_coeffs[n]
                    add_poly *= mult_poly
                current_poly = current_poly * (self.maxY[i] - self.minY[i]) + self.minY[i]
                constant += current_poly[0]
                current_poly[0] = 0
                current_poly = np.poly1d(current_poly.coeffs, variable='(x{0}{1})'.format(j + 1, k + 1))
                strings.append(str(_Polynom(current_poly, '(x{0}{1})'.format(j + 1, k + 1))))
        strings.append(str(constant))
        return ' +\n'.join(strings)

    def _print_F_i_transformed(self, i):
        """
        Returns string of F function in special polynomial form
        :param i: an index for Y
        :return: result string
        """
        strings = list()
        constant = 0
        for j in range(3):
            for k in range(len(self.psi[i][j])):
                shift = sum(self._solution.deg[:j]) + k
                current_poly = np.poly1d(self._transform_to_standard(self.c[i][j] * self.a[i][shift] *
                                                                     self.psi[i][j][k])[::-1],
                                         variable='(x{0}{1})'.format(j + 1, k + 1))
                constant += current_poly[0]
                current_poly[0] = 0
                strings.append(str(_Polynom(current_poly, '(x{0}{1})'.format(j + 1, k + 1))))
        strings.append(str(constant))
        return ' +\n'.join(strings)

    def _print_F_i_c(self, i): # новая функция
        """
        :param i: an index for Y
        """
        strings = list()
        for j in range(3):
            strings.append('{0:.6f}*{symbol}{deg}(x{1})'.format(self.c[i][j], j + 1, symbol='F', deg=str(i+1)+str(j+1)))
        return ' + '.join(strings)


    def get_results(self):
        self._form_lamb_lists()
        psi_strings = ['(Psi{1}{2})[{0}]={result}\n'.format(i + 1, j + 1, k + 1, result=self._print_psi_i_jk(i, j, k))
                       for i in range(self._solution.Y.shape[1])
                       for j in range(3)
                       for k in range(self._solution.deg[j])]
        phi_strings = ['(Phi{1})[{0}]={result}\n'.format(i + 1, j + 1, result=self._print_phi_i_j(i, j))
                       for i in range(self._solution.Y.shape[1])
                       for j in range(3)]
        f_strings = ['(F{0})={result}\n'.format(i + 1, result=self._print_F_i(i))
                     for i in range(self._solution.Y.shape[1])]
        f_strings_transformed = ['(F{0}) transformed:\n{result}\n'.format(i + 1, result=self._print_F_i_transformed(i))
                                 for i in range(self._solution.Y.shape[1])]
        f_strings_transformed_denormed = ['(F{0}) transformed ' \
                                          'denormed:\n{result}\n'.format(i + 1, result=
        self._print_F_i_transformed_denormed(i))
                                          for i in range(self._solution.Y.shape[1])]
        f_strings_F_i_c = ['(F{0})={result}\n'.format(i + 1, result=self._print_F_i_c(i))
                     for i in range(self._solution.Y.shape[1])] # новая строка
        return '\n'.join(psi_strings + phi_strings + f_strings + f_strings_transformed + f_strings_transformed_denormed + f_strings_F_i_c) # обновлена строка

    def plot_graphs(self, path):
        for index in range(self._solution.Y.shape[1]):
            x = np.arange(1, self._solution.n + 1)
            y = np.array(self._solution.Y_[:, index]).flatten()
            solution_y = go.Scatter(
                x=x, y=y, mode='lines',
                name='Y{}'.format(index + 1))
            f = np.array(self._solution.F_[:, index]).flatten()
            solution_f = go.Scatter(
                x=x, y=f, mode='lines',
                name='F{}'.format(index + 1))
            r = np.array(abs(self._solution.Y_[:, index] - self._solution.F_[:, index])).flatten()
            solution_r = go.Scatter(
                x=x, y=r, mode='lines',
                name='Residual {}'.format(index + 1))

            fig = tools.make_subplots(
                rows=2, cols=1, specs=[[{}], [{}]],
                shared_xaxes=True, shared_yaxes=True,
                vertical_spacing=0.001)
            fig.append_trace(solution_y, 1, 1)
            fig.append_trace(solution_f, 1, 1)
            fig.append_trace(solution_r, 2, 1)

            fig['layout'].update(xaxis=dict(title='x'),title='Coordinate {0}'.format(index + 1), barmode='overlay')
            offline.plot(fig, filename=path+'graph_'+str(index)+'.html')
