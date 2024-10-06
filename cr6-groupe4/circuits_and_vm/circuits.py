"""
Authors: Paul Vie, Yanis Lacenne
"""

from collections import defaultdict
from enum import Enum
import networkx as nx
import matplotlib.pyplot as plt


class NodeType(Enum):
    IN = 0
    NOT = 1
    AND = 2
    XOR = 3
    OUT = 4

    def __str__(self):
        if self == self.IN:
            return "IN"

        if self == self.NOT:
            return "NOT"

        if self == self.AND:
            return "AND"

        if self == self.XOR:
            return "XOR"

        if self == self.OUT:
            return "OUT"


class Graph:
    def __init__(self):
        self.vertex = []
        self.edges = defaultdict(list)

    def add_vertex(self, node):
        self.vertex.append(node)

    def add_edge(self, node1, node2):
        self.edges[node1].append(node2)
        node1.childs.append(node2)
        node2.ancestors.append(node1)

    def topological_sort(self):
        visited = set()
        stack = []
        for node in self.vertex:
            if node not in visited:
                self.topological_sort_util(node, visited, stack)
        return stack

    def topological_sort_util(self, node, visited, stack):
        visited.add(node)
        for neighbor in self.edges[node]:
            if neighbor not in visited:
                self.topological_sort_util(neighbor, visited, stack)
        stack.insert(0, node)

    def is_cyclic(self):
        visited = set()
        stack = set()
        for node in self.vertex:
            if node not in visited:
                if self.is_cyclic_util(node, visited, stack):
                    return True
        return False

    def is_cyclic_util(self, node, visited, stack):
        visited.add(node)
        stack.add(node)
        for neighbor in self.edges[node]:
            if neighbor not in visited:
                if self.is_cyclic_util(neighbor, visited, stack):
                    return True
            elif neighbor in stack:
                return True
        stack.remove(node)
        return False

    def __str__(self):
        return str(self.edges)

    def build_in_gate(self, name=None):
        in_node = Node(NodeType.IN, name)
        self.add_vertex(in_node)

        return in_node

    def build_not_gate(self, ancestor):
        not_node = Node(NodeType.NOT)
        self.add_vertex(not_node)
        self.add_edge(ancestor, not_node)

        return not_node

    def build_and_gate(self, ancestor_1, ancestor_2):
        and_node = Node(NodeType.AND)
        self.add_vertex(and_node)
        self.add_edge(ancestor_1, and_node)
        self.add_edge(ancestor_2, and_node)

        return and_node

    def build_xor_gate(self, ancestor_1, ancestor_2):
        xor_node = Node(NodeType.XOR)
        self.add_vertex(xor_node)
        self.add_edge(ancestor_1, xor_node)
        self.add_edge(ancestor_2, xor_node)

        return xor_node

    def build_out_gate(self, ancestor, name=None):
        out_node = Node(NodeType.OUT, name)
        self.add_vertex(out_node)
        self.add_edge(ancestor, out_node)

        return out_node


class Node:
    index = 0

    def __init__(self, type=None, name=None):
        self.index = Node.index
        Node.index += 1
        if name is None:
            self.name = ""
        else:
            self.name = name
        self.type = type
        self.childs = []
        self.ancestors = []
        self.value = None

    def compute_value(self):
        if self.value is not None:
            return self.value

        if self.type == NodeType.NOT:
            self.value = 1 - self.ancestors[0].value
        elif self.type == NodeType.XOR:
            self.value = abs(self.ancestors[0].value - self.ancestors[1].value)
        elif self.type == NodeType.AND:
            self.value = min(self.ancestors[0].value, self.ancestors[1].value)
        elif self.type == NodeType.IN:
            self.value = 0
        else:
            self.value = self.ancestors[0].value

    def add_ancestor(self, ancestor):
        self.ancestors.append(ancestor)

    def add_child(self, child):
        self.childs.append(child)

    def __str__(self):
        return f"{self.type} {self.name} | {self.value}"


