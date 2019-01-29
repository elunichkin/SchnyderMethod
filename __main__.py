import networkx as nx


def find_faces(G, ce):
    edges = list(G.to_directed().edges())
    faces = []
    path = [edges[0]]
    edges.pop(0)

    while len(edges) > 0:
        u, v = path[-1]
        nbr = ce[v]
        w = nbr[(nbr.index(u) + 1) % len(nbr)]
        e = (v, w)

        if e == path[0]:
            faces.append(path)
            path = [edges[0]]
            edges.pop(0)
        else:
            path.append(e)
            index = edges.index(e)
            edges.pop(index)

    if len(path) > 0:
        faces.append(path)

    return faces


def triangulate(G, ce):
    if G.number_of_nodes() < 3 or not nx.is_connected(G):
        raise ValueError("Incorrect graph")

    added_edges = []

    if G.number_of_nodes() == 3 and G.number_of_edges() == 2:
        if G.number_of_edges(0, 1) > 0 and G.number_of_edges(0, 2) > 0:
            G.add_edge(1, 2)
            added_edges.append((1, 2))
            return added_edges
        elif G.number_of_edges(1, 0) > 0 and G.number_of_edges(1, 2) > 0:
            G.add_edge(0, 2)
            added_edges.append((0, 2))
            return added_edges
        else:
            G.add_edge(0, 1)
            added_edges.append((0, 1))
            return added_edges

    faces = find_faces(G, ce)

    for face in faces:
        if len(face) == 3:
            continue

        elif len(face) == 4:
            new_edge = (face[0][0], face[2][0])\
                if G.number_of_edges(face[0][0], face[2][0]) == 0\
                else (face[0][1], face[2][1])
            G.add_edge(new_edge[0], new_edge[1])
            added_edges.append(new_edge)

        else:
            new_face = []
            l, i = len(face), 0
            while i < l-1:
                new_edge = (face[i][0], face[i+1][1])
                if G.number_of_edges(new_edge[0], new_edge[1]) > 0:
                    new_face.append(face[i])
                    if i == l-2:
                        break
                    i += 1
                    continue
                G.add_edge(new_edge[0], new_edge[1])
                added_edges.append(new_edge)
                new_face.append(new_edge)
                i += 2
            if i != l:
                new_face.append(face[-1])
            faces.append(new_face)

    return added_edges


print('Enter two numbers V and E: number of vertices and edges in G, then edges (u, v) of G, 2 numbers at a line:')

"""
Example graph:
7 7
0 1
1 2
2 3
3 4
4 0
1 6
2 6
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

print(tr)
print(faces)