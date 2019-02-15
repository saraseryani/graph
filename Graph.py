import random


# Custom Graph error
class GraphError(Exception): pass


class Graph:
    """
    Graph Class ADT
    """

    class Edge:
        """
        Class representing an Edge in the Graph
        """
        __slots__ = ['source', 'destination']

        def __init__(self, source, destination):
            """
            DO NOT EDIT THIS METHOD!
            Class representing an Edge in a graph
            :param source: Vertex where this edge originates
            :param destination: ID of Vertex where this edge ends
            """
            self.source = source
            self.destination = destination

        def __eq__(self, other):
            return self.source == other.source and self.destination == other.destination

        def __repr__(self):
            return f"Source: {self.source} Destination: {self.destination}"

        __str__ = __repr__

    class Path:
        """
        Class representing a Path through the Graph
        """
        __slots__ = ['vertices']

        def __init__(self, vertices=[]):
            """
            DO NOT EDIT THIS METHOD!
            Class representing a path in a graph
            :param vertices: Ordered list of vertices that compose the path
            """
            self.vertices = vertices

        def __eq__(self, other):
            return self.vertices == other.vertices

        def __repr__(self):
            return f"Path: {' -> '.join([str(v) for v in self.vertices])}\n"

        __str__ = __repr__

        def add_vertex(self, vertex):
            """
            adds vertex
            :param vertex: the vertex to be added
            :return: none
            """
            self.vertices.append(vertex)

        def remove_vertex(self):
            """
            removes the last vertex
            :return: none
            """
            if len(self.vertices) != 0:
                self.vertices.pop()

        def last_vertex(self):
            """
            returns the last item in the list
            :return: last vertex
            """
            if len(self.vertices) == 0:
                return None
            return self.vertices[-1]

        def is_empty(self):
            """
            Checks to see if it is empty
            :return: boolean if its true or false
            """
            if len(self.vertices) == 0:
                return True
            return False

    class Vertex:
        """
        Class representing a Vertex in the Graph
        """
        __slots__ = ['ID', 'edges', 'visited', 'fake']

        def __init__(self, ID):
            """
            Class representing a vertex in the graph
            :param ID : Unique ID of this vertex
            """
            self.edges = []
            self.ID = ID
            self.visited = False
            self.fake = False

        def __repr__(self):
            return f"Vertex: {self.ID}"

        __str__ = __repr__

        def __eq__(self, other):
            """
            DO NOT EDIT THIS METHOD
            :param other: Vertex to compare
            :return: Bool, True if same, otherwise False
            """
            if self.ID == other.ID and self.visited == other.visited:
                if self.fake == other.fake and len(self.edges) == len(other.edges):
                    edges = set((edge.source.ID, edge.destination) for edge in self.edges)
                    difference = [e for e in other.edges if (e.source.ID, e.destination) not in edges]
                    if len(difference) > 0:
                        return False
                    return True

        def add_edge(self, destination):
            """

            :param destination:
            :return: none
            """
            self.edges.append(Graph.Edge(self, destination))

        def degree(self):
            """
            gets the degree
            :return: degree
            """
            return len(self.edges)

        def get_edge(self, destination):
            """

            :param destination:
            :return:
            """
            for i in self.edges:
                if i.destination != destination:
                    return None
                return i

        def get_edges(self):
            """

            :return:
            """
            return self.edges

        def set_fake(self):
            """

            :return: True
            """
            self.fake = True

        def visit(self):
            """

            :return: boolean
            """
            self.visited = True

    def __init__(self, size=0, connectedness=1, filename=None):
        """
        DO NOT EDIT THIS METHOD
        Construct a random DAG
        :param size: Number of vertices
        :param connectedness: Value from 0 - 1 with 1 being a fully connected graph
        :param: filename: The name of a file to use to construct the graph.
        """
        assert connectedness <= 1
        self.adj_list = {}
        self.size = size
        self.connectedness = connectedness
        self.filename = filename
        self.construct_graph()

    def __eq__(self, other):
        """
        DO NOT EDIT THIS METHOD
        Determines if 2 graphs are IDentical
        :param other: Graph Object
        :return: Bool, True if Graph objects are equal
        """
        if len(self.adj_list) == len(other.adj_list):
            for key, value in self.adj_list.items():
                if key in other.adj_list:
                    if not self.adj_list[key] == other.adj_list[key]:
                        return False
                else:
                    return False
            return True
        return False

    def generate_edges(self):
        """
        DO NOT EDIT THIS METHOD
        Generates directed edges between vertices to form a DAG
        :return: A generator object that returns a tuple of the form (source ID, destination ID)
        used to construct an edge
        """
        random.seed(10)
        for i in range(self.size):
            for j in range(i + 1, self.size):
                if random.randrange(0, 100) <= self.connectedness * 100:
                    yield [i, j]

    def get_vertex(self, ID):
        """

        :param ID:
        :return:
        """
        if len(self.adj_list) == 0:
            return None

        if ID in self.adj_list:
            return self.adj_list[ID]
        return None

    def construct_graph(self):
        """
        Constructs a graph
        :return: graph or error
        """

        if self.filename:
            try:
                file = open(self.filename)
            except FileNotFoundError:
                raise GraphError

            for i in file:
                i = i.strip().split()
                adj_list = self.adj_list

                if len(i) != 2:
                    raise GraphError
                if int(i[0]) is None or int(i[1]) is None:
                    raise GraphError

                if int(i[0]) not in adj_list:
                    adj_list[int(i[0])] = self.Vertex(int(i[0]))
                if int(i[1]) not in adj_list:
                    adj_list[int(i[1])] = self.Vertex(int(i[1]))
                new_edge = adj_list[int(i[0])]
                new_edge.add_edge(int(i[1]))

        if self.filename == None:
            if self.connectedness > 1 and self.connectedness <= 0:
                raise GraphError
            if self.size <= 0:
                raise GraphError

            for k, v in self.generate_edges():
                if self.get_vertex(k) is None: #check if theres no verticies
                    value = self.Vertex(k)
                    self.adj_list[k] = value
                if self.get_vertex(v) is None:
                    value = self.Vertex(v)
                    self.adj_list[v] = value

                value = self.adj_list[k]
                value.add_edge(v)


    def BFS(self, start, target):
        """
        Breath first traversal
        :param start: starting
        :param target: search item
        :return: item searched for
        """
        path = [self.Path([start])]

        while path:
            first = path.pop(0)
            if first.last_vertex() == target:
                return first
            else:
                for i in self.get_vertex(first.last_vertex()).edges:
                    dest = i.destination
                    path.append(self.Path(first.vertices + [dest]))
        return self.Path()


    def DFS(self, start, target, path=Path()):
        """
        Depth first search traversal
        :param start: vertex
        :param target: item you're searching for
        :param path: path youre going to
        :return: item you're searching for
        """
        path.add_vertex(start)

        if self.get_vertex(start).visited == False:
            self.get_vertex(start).visit()

        for i in self.get_vertex(start).get_edges():
            path_target = i.destination
            if path_target == target:
                path.add_vertex(path_target)
                return path
            self.DFS(path_target, target, path)
            if path.last_vertex() == target:
                return path
        path.remove_vertex()


def fake_emails(graph, mark_fake=False):
    """
    Verifies the emails
    :param graph: graph you're searching
    :param mark_fake: if it's fake
    :return: list of the fake emails
    """
    return_list = []
    def check_fake_emails(start, emails=list()):
        """
        checks list of emails to find fake email
        :param start: start of the list
        :param emails: email to be checked
        :return: none
        """
        graph_vertex = graph.get_vertex(start)
        if graph_vertex.visited == False:
            graph_vertex.visit()
            if graph_vertex.degree() == 0:
                if mark_fake == True:
                    graph_vertex.set_fake()
                return_list.append(graph_vertex.ID)
            for i in graph_vertex.get_edges()[:]:
                check_fake_emails(i.destination, return_list)
                if graph.get_vertex(i.destination).fake:
                    graph_vertex.get_edges().remove(i)
    for i in graph.adj_list.values():
        if i.visited == False:
            check_fake_emails(i.ID, return_list)
    return return_list


