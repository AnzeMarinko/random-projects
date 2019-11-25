# Anze Marinko, ISRM2, Algoritmi, seminar 2           # 16. april 2019
import sys       # najdi prirejanje brez presecisc med tockamiv R^2, kjer ena z x<0 in ena z x>0
with open(sys.argv[1],'r') as f: # ime vhodne datoteke podan za ukazom 'python3 connect.py'
	f.readline()      # uvozimo tocke definirane v vhodni datoteki, tocke razvrstimo po y padajoce
	V = sorted([(int(i),float(x),float(y)) for i,x,y in [line.split(sep=',') for line in f.readlines()]], key = lambda x: (-x[2],-x[1],-x[0]))
while V:          # dokler imamo na seznamu se kaj tock
	v0, poz = V[0], 1 if V[0][1]>0 else -1     # vzamemo najvisjo tocko, nadaljni postopek odvisen ali je x<0 ali je x>0
	while True:       # iscemo naslednji element na robu konveksne ovojnice v smeri proti x=0
		v1 = min([v for v in V if poz*v[1]<poz*v0[1]], key=lambda x: poz*(v0[2]-x[2])/(1000*(v0[1]-x[1])))
		if v1[1]*poz < 0:    # ko z robom konveksne ovojnice preckamo os x=0
			print('{}-{}'.format(v0[0],v1[0]),file=sys.stdout)    # natisnemo indeksa krajisc povezave
			V.remove(v0)   # odstranimo tocki na konveksni ovojnici iz seznama tock
			V.remove(v1)
			break
		v0 = v1   # sicer se prestavimo do naslednje tocke na robu konveksne ovojnice