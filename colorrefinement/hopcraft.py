import unittest

from graphs.graphIO import loadgraph, writeDOT
import time
from graphs.basicgraphs import graph


class Node(object):

    def __init__(self, data, prev, next):
        self.data = data
        self.prev = prev
        self.next = next


class ListIterator(object):
    def __init__(self, node):
        self.current = node

    def __iter__(self):
        return self

    def __next__(self):
        if self.current is None:
            raise StopIteration()

        result = self.current.data
        self.current = self.current.next

        return result


class DoubleList(object):
    head = None
    tail = None
    length = 0

    def __iter__(self):
        return ListIterator(self.head)

    @property
    def size(self):
        return self.length

    @size.setter
    def size(self, value):
        self.length = value

    def append(self, data):
        new_node = Node(data, None, None)
        if self.head is None:
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            new_node.next = None
            self.tail.next = new_node
            self.tail = new_node
        self.size = self.size + 1

    def remove(self, nodevalue):
        currentnode = self.head
        self.length -= 1

        while currentnode is not None:
            if currentnode.data == nodevalue:
                if currentnode.prev is not None:
                    currentnode.prev.next = currentnode.next
                    currentnode.next.prev = currentnode.prev
                else:
                    self.head = currentnode.next
                    currentnode.next.prev = None
            currentnode = currentnode.next

    def show(self):
        print("Show list data:")
        currentnode = self.head
        while currentnode is not None:
            print(currentnode.prev.data if hasattr(currentnode.prev, "data") else None)
            print(currentnode.data)
            print(currentnode.next.data if hasattr(currentnode.next, "data") else None)
            currentnode = currentnode.next
        print("*" * 50)


def neighbourlist(g: graph, directed=False):
    """
     Generate an incoming list for given vertices.
     Set directed to True if the graph is directed.
     :param directed:
     :param g:
    """
    result = dict()
    for v in g.V():
        result[v] = set()
    for e in g.E():
        result[e.tail()].add(e.head())
        if not directed:
            result[e.head()].add(e.tail())
    return result

def fasthopcraft(g: graph):
    nbl = neighbourlist(g, g.isdirected())

    queue = set()
    dll = dict()
    inqueue = dict()
    color = dict()
    maxl = 0
    maxxl = 0

    # Set initial coloring
    for key, neighbours in nbl.items():
        # Setup queue that contains colors that need to be refined
        if not len(neighbours) in queue: # No duplicates
            queue.add(len(neighbours))
            inqueue[len(neighbours)] = True
            maxl = max(len(neighbours), maxl)
            maxl = max(len(neighbours), maxxl)

    for v in g.V():
        if not len(nbl[v]) in dll.keys():
            dll[len(nbl[v])] = DoubleList()
        dll[len(nbl[v])].append(v)

    while queue:
        l = set()
        a = dict()

        # In time O(|E-(C)|) loop dll
        ci = queue.pop()
        print(ci)
        print(dll[ci].show())
        for q in dll[ci]:

            print(nbl)
            """
            for qa in nbl[q]:
                print(qa)
                if color[qa] not in l:
                    l.add(color[qa])
                if color[qa] not in a.keys():
                    a[color[qa]] = 1
                else:
                    a[color[qa]] += 1
            """
        print(l)
        print(a)
        for i in l:
            print("test")
            print(a[i])
            print(dll[ci].size)
            if a[i] < dll[1].size:
                maxl += 1
                if a[i] < (len(ci) / 2):
                    queue.add(i)
                    print("adding i to queue")
                    pass
                elif a[i] > (len(ci) / 2):
                    queue.add(maxl)
                    print("adding maxl to queue")
                    pass
                color[i] = dll[i]
                color[l] = dll[ci] - dll[i]
            else:
                print("same size")

    # Return graph
    for v in g.V():
        v.colornum = color[v]
    return g

