# algoritem pometanja
import random

def genefy(S):
	newS = []
	eps = 1e-8
	for s in S:
		newS.append((s[0] + eps*(0.5 - random.random()), s[1] + eps*(0.5 - random.random())))
	return newS

def triangulate(S, vertical=True):
	S = genefy(S)
	if not vertical:
		S.sort(key = lambda s: (-s[1],s[0]))
	else:
		S.sort()
	T = [(S[0],S[1],S[2])]
	rob = [S[2], S[0], S[1], S[2], S[0]]
	for i in range(3,len(S)):
		newRob = []
		prvic = True
		for j in range(len(rob)-2):
			detT = (rob[j+1][1] - rob[j+2][1])*(rob[j][0] - rob[j+2][0]) - (rob[j+1][0] - rob[j+2][0])*(rob[j][1] - rob[j+2][1])
			bar1 = (rob[j+1][1] - rob[j+2][1])*(S[i][0] - rob[j+2][0]) - (rob[j+1][0] - rob[j+2][0])*(S[i][1] - rob[j+2][1])
			# preverimo ce je prva baricentricna koordinata negativna ... ce je dodamo trikotnik v T in tocko dodamo na rob
			if bar1*detT >= 0:
				newRob.append(rob[j+1])
			elif prvic and bar1*detT < 0:
				T.append((rob[j+1],rob[j+2],S[i]))
				newRob.append(rob[j+1])
				newRob.append(S[i])
				prvic = False
			else:
				T.append((rob[j+1],rob[j+2],S[i]))
		newRob.append(newRob[0])
		newRob = [newRob[len(newRob)-2], newRob[len(newRob)-1]] + newRob
		rob = newRob
	return (S, T)
