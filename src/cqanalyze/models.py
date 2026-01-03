from dataclasses import dataclass

@dataclass(frozen=True)
class Relation:
    name: str
    attributes: list[str]

@dataclass(frozen=True)
class Query:
    relations: list[Relation]

@dataclass(frozen=True)
class Node:
    identifier: str

@dataclass(frozen=True)
class Edge:
    node1: Node
    node2: Node

class Graph:
    def __init__(self, nodes: list[Node], edges: list[Edge]):
        self.nodes = nodes
        self.adjacent_list = {}
        # initialize adjacent_list
        for node in nodes:
            self.adjacent_list[node.identifier] = []
        for edge in edges:
            if edge.node2 not in self.adjacent_list[edge.node1.identifier]:
                self.adjacent_list[edge.node1.identifier].append(edge.node2)
            if edge.node1 not in self.adjacent_list[edge.node2.identifier]:
                self.adjacent_list[edge.node2.identifier].append(edge.node1) 
