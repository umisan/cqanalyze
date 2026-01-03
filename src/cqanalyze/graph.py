from collections import deque
from cqanalyze.models import Relation, Query, Node, Edge, Graph

def construct_line_graph(query: Query) -> Graph:
    nodes = [Node(relation.name) for relation in query.relations]
    edges = []
    for i in range(0, len(query.relations)):
        for j in range(i + 1, len(query.relations)):
            attribute_set_i = set(query.relations[i].attributes)
            attribute_set_j = set(query.relations[j].attributes)
            if len(attribute_set_i.intersection(attribute_set_j)) > 0:
                edges.append(Edge(Node(query.relations[i].name), Node(query.relations[j].name)))
    return Graph(nodes = nodes, edges = edges)

# initial value is -1
# visited = 0 or 1
def is_bipartite_graph(graph: Graph) -> bool:
    colors = {}
    for node in graph.nodes:
        colors[node.identifier] = -1
    q = deque()
    q.append(graph.nodes[0].identifier)
    colors[0] = 0
    while len(q) != 0:
        current_node_identifier = q.pop()
        current_node_color = colors[current_node_identifier]
        next_color = 0 if current_node_color == 1 else 1
        for child in graph.adjacent_list[current_node_identifier]:
            if colors[child.identifier] == -1:
                colors[child.identifier] = next_color
                q.append(child.identifier)
            elif colors[child.identifier] == next_color:
                continue
            else:
                return False
    return True
