from graphs.graphIO import loadgraph, writeDOT
from graphs.basicgraphs import graph

"""
Test if the union of two graphs work
"""

l = loadgraph('../../test_grafen/colorref_smallexample_4_7.grl', readlist=True)
union = graph(0)
union.createUnion(l[0][0], l[0][1])
writeDOT(union, "output.dot")
print(union)
