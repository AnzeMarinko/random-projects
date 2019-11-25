import linesweeptriangulation as lst
import delauney
from orientable import orientable
import random
import time
import turtle

def izris(S, T):
	screen = turtle.Screen()
	turtle.tracer(0, 0)
	t = turtle.Turtle()
	t.hideturtle()
	t.fillcolor('orange')
	t.penup()
	mx = min(S)[0]
	my = min([(x[1],x[0]) for x in S])[0]
	w = max(max(S)[0] - min(S)[0], max([(x[1],x[0]) for x in S])[0] - min([(x[1],x[0]) for x in S])[0])
	for tri in T:
		t.begin_fill()
		t.goto((tri[2][0] - mx)*400/w-200, (tri[2][1] - my)*400/w - 200)
		t.pendown()
		for i in range(3):
			t.goto((tri[i][0] - mx)*400/w-200, (tri[i][1] - my)*400/w - 200)
		t.end_fill()
		t.penup()
	for s in S:
		t.goto((s[0] - mx)*400/w-200, (s[1] - my)*400/w - 200)
		t.dot(8, 'blue')
	turtle.update()
	time.sleep(5)
	t.clear()

# test linesweeptriangulation.py and delauney.py
Ss = [[(0, 0), (3, 9), (5, -1), (9, 4), (7, -5)], [(random.random()*20,random.random()*20) for i in range(100)], [(random.random()*20,random.random()*20) for i in range(200)]]
for S in Ss:
	t = time.time()
	(S1, T1) = lst.triangulate(S, True)
	print(time.time()-t)
	t = time.time()
	(S2, T2) = lst.triangulate(S, False)
	print(time.time()-t)
	t = time.time()
	(S3, T3) = delauney.optimize(T1)
	print(time.time()-t)
	izris(S1, T1)
	izris(S2, T2)
	izris(S3, T3)

# test orientable.py
M = [(1, 2, 3), (2, 3, 4), (3, 4, 5), (4, 5, 6), (2, 5, 6), (1, 2, 6)]
S2 = [(1, 2, 3), (1, 2, 4), (1, 3, 4), (2, 3, 4)]
orientable(M)
orientable(S2)
torus = [(0,3,7),(0,2,7),(3,4,8),(3,7,8),(4,0,2),(4,8,2),(2,7,5),(2,1,5),(7,8,6),(7,5,6),(8,2,1),(8,6,1),(1,5,3),(1,0,3),(5,6,4),(5,3,4),(6,1,0),(6,4,0)]
print('Torus')
orientable(torus)
[a,b,c,d,e,f,g,h,i] = [0,1,2,3,4,5,6,7,8]
klein = [(a,b,f),(a,d,f),(b,f,c),(f,c,g),(g,c,a),(g,e,a),(e,d,f),(e,h,f),(h,f,g),(h,i,g),(i,g,e),(i,d,e),(a,e,h),(a,b,h),(b,h,i),(b,c,i),(i,c,a),(i,d,a)]
print('Klein bottle')
orientable(klein)
sphere = [(d,c,a),(c,d,b),(a,c,b),(a,b,d)]
print('Sphere')
orientable(sphere)
cylinder = [(a,d,b),(d,b,e),(e,b,c),(e,f,c),(f,c,a),(f,d,a),(g,d,e),(g,h,e),(h,e,f),(h,i,f),(i,f,d),(i,g,d)]
print('Cylinder')
orientable(cylinder)
moebius = [(0,1,2),(1,2,3),(2,3,4),(3,4,0),(4,1,0)]
print('Moebius strip')
orientable(moebius)