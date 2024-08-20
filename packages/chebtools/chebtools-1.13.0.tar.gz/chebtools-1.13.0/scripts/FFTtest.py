"""
Construct the Chebyshev coefficients from FFT of function values

See: https://www.mathworks.com/matlabcentral/mlc-downloads/downloads/submissions/23972/versions/22/previews/chebfun/examples/approx/html/ChebfunFFT.html

"""
import timeit

import ChebTools, numpy as np#, matplotlib.pyplot as plt

f = lambda x: np.exp(x)*np.sin(np.pi*x) + x

n = 21

def gen_Gil(f):
    """ 
    Discrete cosine transform to get the values of the coefficients as in 
    Eq. 3.56 of "Numerical Methods for Special Functions" by Amparo Gil, Javier Segura, and Nico Temme
    """
    j = np.arange(0, n+1)
    thetavec = (j+1/2)*np.pi/(n+1)
    fval = f(np.cos(thetavec))

    c = []
    for k in range(n+1):
        ck = 0
        for j in range(n+1):
            ck += fval[j]*np.cos(k*thetavec[j])
        ck *= 2/(n+1)
        c.append(ck)
    c[0] /= 2
    return np.array(c)

print('Gil')
tic = timeit.default_timer()
c = gen_Gil(f); 
toc = timeit.default_timer()
print(c.tolist())
print(toc-tic, 'seconds')

tic = timeit.default_timer()
for i in range(100):
    ce = ChebTools.generate_Chebyshev_expansion(n, f, -1, 1)
toc = timeit.default_timer()
print('ChebTools (DCT)')
print(ce.coef().tolist())
print((toc-tic)/100,'seconds')

jvec = np.arange(0, n+1)
xnodes = np.cos(np.pi*jvec/n)
fstar = f(xnodes)

print(np.__version__)
# print(np.show_config())
import mkl_fft

tic = timeit.default_timer()
valsUnitDisc = np.array(fstar.tolist() + fstar[::-1][1:len(fstar)-1].tolist()) # starting at x=1, going to -1, then the same nodes, not including -1 and 1, in the opposite order
FourierCoeffs = np.real(np.fft.rfft(valsUnitDisc))
toc = timeit.default_timer()
ChebCoeffs = FourierCoeffs[0:n+1]/n
ChebCoeffs[0] /= 2
ChebCoeffs[-1] /= 2
print('numpyFFT')
print(ChebCoeffs.tolist())
print(toc-tic, 'seconds')

# plt.plot(ChebTools.generate_Chebyshev_expansion(n, f, -1, 1).coef()/c-1)
# plt.plot(ChebCoeffs/c-1)
# plt.show()