# test
import BLU as blu
import BLUP as blup
import numpy as np

bns = [1,100,200,300,400,500,700,800,900,1000]
results = [] # collect dimension, execution time of LU, solving, relative residual norm, relative forward and factorization error
maxN = 6000    # set highest testing n
step = 500        # step from 500 to maxN
methods = ['blockLU','BLUP']
method = 0   # index of a method from a list methods

# relative forward error: max_i(x_i-x'_i)/max_i(x'_i), where x is computed solution and x' is exact solution
def relative_forward_error(computed_x, exact_x):
	return np.abs(computed_x - exact_x).max() / np.abs(exact_x).max()

# relative residual norm: max_i (Ax-b)_i / max_i b_i
def relative_residual_norm(A, computed_x, b):
	return np.abs(np.dot(A,computed_x)-b).max() / np.abs(b).max()

# relative factorization error: max_ij (PA-LU)_ij / max_ij A_ij
def relative_factorization_error(P, A, L, U):
	return np.abs(np.dot(P, A)-np.dot(L, U)).max() / np.abs(A).max()

def efficiency(flops, t):
	perf = flops/t
	# Theoretical peak performance in flops:
	n_cores = 1
	clock_speed = 1.7e9
	flopcyc = 2
	theoretical_peak_perf = n_cores*clock_speed*flopcyc # in flop/s
	return perf/theoretical_peak_perf


for n in [100, 200, 300, 400] + [i * step for i in range(1, maxN // step + 1)]:
	A = np.random.rand(n, n)  # make a random matrix A
	exact_x = np.ones((n, 1))  # let be exact solution x = [1 ... 1]^T
	b = np.dot(A, exact_x) 
	for bn in bns:
		for method in range(len(methods)):
			print(n,bn,methods[method])
			# high.start_counters([events.PAPI_FP_OPS,])
			if method == 0:
				((computed_x, L, U, P), tLU), tSolve = blu.solveLinearSystem(A, b, bn)
			else:
				((computed_x, L, U, P), tLU), tSolve = blup.solveLinearSystem(A, b, bn)
			results.append([n,tLU,tSolve])
			# number of flops
			# flops=high.stop_counters()
			# print(n,flops)
			results[-1].append(relative_forward_error(computed_x, exact_x))
			results[-1].append(relative_residual_norm(A, computed_x, b))
			results[-1].append(relative_factorization_error(P, A, L, U))
			# results[-1].append(efficiency(flops, results[-1][2]))
			if method < 2:
				with open("results/{}-block{}.csv".format(methods[method], bn), "a") as f:
					r = results[-1]
					row = '{}'.format(r[0])
					for value in r[1:]:
						row += ',{}'.format(value)
					f.write(row+'\n')
			else:
				with open("results/{}.csv".format(methods[method]), "a") as f:
					r = results[-1]
					row = '{}'.format(r[0])
					for value in r[1:]:
						row += ',{}'.format(value)
					f.write(row+'\n')
results = np.array(results)
#print(['A dimension', 'LU time', 'solving time', 'rel. forward err.', 'rel. residual norm.', 'rel. factor. err.'])
