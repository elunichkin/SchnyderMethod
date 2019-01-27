import networkx as nx


def find_faces(G, ce):
    edges = list(G.edges())
    edges += [(x[1], x[0]) for x in edges]
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

    if G.number_of_nodes() == 3 and G.number_of_edges() == 2:
        pass

    return find_faces(G, ce)


print('Enter two numbers V and E: number of vertices and edges in G, then edges (u, v) of G, 2 numbers at a line:')

V, E = [int(x) for x in input().split()]
e = []
for i in range(E):
    e.append(tuple([int(x) for x in input().split()]))

G = nx.Graph()
G.add_edges_from(e)
ce = nx.PlanarEmbedding.get_data(nx.check_planarity(G)[1])

tr = triangulate(G, ce)
print(tr)