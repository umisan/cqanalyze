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

def is_bipartite_graph(graph: Graph) -> bool:
    _, is_bipartite = _color_graph(graph)
    return is_bipartite

def calc_maximum_matching(graph: Graph) -> list[Edge]:
    colors, is_bipartite = _color_graph(graph)
    if not is_bipartite:
        raise ValueError("calc_maximum_matching supports only bipartite graphs")

    left_partition = [
        node.identifier for node in graph.nodes if colors[node.identifier] == 0
    ]
    pair_left = {node.identifier: None for node in graph.nodes}
    pair_right = {node.identifier: None for node in graph.nodes}
    distances = {}

    def bfs() -> bool:
        q = deque()
        found_augmenting_path = False

        for left in left_partition:
            if pair_left[left] is None:
                distances[left] = 0
                q.append(left)
            else:
                distances[left] = -1

        while len(q) != 0:
            current_left = q.popleft()
            for right in graph.adjacent_list[current_left]:
                matched_left = pair_right[right.identifier]
                if matched_left is None:
                    found_augmenting_path = True
                elif distances[matched_left] == -1:
                    distances[matched_left] = distances[current_left] + 1
                    q.append(matched_left)
        return found_augmenting_path

    def dfs(left: str) -> bool:
        for right in graph.adjacent_list[left]:
            matched_left = pair_right[right.identifier]
            if matched_left is None or (
                distances.get(matched_left, -1) == distances[left] + 1 and dfs(matched_left)
            ):
                pair_left[left] = right.identifier
                pair_right[right.identifier] = left
                return True
        distances[left] = -1
        return False

    while bfs():
        for left in left_partition:
            if pair_left[left] is None:
                dfs(left)

    matching = []
    for left in left_partition:
        right = pair_left[left]
        if right is not None:
            matching.append(Edge(Node(left), Node(right)))
    return matching

def _color_graph(graph: Graph) -> tuple[dict[str, int], bool]:
    colors = {node.identifier: -1 for node in graph.nodes}
    if len(graph.nodes) == 0:
        return colors, True

    q = deque([graph.nodes[0].identifier])
    colors[graph.nodes[0].identifier] = 0

    while len(q) != 0:
        current_node_identifier = q.popleft()
        current_node_color = colors[current_node_identifier]
        next_color = 0 if current_node_color == 1 else 1
        for child in graph.adjacent_list[current_node_identifier]:
            if colors[child.identifier] == -1:
                colors[child.identifier] = next_color
                q.append(child.identifier)
            elif colors[child.identifier] == current_node_color:
                return colors, False

    return colors, True
