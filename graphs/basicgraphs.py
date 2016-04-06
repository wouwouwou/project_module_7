"""
This is a module for working with *undirected* graphs (simple graphs or multigraphs).

It contains three classes: vertex, edge and graph. 

The interface of these classes is extensive and allows programming all kinds of graph algorithms.

However, the data structure used is quite basic and inefficient: a graph object stores only a vertex list and
an edge list, and methods such as adjacency testing / finding neighbors of a vertex require going through the
entire edge list!
"""

# version: 29-01-2015, Paul Bonsma

unsafe = False

# Set to True for faster, but unsafe listing of all vertices and edges.


class GraphError(Exception):
    def __init__(self, message):
        self.mess = message

    def __str__(self):
        return self.mess


class vertex:
    """
    Vertex objects have an attribute <_graph> pointing to the graph they are part of,
    and an attribute <_label> which can be anything: it is not used for any methods,
    except for __repr__. It contains getters and setters for each attribute.
    """

    def __init__(self, graph, label=0):
        """
        Creates a vertex, part of <graph>, with optional label <label>.
        (Labels of different vertices may be chosen the same; this does
        not influence correctness of the methods, but will make the string
        representation of the graph ambiguous.)
        """
        self._graph = graph
        self._label = label
        self.colornum = 0
        self._inclist = []

    def __repr__(self):
        return str(self._label)

    def getgraph(self):
        return self._graph

    def setgraph(self, graph):
        self._graph = graph

    def getlabel(self):
        return self._label

    def setlabel(self, label):
        self._label = label

    def getcolornum(self):
        return self.colornum

    def setcolornum(self, colornum):
        self.colornum = colornum

    def getinclist(self):
        return self._inclist[:]

    def setinclist(self, inclist):
        self._inclist = inclist

    def nbcolornums(self):
        colornums = []
        for v in self.nbs():
            colornums.append(v.colornum)
        return colornums

    def adj(self, other):
        """
        Returns True iff vertex <self> is adjacent to <other> vertex.

        :param other: The <other> vertex which could be adjacent to the <self> vertex
        """
        return self._graph.adj(self, other)

    def nbs(self):
        """
        Returns the list of neighbors of vertex <self>.
        In case of parallel edges: duplicates are not removed from this list!
        """
        nbl = []
        for e in self.getinclist():
            nbl.append(e.otherend(self))
        return nbl

    def deg(self):
        """
        Returns the degree of vertex <self>.
        """
        return len(self.getinclist())


class edge:
    """
    Edges have attributes <_tail> and <_head> which point to the end vertices
    (vertex objects). The order of these is arbitrary (undirected edges).
    """

    def __init__(self, tail, head):
        """
        Creates an edge between vertices <tail> and <head>.
        """
        # tail and head must be vertex objects.
        if not tail.getgraph() == head.getgraph():
            raise GraphError(
                'Can only add edges between vertices of the same graph')
        self._tail = tail
        self._head = head

    def __repr__(self):
        return '(' + str(self._tail) + ',' + str(self._head) + ')'

    def tail(self):
        return self._tail

    def head(self):
        return self._head

    def otherend(self, oneend):
        """
        Given one end vertex <oneend> of the edge <self>, this returns
        the other end vertex of <self>.

        :param oneend: One of the end vertices <oneend> of the edge <self>
        """
        # <oneend> must be either the head or the tail of this edge.
        if self._tail == oneend:
            return self._head
        elif self._head == oneend:
            return self._tail
        raise GraphError(
            'edge.otherend(oneend): oneend must be head or tail of edge')

    def incident(self, v):
        """
        Returns True iff the edge <self> is incident with the
        vertex <vertex>.

        :param v: The vertex <vertex> the edge <self> should be incident with.
        """
        if self.tail() == v or self.head() == v:
            return True
        else:
            return False


