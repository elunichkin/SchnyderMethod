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


def schnyder_labeling(G, ce, ef):
    def intersect(l1, l2):
        return list(set(l1) & set(l2))

    def subtract(l1, l2, l3 = []):
        return [x for x in l1 if x not in (l2 + l3)]

    v = sorted([ef[0][0], ef[1][0], ef[2][0]])
    ce_cnt = {}

    for u in list(G.nodes()):
        ce_cnt[u] = 0
    for u in ce[v[0]]:
        ce_cnt[u] = len(intersect(ce[v[0]], ce[u]))

    to_strip = []
    strip = []

    for u in ce[v[0]]:
        if u not in v and ce_cnt[u] == 2:
            to_strip.append(u)

    ce_v0 = ce[v[0]]

    while G.number_of_nodes() > 3:
        if len(to_strip) == 0:
            break
        u = to_strip.pop()

        strip.append((u, ce[u], subtract(ce[u], ce_v0, [v[0]])))
        G.remove_node(u)
        ce_v0 = subtract(ce_v0, [u])

        for w in subtract(ce[u], ce_v0, [v[0]]):
            G.add_edge(v[0], w)

        if G.number_of_nodes() == 3:
            break

        ce_v0 += subtract(ce[u], [v[0]])
        to_strip = []

        for w in ce[v[0]]:
            if len(intersect(ce_v0, ce[w])) == 2 and w not in v:
                to_strip.append(w)

    labels = {v[0]: {(v[0], v[1]): 3},
              v[1]: {(v[0], v[2]): 2},
              v[2]: {(v[1], v[2]): 1}}

    while len(strip) > 0:
        u, new_ce, old_ce = strip.pop()
        labels[u] = {}

        for w in old_ce:
            G.remove_edge(v[0], w)

        if len(old_ce) == 0:
            w = sorted(new_ce)

            labels[u] = {(w[0], w[1]): labels[w[2]].pop((w[0], w[2])),
                         (w[0], w[2]): labels[w[1]].pop((w[0], w[2])),
                         (w[1], w[2]): labels[w[0]].pop((w[0], w[1]))}

            labels[w[0]][tuple(sorted([w[1], u]))] = labels[u][(w[0], w[1])]


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
lbl = schnyder_labeling(G, ce, faces[0])