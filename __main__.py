import networkx as nx
from schnyder import find_faces, triangulate, schnyder_labeling, realizer

print('Enter two numbers V and E: number of vertices and edges in G, then edges (u, v) of G, 2 numbers at a line:')

"""
Example graph:
6 7
0 1
1 2
2 3
3 4
4 0
1 5
2 5
"""

V, E = [int(x) for x in input().split()]
e = []
for i in range(E):
    e.append(tuple([int(x) for x in input().split()]))

G = nx.Graph()
G.add_edges_from(e)
G_old = G.copy()

ce = nx.PlanarEmbedding.get_data(nx.check_planarity(G)[1])
tr = triangulate(G, ce)

ce = nx.PlanarEmbedding.get_data(nx.check_planarity(G)[1])
faces = find_faces(G, ce)
lbl = schnyder_labeling(G, ce, faces[0])
r = realizer(G, lbl)
print(r)