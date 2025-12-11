import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dijkstra Visualizer", layout="wide")

st.title("🚦 Interactive Dijkstra's Algorithm Visualizer")

# -----------------------------
# Initialize Graph
# -----------------------------
if "graph" not in st.session_state:
    st.session_state.graph = nx.Graph()
if "edges" not in st.session_state:
    st.session_state.edges = []

G = st.session_state.graph

# -----------------------------
# Sidebar: Add Nodes and Edges
# -----------------------------
st.sidebar.header("Graph Editor")

# Add Node
node_input = st.sidebar.text_input("Add Node (integer)", "")
if st.sidebar.button("Add Node"):
    if node_input.isdigit():
        n = int(node_input)
        if n not in G.nodes():
            G.add_node(n)
            st.success(f"Node {n} added")
        else:
            st.warning("Node already exists")
    else:
        st.error("Enter a valid integer")

# Add Edge
col1, col2, col3 = st.sidebar.columns(3)
u_input = col1.text_input("Node U", "")
v_input = col2.text_input("Node V", "")
weight_input = col3.text_input("Weight", "")

if st.sidebar.button("Add Edge"):
    if u_input.isdigit() and v_input.isdigit() and weight_input.isdigit():
        u, v, w = int(u_input), int(v_input), int(weight_input)
        if u in G.nodes() and v in G.nodes():
            G.add_edge(u, v, weight=w)
            st.session_state.edges.append((u, v, w))
            st.success(f"Edge {u} --{w}--> {v} added")
        else:
            st.error("Both nodes must exist")
    else:
        st.error("Enter valid integers for nodes and weight")

# -----------------------------
# Show current graph
# -----------------------------
st.subheader("Current Graph")
plt.figure(figsize=(6,4))
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_size=700)
labels = nx.get_edge_attributes(G, "weight")
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
st.pyplot(plt)
plt.clf()

# -----------------------------
# Dijkstra Algorithm
# -----------------------------
def dijkstra(graph, source):
    dist = {n: float('inf') for n in graph.nodes()}
    parent = {n: None for n in graph.nodes()}
    dist[source] = 0
    visited = set()
    while len(visited) < len(graph.nodes()):
        u = min((n for n in graph.nodes() if n not in visited), key=lambda n: dist[n], default=None)
        if u is None:
            break
        visited.add(u)
        for v in graph.neighbors(u):
            w = graph[u][v]["weight"]
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
    return dist, parent

# -----------------------------
# Run Dijkstra
# -----------------------------
if len(G.nodes()) > 0:
    st.subheader("Run Dijkstra Algorithm")
    col1, col2 = st.columns(2)
    source_node = col1.number_input("Source Node", min_value=0, value=min(G.nodes()))
    dest_node = col2.number_input("Destination Node", min_value=0, value=min(G.nodes()))

    if st.button("Compute Shortest Path"):
        if source_node not in G.nodes() or dest_node not in G.nodes():
            st.error("Source/Destination node does not exist")
        else:
            dist, parent = dijkstra(G, source_node)
            
            # Distance table
            st.subheader("📏 Distance Table")
            st.table({"Node": list(dist.keys()), "Distance": list(dist.values())})
            
            # Parent table
            st.subheader("🧭 Predecessor Table")
            st.table({"Node": list(parent.keys()), "Parent": [p if p is not None else "-" for p in parent.values()]})
            
            # Shortest Path
            path = []
            temp = dest_node
            while temp is not None:
                path.append(temp)
                temp = parent[temp]
            path.reverse()
            
            st.success(f"Shortest Path: {' → '.join(map(str, path))}")
            
            # Plot graph with highlighted path
            plt.figure(figsize=(6,4))
            nx.draw(G, pos, with_labels=True, node_size=700)
            labels = nx.get_edge_attributes(G,"weight")
            nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
            
            edges_on_path = list(zip(path, path[1:]))
            nx.draw_networkx_nodes(G,pos,nodelist=path,node_color="yellow")
            nx.draw_networkx_edges(G,pos,edgelist=edges_on_path,width=4,edge_color="red")
            
            st.pyplot(plt)
            plt.clf()
