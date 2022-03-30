class Node:
    """
    Node representation in a graph.
    It keeps a list of next and previous nodes based on created edges.
    """

    def __init__(self,
                 name: str):
        self.name: str = name
        self.value = 0
        self.next_nodes: dict[str, tuple[Node, Edge]] = dict()
        self.previous_nodes: dict[str, tuple[Node, Edge]] = dict()

    def __repr__(self):
        return self.name


class Edge:
    def __init__(self,
                 tail: Node,
                 head: Node,
                 capacity: int = float("inf"),
                 flow: int = 0):
        self.tail = tail
        self.head = head
        self.capacity = capacity
        self.flow = flow

        # Update node dependencies
        self.tail.next_nodes[self.head.name] = (self.head, self)
        self.head.previous_nodes[self.tail.name] = (self.tail, self)

    @property
    def tuple(self):
        return self.tail, self.head

    def __repr__(self):
        return "(%s->%s,%d[%d])" % (self.tail.name, self.head.name, self.flow, self.capacity)


class Graph:
    def __init__(self):
        self.nodes: dict[str, Node] = dict()
        self.edges: dict[tuple[Node, Node], Edge] = dict()

    def __repr__(self):
        return str(list(self.nodes.keys())) + str(list(self.edges.values()))

    def add_edge(self, edge: Edge):
        """
        Adds edge to the current graph.
        If the edge already exists, it is overwritten with the new provided one.
        """

        self.edges[edge.tuple] = edge
        self.nodes[edge.head.name] = edge.head
        self.nodes[edge.tail.name] = edge.tail

    def add_edges(self, edges: list[Edge]):
        for edge in edges:
            self.add_edge(edge)

    def edge(self, head: Node, tail: Node):
        """
        Returns an edge from its tuple description.
        Defaults to None if the edge doesn't exist in the graph.
        """

        try:
            return self.edges[(head, tail)]
        except KeyError:
            return None

    def ford_fulkerson(self, source_str: str, sink_str: str):
        """
        Applies the Ford-Fulkerson algorithm to find a maximum flow.
        """

        # Reset flow
        for edge in self.edges.values():
            edge.flow = 0

        source = self.nodes[source_str]
        sink = self.nodes[sink_str]
        while True:
            found, backtrack_dict = self.__find_incrementing_path(source, sink)
            if found:
                self.__increment_flow(source, sink, backtrack_dict)
            else:
                return

    def __increment_flow(self,
                         source: Node,
                         sink: Node,
                         backtrack_dict: dict[str, tuple[Node, Edge, int]]):
        tail = sink

        while True:
            head, edge, epsilon = backtrack_dict[tail.name]
            edge.flow += epsilon * sink.value
            if head == source:
                return
            tail = head


    def __find_incrementing_path(self,
                                 source: Node,
                                 sink: Node):
        pred: dict[str, tuple[Node, Edge, int]] = dict()

        source.value = float("inf")
        L: dict[str, Node] = dict()
        L[source.name] = source

        Z: dict[str, Node] = dict()

        while True:
            # "Random" element in heads but not in tails
            diff_set = set(L.values()) - set(Z.values())
            x: Node = diff_set.pop()
            Z[x.name] = x

            # Inspect outward edges
            y: Node
            a: Edge
            for (y, a) in x.next_nodes.values():
                if not L.get(y.name) and a.flow < a.capacity:
                    y.value = min(x.value, a.capacity - a.flow)
                    L[y.name] = y
                    pred[y.name] = x, a, +1

            # Inspect inward edges
            y: Node
            a: Edge
            for (y, a) in x.previous_nodes.values():
                if not L.get(y.name) and a.flow > 0:
                    y.value = min(x.value, a.flow)
                    L[y.name] = y
                    pred[y.name] = x, a, -1

            if L.get(sink.name):
                found = True
                return found, pred

            diff_set = set(L.values()) - set(Z.values())
            if len(diff_set) == 0:
                not_found = False
                return not_found, pred


def main():
    q: int = 5

    s = Node("s")
    x = Node("x")
    y = Node("y")
    z = Node("z")
    t = Node("t")
    u = Node("u")
    v = Node("v")
    w = Node("w")

    sx = Edge(s, x, capacity=q)
    xy = Edge(x, y, capacity=q)
    yz = Edge(y, z, capacity=q)
    zt = Edge(z, t, capacity=q)
    su = Edge(s, u, capacity=q)
    uv = Edge(u, v, capacity=q)
    vw = Edge(v, w, capacity=q)
    wt = Edge(w, t, capacity=q)
    yv = Edge(y, v, capacity=1)

    g = Graph()
    g.add_edges([sx, xy, yz, zt, su, uv, vw, wt, yv])

    g.ford_fulkerson(s.name, t.name)

    print(g)


if __name__ == "__main__":
    main()

