# Anze Marinko
# just to draw plots out of results

import matplotlib.pyplot as plt
import numpy as np
import os

directory = 'resultsHarris'

tests = sorted([os.path.splitext(base)[0] for base in os.listdir('results')])
results = [(('BLUP' if '0' in test and 'BLUP' in test else 'LU' if '0' not in test else 'BLU') + (' block={}'.format(test[-4:] if '000' in test else int(test[-3:])) if '0' in test else ' Perm.' if 'P' in test else ''), np.genfromtxt(directory+'/{}.csv'.format(test), delimiter=','), '-' if '0' not in test else '--' if 'B' in test else ':') for test in tests]

# n, lu, sol, forw, res, fact = results[:,0], results[:,1], results[:,2], results[:,3], results[:,4], results[:,5]
# draw graphs   
#   https://www.machinelearningplus.com/plots/matplotlib-tutorial-complete-guide-python-plot-examples/
ns = results[0][1][:,0]

best = ({0:0},{0:(0,0)},{0:(0,0)})  # best LU, BLU, BLUP: (n, tLU, P/bn)
for test, result, _ in results:
	i = 0 if '0' not in test else 2 if 'P' in test else 1
	for n, t in result[:,:2]:
		if i == 0:
			if 'P' not in test:
				best[i][n] = t
		elif t < best[i].get(n,(t+1,0))[0]:
			best[i][n] = (t, int(test[-4:]) if '000' in test else int(test[-3:]))
#print(bestLU)
LU = ([int(n) for n in ns], [best[0][n] for n in ns])
bestBLU = ([int(n) for n in ns], [best[1][n][0] for n in ns], [best[1][n][1] for n in ns])
bestBLUP = ([int(n) for n in ns], [best[2][n][0] for n in ns], [best[2][n][1] for n in ns])


plt.figure(1)
for res in results:
	plt.plot(res[1][:,0], res[1][:,1], res[2], label=res[0])
# plt.plot(n, sol, 'r--', label='System solving time')
plt.ylabel('time [s]')
plt.xlabel('dimension of matrix A')
plt.legend(loc='best')
plt.title('LU factorization time')

plt.figure(2)
for res in results:
	plt.plot(res[1][:,0], res[1][:,4], label=res[0])
plt.ylabel("$|| Ax-b||_1$ / $|| b||_1$")
plt.xlabel('dimension of matrix A')
#plt.legend(loc='best')
plt.yscale("log")
plt.title('Relative residual norm')

plt.figure(3)
for res in results:
	plt.plot(res[1][:,0], res[1][:,5], label=res[0])
plt.ylabel('$|| PA-LU||_1$ / $|| A||_1$')
plt.xlabel('dimension of matrix A')
#plt.legend(loc='best')
plt.yscale("log")
plt.title('Relative factorization error')

plt.figure(4)
for res in results:
	plt.plot(res[1][:,0], res[1][:,3], label=res[0])
plt.ylabel('$|| \hat{x}-x||_1$ / $|| \hat{x}||_1$')
plt.xlabel('dimension of matrix A')
#plt.legend(loc='best')
plt.yscale("log")
plt.title('Relative forward error')

plt.figure(5)
plt.plot(LU[0], LU[1], 'r-', label='LU')
plt.plot(bestBLU[0], bestBLU[1], 'g-', label='best BLU')
plt.plot(bestBLUP[0], bestBLUP[1], 'b-', label='best BLUP')
# plt.plot(n, sol, 'r--', label='System solving time')
plt.ylabel('time [s]')
plt.xlabel('dimension of matrix A')
plt.legend(loc='best')
plt.title('Runtime of the best in a method')

plt.figure(6)
plt.plot(bestBLU[0], bestBLU[2], 'g-', label='best BLU')
plt.plot(bestBLUP[0], bestBLUP[2], 'b-', label='best BLUP')
# plt.plot(n, sol, 'r--', label='System solving time')
plt.ylabel('block size')
plt.xlabel('dimension of matrix A')
plt.legend(loc='best')
plt.title('Best block size out of [100, 200, ..., 1000]')

plt.figure(7)
plt.plot(bestBLU[0], [bestBLU[1][i]/LU[1][i] for i in range(len(ns))], 'g-', label='best BLU')
plt.plot(bestBLUP[0], [bestBLUP[1][i]/LU[1][i] for i in range(len(ns))], 'b-', label='best BLUP')
# plt.plot(n, sol, 'r--', label='System solving time')
plt.ylabel('t / $t_{LU}$')
plt.xlabel('dimension of matrix A')
plt.legend(loc='best')
plt.title('Procent of time that LU has used')
plt.ylim(0,1.1)

plt.figure(8)
plt.plot(bestBLU[0], [bestBLUP[1][i]/bestBLU[1][i] for i in range(len(ns))], 'r-', label='BLUP')
# plt.plot(n, sol, 'r--', label='System solving time')
plt.ylabel('$t_{BLUP}$ / $t_{BLU}$')
plt.xlabel('dimension of matrix A')
plt.title('Procent of time that BLU has used')
plt.ylim(0,1.1)
	
plt.show()