def generatePfromColors(G):
    p = []
    colors = dict()
    for v in G.V():
        if v.colornum in colors.keys():
            colors[v.colornum].add(v)
        else:
            colors[v.colornum] = {v}
    keys = list(colors.keys())
    for key in keys:
        p.append(colors[key])
    return p

def writeColors(partitions):
    for i in range(len(partitions)):
        for v in partitions[i]:
            v.colornum = i

def hopcraft(g: graph, usecolors=False):
    """
     Generate a Minimum DFA as described by the Hopcroft's algorithm
     This algorithm has a worst-case complexity of O(ns log n), with n the number of states and s the different amount of degrees.
     @see https://en.wikipedia.org/wiki/DFA_minimization#Hopcroft.27s_algorithm
     @see https://riunet.upv.es/bitstream/handle/10251/27623/partial%20rev%20determ.pdf?sequence=1 Algorithm 6.1
     :param smallestpartition: Select the smallest partition to refine first.
     :param g: The graph
    """

    neighbours = neighbourlist(g, g.isdirected())
    p = []
    pSplit = []
    degrees = dict()
    for v in g.V():
        degree = len(neighbours[v])
        if degrees.get(degree, -1) == -1:
            degrees[degree] = {v}
        else:
            degrees[degree].add(v)

    if usecolors:
        p = generatePfromColors(g)
        pSplit = generatePfromColors(g)
    else:
        for k in degrees:
            p.append(degrees[k])
            pSplit.append(degrees[k])

    w = set(range(len(p)))
    while w:
        #print("w: ", w)
        #print("wl: ", [(c, len(p[c])) for c in w])
        aN = w.pop()
        a = p[aN]
        nbs = set()
        for va in a:
            nbs |= neighbours[va]
        # print("nbs: ", nbs)
        for color in pSplit:
            x = nbs & color
            # print("nbs & color: ", x)
            if x:
                for yN in range(len(p)):
                    if len(p[yN]) > 1:
                        y = p[yN]
                        both = x & y
                        ynotx = y - x
                        if both and ynotx:
                            p[yN] = both
                            p.append(ynotx)
                            if yN in w:
                                w.add(len(p) - 1)
                            else:
                                if len(both) <= len(ynotx):
                                    w.add(yN)
                                else:
                                    w.add(len(p) - 1)
    r = dict()
    count = 0
    for ap in p:
        r[count] = ap
        count += 1

    return r



def fastautomorphismcount(g: graph):
    """
    Calculate the amount of automorphisms of one graph.
    :param g:
    :return:
    """
    coloring = hopcraft(g, False)
    isomorphisms = 1
    for cl in range(len(coloring)):
        isomorphisms *= len(coloring[cl])
    return isomorphisms


class TestColorRefinement(unittest.TestCase):
    def testIsomorphismCount(self):
        start = time.time()

        # Load a Python tuple of length 2, where the first element is a list of Graphs.
        # l = loadgraph('../test_grafen/colorref_smallexample_2_49.grl', readlist=True)
        #l = loadgraph('../test_grafen/colorref_smallexample_2_49.grl', readlist=True)
        # l = loadgraph('../test_grafen/colorref_smallexample_4_16.grl', readlist=True)
        l = loadgraph('../test_grafen/colorref_smallexample_4_7.grl', readlist=True)
        # l = loadgraph('../test_grafen/colorref_smallexample_6_15.grl', readlist=True)
        # l = loadgraph('../test_grafen/threepaths10240.gr', readlist=True)
        #   `l = loadgraph('../test_grafen/torus24.grl', readlist=True)
        # l = loadgraph('../test_grafen/trees90.grl', readlist=True)
        # Gets the first graph out of the list of graphs
        graph = fasthopcraft(l[0][1])

        end = time.time()
        t = end - start
        writeDOT(graph, "output.dot")
        print("Execution time: " + str(t))


if __name__ == '__main__':
    unittest.main()