class graph:
    """
    A graph object has as main attributes:
     <_V>: the list of its vertices
     <_E>: the list of its edges
    In addition:
     <_simple> is True iff the graph must stay simple (used when trying to add edges)
     <_directed> is False for now (feel free to write a directed variant of this
        module)
     <_nextlabel> is used to assign default labels to vertices.
    """

    def __init__(self, n=0, simple=False):
        """
        Creates a graph.
        Optional argument <n>: number of vertices.
        Optional argument <simple>: indicates whether the graph should stay simple.
        """
        self._V = []
        self._E = []
        self._directed = False
        # may be changed later for a more general version that can also
        # handle directed graphs.
        self._simple = simple
        self._nextlabel = 0
        self._coloring = dict()
        for i in range(n):
            self.addvertex()

    def __repr__(self):
        return 'V=' + str(self._V) + '\nE=' + str(self._E)

    def V(self):
        """
        Returns the list of vertices of the graph.
        """
        if unsafe:  # but fast
            return self._V
        else:
            return self._V[:]  # return a *copy* of this list

    def E(self):
        """
        Returns the list of edges of the graph.
        """
        if unsafe:  # but fast
            return self._E
        else:
            return self._E[:]  # return a *copy* of this list

    def __getitem__(self, i):
        """
        Returns the <i>th vertex of the graph -- as given in the vertex list;
        this is not related to the vertex labels.
        """
        return self._V[i]

    def getcoloring(self):
        return self._coloring

    def setcoloring(self, a):
        self._coloring = a
        for key in a.keys():
            vertices = a[key]
            for v in vertices:
                v.setcolornum(key)

    def getslowcoloring(self):
        res = []
        for v in self.V():
            res.append(v.getcolornum())
        return res

    def isdirected(self):
        """
        Returns False, because for now these graphs are always undirected.
        """
        return self._directed

    def addvertex(self, label=-1):
        """
        Add a vertex to the graph.
        Optional argument: a vertex label (arbitrary)
        :param label: The optional vertex label.
        """
        if label == -1:
            label = self._nextlabel
            self._nextlabel += 1
        u = vertex(self, label)
        self._V.append(u)
        return u

    def addedge(self, tail, head):
        """
        Add an edge to the graph between <tail> and <head>.
        Includes some checks in case the graph should stay simple.
        :param head: The head vertex of the edge
        :param tail: The tail vertex of the edge
        """
        if self._simple:
            if tail == head:
                raise GraphError('No loops allowed in simple graphs')
            for e in self._E:
                if e.tail() == tail and e.head() == head:
                    raise GraphError(
                        'No multiedges allowed in simple graphs')
                if not self._directed:
                    if e.tail() == head and e.head() == tail:
                        raise GraphError(
                            'No multiedges allowed in simple graphs')
        if not (tail.getgraph() == self and head.getgraph() == self):
            raise GraphError(
                'Edges of a graph G must be between vertices of G')
        e = edge(tail, head)
        self._E.append(e)

        i = tail.getinclist()
        i.append(e)
        tail.setinclist(i)

        j = head.getinclist()
        j.append(e)
        head.setinclist(j)
        return e

    def findedge(self, u, v):
        """
        If <u> and <v> are adjacent, this returns an edge between them.
        (Arbitrary in the case of multigraphs.)
        Otherwise this returns <None>.
        :param v: vertex v
        :param u: vertex u
        """
        if len(u.getinclist()) < len(v.getinclist()):
            for e in u.getinclist():
                if e.head() == v or e.tail() == v:
                    return e
        else:
            for e in v.getinclist():
                if e.tail() == u or e.head() == u:
                    return e
        return None

    def adj(self, u, v):
        """
        Returns True iff vertices <u> and <v> are adjacent.
        :param v: vertex v
        :param u: vertex u
        """
        if self.findedge(u, v) is None:
            return False
        else:
            return True

    def getvwithcolornum(self, colornum):
        vs = []
        for v in self.V():
            if v.colornum == colornum:
                vs.append(v)
        return vs

    def maxcolornum(self):
        maxcolornum = 0
        for v in self.V():
            if v.colornum > maxcolornum:
                maxcolornum = v.colornum
        return maxcolornum

    def degset(self):
        degs = set()
        for v in self.V():
            degs.add(v.deg())
        return degs

    def degtocol(self):
        degs = self.degset()
        degcol = dict()
        i = 0
        for d in degs:
            degcol[d] = i
            i += 1
        return degcol
