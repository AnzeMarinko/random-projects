import turtle
import math

def graf(V, E):
    g = {}
    for v in V:
        g[v] = set()
    for e in E:
        g[e[0]].add(e[1])
        g[e[1]].add(e[0])
    return g

def sosedje(g, v):
    return g.get(v)
				
def odstrani(g, v):
    for u in sosedje(g,v):
        g[u].remove(v)
    g.pop(v, None)
    return g

def povezan(g):
    if len(g.keys()) == 0:
        return []
    v = list(g.keys())[0]
    komponenta = [v]
    kandidati = sosedje(g, v)
    g = odstrani(g, v)
    while len(kandidati) > 0:
        u = kandidati.pop()
        komponenta.append(u)
        if sosedje(g, u) == None:
            continue
        for w in sosedje(g, u):
            kandidati.add(w)
        g = odstrani(g, u)
    kandidati = set()
    return [komponenta]+povezan(g)

def findComponents(V,E):
    return povezan(graf(V,E))

V = [1,2,3,4,5,6,7,8]
E = [(1,2),(2,3),(1,3),(4,5),(5,6),(5,7),(6,7),(7,8)]
print(findComponents(V, E))

V = [1,2,3,4,5]
E = [(1,2),(1,3),(1,4),(1,5)]
print(findComponents(V, E))

V = [1,2,3,4,5,6,7,8,9]
E = [(1,2),(1,3),(1,8),(3,7),(4,5),(4,6),(4,9),(5,6),(5,9),(7,8)]
print(findComponents(V, E))

V = [1,2,3,4,5,6,7]
E = []
print(findComponents(V, E))

V = [1,2,3,4]
E = [(1,2),(1,3),(1,4),(2,3),(2,4),(3,4)]
print(findComponents(V, E))

V = [1,2,3,4,5]
E = [(1,2),(2,3),(3,5)]
print(findComponents(V, E))

# rezultati:
# [[1, 2, 3], [4, 5, 6, 7, 8]]
# [[1, 2, 3, 4, 5]]
# [[1, 8, 2, 3, 7], [4, 9, 5, 6]]
# [[1], [2], [3], [4], [5], [6], [7]]
# [[1, 2, 3, 4]]
# [[1, 2, 3, 5], [4]]

# enostavno in licno izrisovanje grafov: https://csacademy.com/app/graph_editor/
