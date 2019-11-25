# Anze Marinko, 11905846
# Blocking LU factotization with Permutation Vector

#import os
#os.environ["OMP_NUM_THREADS"] = "1"
import numpy as np
import time
# from pypapi import events, papi_high as high

def timer(func):  # decorating function for timing
	def timed(*args, **kwargs):
		t0 = time.time()
		result = func(*args, **kwargs)
		t = time.time()-t0
		# print('Function {} was executed in {:.5f} s.'.format(func.__name__, t))  # for printing time in console
		if func.__name__ in 'LU_blocked':
			return (result, t)    # add LU time to collection
		else:
			return (result, t)   # add solving time to collection
	return timed

# ============== Permutations ==============
def newPermutation(n):
	return [*range(n)]

def permutePermutation(P1, P2):
	return [P2[p] for p in P1]

def permuteArray(P, A):
	out = np.zeros(A.shape)
	for p in range(len(P)):
		out[p,:] = A[P[p],:]*1
	return out

def permutationMatrix(P):
	return permuteArray(P, np.eye(len(P)))

# =============== Solving =================
def LU( A ):   # LU factorization with partial pivoting
	(n,m) = A.shape   # be careful that A is squear matrix!
	A = A*1    # just not to change the original from otside of the function
	L, P = np.eye(n), newPermutation(n)
	for j in range(m):
		q = j+np.argmax(np.abs(A[j:,j]))    # pivot row
		A[j,j:], A[q,j:] = A[q,j:]*1, A[j,j:]*1  # row q <---> row j
		L[j,:j], L[q,:j] = L[q,:j]*1, L[j,:j]*1
		P[j], P[q] = P[q]*1, P[j]*1
		for i in range(j+1, n):
			L[i,j] = A[i,j] / A[j,j]
			A[i,j:] = A[i,j:] - L[i,j] * A[j,j:]
		#L[j+1:,j] = A[j+1:,j] / A[j,j]
		# A[j+1:,j:] = A[j+1:,j:] - np.dot(L[j+1:,j:j+1], A[j:j+1,j:])
	return L, A, P
	
def forward( L, b):  # forward substitution
	y = np.zeros(b.shape)
	y[0,:] = b[0,:]
	for i in range(1, b.shape[0]):   # L is a lower triangular matix
		y[i,:] = b[i,:] - np.dot(L[i,:i], y[:i,:])
	return y

def back( U, y):   # back substitution
	x = np.zeros(y.shape)
	for k in range(y.shape[0]):   # U in an upper triangular matix
		i = y.shape[0] - 1 - k
		x[i,0] = (y[i,0] - sum(U[i,i+1:] * x[i+1:,0])) / U[i,i]
	return x

@timer
def LU_blocked( A, bn = 500 ):   # John Cole: LU FACTORIZATION MEASUREMENT AND OPTIMIZATION
	# bn ..... right looking algorithm block size
	(n,m) = A.shape
	A = A*1    # just not to change the original from otside of the function
	if bn == 1:
		return LU(A)
	steps = min(m,n)//bn + (1 if min(m,n)%bn > 0 else 0)
	L, P = np.eye(n), newPermutation(n)
	for k in range(steps):
		if k == steps-1:
			Lk, Ak, Pk = LU(A[bn*k:,bn*k:])
			L[bn*k:,bn*k:], A[bn*k:,bn*k:] = Lk, Ak
			P[bn*k:] = permutePermutation(Pk, P[bn*k:])
			L[bn*k:,:bn*k] = permuteArray(Pk, L[bn*k:,:bn*k])
			return L, A, P
		# factorize A11 and A21 to get L11, L21, U11 (Cole 3)
		Lk, Ak, Pk = LU(A[bn*k:,bn*k:bn*(k+1)])
		L11, L21, U11 = Lk[:bn,:bn], Lk[bn:,:bn], Ak[:,:bn]
		L[bn*k:bn*(k+1),bn*k:bn*(k+1)], L[bn*(k+1):,bn*k:bn*(k+1)], A[bn*k:,bn*k:bn*(k+1)] = L11, L21, U11
		# (Cole 4)
		A[bn*k:,bn*(k+1):], L[bn*k:,:bn*k] = permuteArray(Pk, A[bn*k:,bn*(k+1):]), permuteArray(Pk, L[bn*k:,:bn*k])
		P[bn*k:] = permutePermutation(Pk, P[bn*k:])
		# solve L11*A12 = A12
		A[bn*k:bn*(k+1),bn*(k+1):] = forward(L11, A[bn*k:bn*(k+1),bn*(k+1):])
		# update A22
		A[bn*(k+1):,bn*(k+1):] = A[bn*(k+1):,bn*(k+1):] - np.dot(L[bn*(k+1):,bn*k:bn*(k+1)], A[bn*k:bn*(k+1),bn*(k+1):])
	return L, A, P

@timer
def solveLinearSystem( A, b, blockN = 500):  # solve linear system A*x = b, return x
	(L, U, P), tLU = LU_blocked(A, blockN)
	pb = permuteArray(P, b)     # we want to solve (P*A) * x = (P*b), because we know P*A=L*U
	y = forward(L, pb)    # L * y = pb
	x = back(U, y)       # U * x = y
	return (x, L, U, permutationMatrix(P)), tLU