def create_min_n(n):
    graph = Graph()

    in_nodes_a = []
    in_nodes_b = []

    last_row_and_nodes = []
    xnor_nodes = []

    for _ in range(n):
        in_nodes_a.append(graph.build_in_gate("A"))

    for _ in range(n):
        in_nodes_b.append(graph.build_in_gate("B"))

    for index in range(n):

        not_node = graph.build_not_gate(in_nodes_a[n - index - 1])
        last_row_and_nodes.append(graph.build_and_gate(in_nodes_b[n - index - 1], not_node))

        if index > 0:
            xor_gate = graph.build_xor_gate(in_nodes_a[n - index - 1], in_nodes_b[n - index - 1])
            xnor_nodes.append(graph.build_not_gate(xor_gate))

    not_nodes_to_xor = []

    index_diff = 0
    while len(last_row_and_nodes) > 1:
        new_last_row = []
        for index in range(len(last_row_and_nodes) - 1):
            new_last_row.append(
                graph.build_and_gate(
                    xnor_nodes[index + index_diff], last_row_and_nodes[index]
                )
            )
        not_nodes_to_xor.append(last_row_and_nodes[-1])
        last_row_and_nodes = new_last_row
        index_diff += 1

    not_nodes_to_xor.append(last_row_and_nodes[-1])

    last_xor = None
    if len(not_nodes_to_xor) == 1:
        last_xor = not_nodes_to_xor[0]
    else:
        last_xor = graph.build_xor_gate(not_nodes_to_xor[0], not_nodes_to_xor[1])
        for index in range(2, len(not_nodes_to_xor)):
            last_xor = graph.build_xor_gate(not_nodes_to_xor[index], last_xor)

    b_gt_a = last_xor
    a_geq_b = graph.build_not_gate(b_gt_a)

    nodes_a_for_output = []
    nodes_b_for_output = []

    for index in range(n):
        node_a = graph.build_and_gate(in_nodes_a[index], b_gt_a)
        nodes_a_for_output.append(node_a)

    for index in range(n):
        node_b = graph.build_and_gate(in_nodes_b[index], a_geq_b)
        nodes_b_for_output.append(node_b)

    result = []

    for index in range(n):
        result.append(
            graph.build_xor_gate(nodes_a_for_output[index], nodes_b_for_output[index])
        )

    output_a = []
    output_b = []

    for index in range(n):
        output_a.append(graph.build_out_gate(result[index], "A"))

    for index in range(n):
        output_b.append(graph.build_out_gate(result[index], "B"))

    return graph, in_nodes_a, in_nodes_b, output_a, output_b


def compute_min(
    g, ina_nodes, inb_nodes, outa_nodes, outb_nodes, ina_values, inb_values
):
    for node, value in zip(ina_nodes, ina_values):
        node.value = value

    for node, value in zip(inb_nodes, inb_values):
        node.value = value

    topoligical_order = g.topological_sort()
    for node in topoligical_order:
        # print(node)
        # print(node.index)
        node.compute_value()
        # print(node.value)


def plot_graph(g):
    """
    visualisation of the graph
    """
    G = nx.DiGraph()
    mapping = {}
    for node in g.vertex:
        mapping[node.index] = str(node.type) + str(node.index)
    for node in g.vertex:
        G.add_node(node.index, value=node.type)
    for node, neighbors in g.edges.items():
        for neighbor in neighbors:
            G.add_edge(node.index, neighbor.index)
    G = nx.relabel_nodes(G, mapping)
    pos = nx.nx_pydot.graphviz_layout(G, prog="dot")
    nx.draw(
        G,
        pos,
        with_labels=True,
        arrows=True,
        font_size=8,
        node_size=500,
        node_color="skyblue",
    )
    plt.show()


def min_n(values_a, values_b):
    assert len(values_a) == len(values_b)

    graph, ina, inb, outa, outb = create_min_n(len(values_a))

    # assert not graph.is_cyclic()

    compute_min(graph, ina, inb, outa, outb, values_a, values_b)

    assert [i.value == j.value for i, j in zip(outa, outb)]

    return [i.value for i in outa]

import argparse
import random
if __name__ == "__main__":
    
    argparse = argparse.ArgumentParser()
    argparse.add_argument(
        "-b",
        type=int,
        help="Number of bits",
        required=True
    )
    
    args = argparse.parse_args()
    graph, _, _, _, _ = create_min_n(args.b)
    plot_graph(graph)
    random_a = [random.randint(0, 1) for _ in range(args.b)]
    random_b = [random.randint(0, 1) for _ in range(args.b)]
    print(min(random_a, random_b)) # expected output
    print(min_n(random_a, random_b))
