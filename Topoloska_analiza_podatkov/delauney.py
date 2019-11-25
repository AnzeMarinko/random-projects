# delauneyeva triangulacija
# https://www.cise.ufl.edu/~ungor/delaunay/delaunay/node5.html
import random

def genefy(S):
	eps = 1e-8
	return {(s[0],s[1]):(s[0] + eps*(0.5 - random.random()), s[1] + eps*(0.5 - random.random())) for s in S}

def optimize(T):
	# popravi triangulacijo
	# tocke damo v generalno pozicijo
	S = genefy({t[0] for t in T}.union({t[1] for t in T}.union({t[2] for t in T})))
	T = {tuple(sorted([S[t[0]],S[t[1]],S[t[2]]])) for t in T}
	E = {tuple([t[0],t[1]]) for t in T}.union({tuple([t[1],t[2]]) for t in T}.union({tuple([t[0],t[2]]) for t in T}))
	nonDelaunay = set()
	for e in E:
		ts = [t for t in T if len({*t}.intersection({*e})) ==2]
		if len(ts) == 2:
			# https://en.wikipedia.org/wiki/Delaunay_triangulation
			(Ax, Ay) = e[0]
			(Bx, By) = [s for s in ts[0] if s not in e][0]
			(Cx, Cy) = e[1]
			(Dx, Dy) = [s for s in ts[1] if s not in e][0]
			delta = (Ax-Dx)*(By - Dy)*((Cx-Dx)**2+(Cy-Dy)**2) + (Bx-Dx)*(Cy - Dy)*((Ax-Dx)**2+(Ay-Dy)**2) + (Cx-Dx)*(Ay - Dy)*((Bx-Dx)**2+(By-Dy)**2) - (Ax-Dx)*(Cy - Dy)*((Bx-Dx)**2+(By-Dy)**2) - (Bx-Dx)*(Ay - Dy)*((Cx-Dx)**2+(Cy-Dy)**2) - (Cx-Dx)*(By - Dy)*((Ax-Dx)**2+(Ay-Dy)**2)
			if (By - Cy)*(Ax - Cx) - (Bx - Cx)*(Ay - Cy) < 0:
				delta *= -1
			if delta > 0:
				nonDelaunay.add(e)
	while nonDelaunay:
		e = nonDelaunay.pop()
		ts = [t for t in T if len({*t}.intersection({*e})) ==2]
		if len(ts) == 2:
			# https://en.wikipedia.org/wiki/Delaunay_triangulation
			(Ax, Ay) = e[0]
			(Bx, By) = [s for s in ts[0] if s not in e][0]
			(Cx, Cy) = e[1]
			(Dx, Dy) = [s for s in ts[1] if s not in e][0]
			delta = (Ax-Dx)*(By - Dy)*((Cx-Dx)**2+(Cy-Dy)**2) + (Bx-Dx)*(Cy - Dy)*((Ax-Dx)**2+(Ay-Dy)**2) + (Cx-Dx)*(Ay - Dy)*((Bx-Dx)**2+(By-Dy)**2) - (Ax-Dx)*(Cy - Dy)*((Bx-Dx)**2+(By-Dy)**2) - (Bx-Dx)*(Ay - Dy)*((Cx-Dx)**2+(Cy-Dy)**2) - (Cx-Dx)*(By - Dy)*((Ax-Dx)**2+(Ay-Dy)**2)
			if (By - Cy)*(Ax - Cx) - (Bx - Cx)*(Ay - Cy) < 0:
				delta *= -1
			if delta > 0:
				# zasukaj stranico
				T.remove(ts[0])
				T.remove(ts[1])
				T.add(tuple(sorted([(Ax,Ay),(Bx,By),(Dx,Dy)])))
				T.add(tuple(sorted([(Cx,Cy),(Bx,By),(Dx,Dy)])))
				# dodaj sosedne 4
				nonDelaunay.add(tuple(sorted([(Ax,Ay), (Bx, By)])))
				nonDelaunay.add(tuple(sorted([(Ax,Ay), (Dx, Dy)])))
				nonDelaunay.add(tuple(sorted([(Cx,Cy), (Bx, By)])))
				nonDelaunay.add(tuple(sorted([(Cx,Cy), (Dx, Dy)])))
	S = set()
	for t in T:
		S = S.union({*t})
	S = list(S)
	return (S, [list(t) for t in T])
	