import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import heapq

st.set_page_config(page_title="MST Visualizer", layout="wide")

# Graph stored in session_state
if "G" not in st.session_state:
    st.session_state.G = nx.Graph()


def draw_graph(G, highlight_edges=None):
    fig, ax = plt.subplots()
    pos = nx.spring_layout(G)

    nx.draw(G, pos, with_labels=True, node_color='lightblue', ax=ax, node_size=600)

    if highlight_edges:
        nx.draw_networkx_edges(G, pos, edgelist=highlight_edges, width=3, edge_color='red')

    st.pyplot(fig)


def kruskal_mst(G):
    edges = sorted(G.edges(data=True), key=lambda x: x[2]['weight'])
    parent = {}
    rank = {}

    def find(node):
        if parent[node] != node:
            parent[node] = find(parent[node])
        return parent[node]

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            if rank[ra] < rank[rb]:
                parent[ra] = rb
            else:
                parent[rb] = ra
                if rank[ra] == rank[rb]:
                    rank[ra] += 1

    for node in G.nodes():
        parent[node] = node
        rank[node] = 0

    mst_edges = []
    steps = []

    for u, v, w in edges:
        if find(u) != find(v):
            union(u, v)
            mst_edges.append((u, v))
            steps.append(mst_edges.copy())

    return steps


def prim_mst(G, start):
    visited = set([start])
    edges = [(G[start][v]['weight'], start, v) for v in G.neighbors(start)]
    heapq.heapify(edges)

    mst_edges = []
    steps = [mst_edges.copy()]

    while edges:
        weight, u, v = heapq.heappop(edges)
        if v not in visited:
            visited.add(v)
            mst_edges.append((u, v))
            steps.append(mst_edges.copy())

            for w in G.neighbors(v):
                if w not in visited:
                    heapq.heappush(edges, (G[v][w]['weight'], v, w))

    return steps


def bfs(G, start):
    visited = []
    queue = [start]

    while queue:
        node = queue.pop(0)
        if node not in visited:
            visited.append(node)
            queue.extend(list(G.neighbors(node)))

    return visited


def dfs(G, start, visited=None):
    if visited is None:
        visited = []
    visited.append(start)
    for neighbor in G.neighbors(start):
        if neighbor not in visited:
            dfs(G, neighbor, visited)
    return visited


st.title("🌐 Minimum Spanning Tree Visualizer")

with st.sidebar:
    st.header("Graph Controls")

    option = st.selectbox("Choose action", ["Add Node", "Add Edge", "Delete Node"])

    if option == "Add Node":
        node = st.text_input("Enter node name")
        if st.button("Add Node"):
            st.session_state.G.add_node(node)

    elif option == "Add Edge":
        u = st.text_input("Node 1")
        v = st.text_input("Node 2")
        w = st.number_input("Weight", 1, 100)
        if st.button("Add Edge"):
            st.session_state.G.add_edge(u, v, weight=w)

    elif option == "Delete Node":
        node = st.text_input("Node to delete")
        if st.button("Delete Node"):
            if node in st.session_state.G:
                st.session_state.G.remove_node(node)

    st.write("---")
    st.write("### Traversal")
    start_node = st.text_input("Start Node for Traversal")
    if st.button("BFS"):
        st.write("BFS Order:", bfs(st.session_state.G, start_node))
    if st.button("DFS"):
        st.write("DFS Order:", dfs(st.session_state.G, start_node))


st.write("### Current Graph")
draw_graph(st.session_state.G)

st.write("---")
st.write("### Minimum Spanning Tree")

col1, col2 = st.columns(2)

with col1:
    if st.button("Run Kruskal's Algorithm"):
        steps = kruskal_mst(st.session_state.G)
        for step in steps:
            st.write("Step:", step)
            draw_graph(st.session_state.G, highlight_edges=step)

with col2:
    start = st.text_input("Start Node for Prim's Algorithm")
    if st.button("Run Prim's Algorithm"):
        if start:
            steps = prim_mst(st.session_state.G, start)
            for step in steps:
                st.write("Step:", step)
                draw_graph(st.session_state.G, highlight_edges=step)
