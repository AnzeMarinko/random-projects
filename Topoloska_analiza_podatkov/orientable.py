
def orientableQ(T):
	# vrne True, če je triangulacija T orientabilna
	# ali je dovolj preveriti da vsaka tocka nastopa ali na robu ali v sodo trikotnikih?
	E = {tuple(sorted([t[0],t[1]])) for t in T}.union({tuple(sorted([t[1],t[2]])) for t in T}.union({tuple(sorted([t[0],t[2]])) for t in T}))
	E = {e: 0 for e in E}
	T = {*T}
	kandidati = [T.pop()]
	while kandidati:
		t = sorted(kandidati[0])
		kandidati = kandidati[1:]
		o1 = E[(t[0],t[1])]
		o2 = E[(t[0],t[2])]
		o3 = E[(t[1],t[2])]
		# preverimo, ce je prav orientiran, glede na ze orientirane sosede in nastavimo se neorientirane stranice
		if o1 != 0:
			if o1 != o2 and o1 != - o3:
				E[(t[0],t[2])] = o1
				E[(t[1],t[2])] = -o1
			else:
				return False
		elif o2 != 0:
			if o2 != o3:
				E[(t[0],t[1])] = o2
				E[(t[1],t[2])] = o2
			else:
				return False
		elif o3 != 0:
			E[(t[0],t[1])] = -o3
			E[(t[0],t[2])] = o3
		else:
			E[(t[0],t[1])] = 1
			E[(t[0],t[2])] = -1
			E[(t[1],t[2])] = 1
		# dodaj sosede kandidatom
		sosedje = [sosed for sosed in T if len({*sosed}.intersection({*t})) ==2]
		kandidati = kandidati +sosedje
		for sosed in sosedje:
			T.remove(sosed)
	return True

def orientable(T):
	if not orientableQ(T):
		print('This surface is not orientable!')
		print('Oriented triangles:\nNone\n')
		return None
	
	print('This surface is orientable.')
	print('Oriented triangles:')
	E = {tuple(sorted([t[0],t[1]])) for t in T}.union({tuple(sorted([t[1],t[2]])) for t in T}.union({tuple(sorted([t[0],t[2]])) for t in T}))
	E = {e: 0 for e in E}
	oriT = {tuple(sorted(T[i])): i for i in range(len(T))}
	T = {tuple(sorted(t)) for t in T}
	newT = []
	kandidati = [T.pop()]
	while kandidati:
		t0 = kandidati[0]
		t = tuple(sorted(t0))
		kandidati = kandidati[1:]
		o1 = E[(t[0],t[1])]
		o2 = E[(t[0],t[2])]
		o3 = E[(t[1],t[2])]
		if o1 != 0:
			E[(t[0],t[2])] = o1
			E[(t[1],t[2])] = -o1
			if o1 == 1:
				newT.append((t[0],t[2],t[1]))
				oriT[(t[0],t[2],t[1])] = oriT[t0]
				oriT.pop(t0)
			else:
				newT.append(t)
		elif o2 != 0:
			E[(t[0],t[1])] = o2
			E[(t[1],t[2])] = o2
			if o2 == -1:
				newT.append((t[0],t[2],t[1]))
				oriT[(t[0],t[2],t[1])] = oriT[t0]
				oriT.pop(t0)
			else:
				newT.append(t)
		elif o3 != 0:
			E[(t[0],t[1])] = -o3
			E[(t[0],t[2])] = o3
			if o3 == 1:
				newT.append((t[0],t[2],t[1]))
				oriT[(t[0],t[2],t[1])] = oriT[t0]
				oriT.pop(t0)
			else:
				newT.append(t)
		else:
			E[(t[0],t[1])] = 1
			E[(t[0],t[2])] = -1
			E[(t[1],t[2])] = 1
			newT.append(t)
		# dodaj sosede kandidatom
		sosedje = [sosed for sosed in T if len({*sosed}.intersection({*t})) ==2]
		kandidati = kandidati +sosedje
		for sosed in sosedje:
			T.remove(sosed)
	newT.sort(key = lambda x: oriT[x])
	print(newT)
	print()
	return newT
