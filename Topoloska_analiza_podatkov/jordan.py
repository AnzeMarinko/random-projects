import turtle

def insideQ(P,T):
	# stejemo presecisca cez poltrak iz T skozi T + (-1, 0)
	intersections = 0
	P = [(p[0]-T[0],p[1]-T[1]) for p in P]
	P = P + [P[0]]
	for i in range(len(P)-1):
		# ali je tocka na robu
		if P[i] == (0,0):
			 return True
		elif P[i][0]*P[i+1][1] == P[i][1]*P[i+1][0] and (P[i][0]*P[i+1][0]<0 or P[i][1]*P[i+1][1]<0):
			return True
		# pristejemo morebitno presecisce
		if  -P[i][0] * (P[i+1][0] - P[i][0]) > 0 and abs(P[i][0]) < abs(P[i+1][0] - P[i][0]) and P[i][1] - (P[i+1][1] - P[i][1]) * P[i][0] / (P[i+1][0] - P[i][0]) < 0:
			intersections += 1
		elif (P[i][0] == 0 and P[i][1] < 0 and P[i+1][0] > 0) or (P[i+1][0] == 0 and P[i+1][1] < 0 and P[i][0] > 0):
			# pristejemo le ko prihajamo z desne ali odhajamo desno
			intersections += 1
	return (intersections%2 == 1)	

TP = (tp for tp in [((2.33,0.66),[(0.02,0.10),(0.98,0.05),(2.10,1.03),(3.11,-1.23),(4.34,-0.35),(4.56,2.21),(2.95,3.12),(2.90,0.03),(1.89,2.22)]), ((0,0.3),[(1,0),(1,1),(0,1),(0,0)]),  ((4,0.5),[(i,i%2) for i in range(7)]+[(6,-1),(0,-1)]), ((0.1, 0.2),[(1,1), (0,1), (1,0.9)])])

def h1(x, y):
	z.clear()
	(T, P) = next(TP)
	print(insideQ(P,T))
	narisi(z, P, T)

def narisi(z, P, T):
	z.penup()
	z.goto(round(100*P[len(P)-1][0]-200), round(100*P[len(P)-1][1]-100))
	z.pendown()
	for p in P:
		z.goto(round(100*p[0]-200), round(100*p[1]-100))
	z.penup()
	z.goto(round(100*T[0]-200+5), round(100*T[1]-100))
	z.pendown()
	z.goto(round(100*T[0]-200), round(100*T[1]-100+5))
	z.goto(round(100*T[0]-200-5), round(100*T[1]-100))
	z.goto(round(100*T[0]-200), round(100*T[1]-100-5))
	z.goto(round(100*T[0]-200+5), round(100*T[1]-100))
	z.penup()
	z.goto(1000,1000)

def izris():
	wn = turtle.Screen()
	wn.title("Jordan")
	z = turtle.Turtle()
	wn.onclick(h1)
	wn.mainloop()
