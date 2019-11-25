import time

def timer(f):
	def wrapper(*args, **kwargs):
		t0 = time.time()
		fx = f(*args, **kwargs)
		t = time.time() - t0
		print('Cas izvajanja ukaza: {} s'.format(t))
		return fx
	return wrapper

def BronKerboschAlgorithm(R,P,X, EG):
	cliqs = set()
	if len(P) == 0 and len(X) == 0:
		powerset = {tuple(sorted([R[j] for j in range(len(R)) if (i & (1 << j))])) for i in range(1,1 << len(R))}
		cliqs = cliqs.union(powerset)
	for v in P:
		sosedje = {{*e}.difference({v}).pop() for e in EG if len({*e}.intersection({v})) == 1}
		cliqs = cliqs.union(BronKerboschAlgorithm(R+[v], P.intersection(sosedje), X.intersection(sosedje), EG))
		P = P.difference({v})
		X = X.union({v})
	return cliqs

@timer
def cliques(VG, EG):
	return BronKerboschAlgorithm([], {*VG}, set(), EG)

@timer
def VR(S, epsilon):
	if len(S[0]) == 2:
		S = [(s[0],s[1],0) for s in S]
	E = set()
	for i in range(len(S)):
		for j in range(len(S)):
			d = (S[i][0]-S[j][0])**2 + (S[i][1]-S[j][1])**2 + (S[i][2]-S[j][2])**2
			if d > 0 and d <= epsilon**2:
				E.add(tuple(sorted((i,j))))
	cliqs = cliques([i for i in range(len(S))],E)
	VRe = {i-1: sorted([cliq for cliq in cliqs if len(cliq) == i]) for i in range(len(S)) if len([cliq for cliq in cliqs if len(cliq) == i]) > 0}
	return VRe

VG = [1,2,3,4,5,6]
EG = [(1,2),(2,3),(1,3),(3,4),(1,4),(2,4),(3,5),(3,6),(5,6)]
#print(cliques(VG,EG))
EG = []
#print(cliques(VG,EG))
EG = [(1,2),(2,3),(1,3),(3,4),(1,4),(2,4),(3,5),(1,5),(2,5),(4,5),(1,6),(2,6),(3,6),(4,6),(5,6)]
#print(cliques(VG,EG))
#print()

for i in range(12,21):
	VG = [j for j in range(1,i+1)]
	EG = [(k,j) for j in VG for k in range(1,j)]
	print()
	print(len(VG))
	cliques(VG,EG)

S = [(0, 0), (1, 1), (2, 3), (-1, 2), (3, -1), (4, 2)]
epsilon = 3
#print(VR(S, epsilon))
#print(VR(S,2))

S = [(0,0), (1, 0), (1, 1), (0, 1), (0, 2)]
#print(VR(S, epsilon))

