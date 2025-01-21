# Elementary Graph Algorithms

## Graph representation

Representations
1. Adjacency-List Representation A list of
adjacent nodes per node. Encoding size
= Θ(E + V ). Suitable for *sparse graphs*.
2. Adjacency-Matrix Representation The
|V | × |V | matrix that represents
connection between nodes. Encoding size
= Θ(V^2). Suitable for *dense graphs*.


### Adjacency-List Representation

```json
1 : [2, 6]
2 : [3, 5]
3 : []
4 : [1, 3]
5 : [4, 6]
6 : [2]
```


### Adjacency-Matrix Representation
```json
0 1 0 0 0 1
0 0 1 0 1 0
0 0 0 0 0 0
1 0 1 0 0 0
0 0 0 1 0 1
0 1 0 0 0 0
```


## Search strategies

Traversal of Nodes
The problem of visiting all the nodes of a
given graph G starting from a specific node s.
1. Breadth-First Search: Mark all the
unmarked adjacent nodes. Then
recursively visit each of the adjacent
nodes.
2. Depth-First Search: If there are
unmarked adjacent nodes visit one of
them.

*Connectivity in Undirected Graphs Nodes*

u and v are *connected* if there is a path
between them. A graph G is *connected* if
every pair of nodes is connected.

So, when search is finished check whether
any node is yet to be visited. If so, start the
search from any such one.

# Shortest path
1. Computing the Minimum Distance from s with BFS
δ(v)
def
= the minimum distance of v from s

### The Parenthesis Structure of DFS

For each u, let I[u] = (d[u], f[u]). Then, for
all u and v, exactly one of the following three
holds for I[u] and I[v],
* I[u] ∩ I[v] = ∅. This is the case when u
and v are not on the same path from s.
* I[u] ⊆ I[v]. This is the case when u is a
descendant of v on a path from s.
* I[v] ⊆ I[u]. This is the case when v is a
descendant of u on a path from s.

This is called the parenthesis structure of DFS.

## Classification of edges
1. The Tree Edges: The edges on the tree.
2. The Back Edges: The non-tree edges
connecting descendants to ancestors
(including self-loops).
3. The Forward Edges: The non-tree
edges connecting ancestors to
descendants.
4. The Cross Edges: The rest.

In DFS, when e = (u, v) is first explored:
• d[v] = ∞ ⇒ e is a tree edge,
• d[v] < f[v] = ∞ ⇒ e is a back edge, and
• f[v] < ∞ ⇒ e is a forward or cross edge.

Every edge is either a tree edge or a back edge for an undirected graph.

# Topological sort
Let G be a DAG (directed acyclic graph).
Topological sorting of the nodes of G is a
linear ordering of the nodes such that for all u
and v if there is an arc from u to v (i.e.,
(u, v) ∈ E) then u precedes v in the ordering.

## An Algorithm for Topological Sort
Call DFS(G) to compute f-values. While
doing this, each time a node, say v, is done,
insert v as the top element of the list.

# Strongly connected components
Let G be a directed graph. For all nodes u
and v, write u ❀ v if there is a directed path
from u to v in G.

Two vertices u and v of a directed graph G
are *strongly connected* if u ❀ v and v ❀ u.
A strongly connected component of G is a
maximal set S of vertices in G in which every
two nodes are strongly connected.

## An O(E + V )-Step Method
Define GT to be the graph G in which the
direction of each edge is reversed. We do the
following:
1. Call DFS(G) to compute f[u] for all u.
2. Compute H = GT where the nodes are
enumerated in order of decreasing f.
3. Call DFS(H), in which whenever the
paths have been exhausted, find the next
node that is not visited yet in the above
ordering.
4. Output the vertices of each DFS-tree of
H as a separate strongly connected
component.

# MST

Let G = (V, E) be a connected (undirected)
graph. A spanning tree of G is a tree T that
consists of edges of G and connects every
pair of nodes.

Let w be an integer edge-weight function. A
minimum-weight spanning-tree is a tree
whose weight weight respect to w is the
smallest of all spanning trees of G.


Next:
MST
https://www.cs.rochester.edu/u/gildea/csc282/slides/C23-MST.pdf
https://www.cs.rochester.edu/u/gildea/csc282/slides/C24-SSSP.pdf
https://www.cs.rochester.edu/u/gildea/csc282/slides/C25-APSP.pdf

Ref: 
1. https://www.cs.rochester.edu/u/gildea/csc282/slides/C22-graph.pdf
2. https://www.cs.usfca.edu/~galles/visualization/DFS.html