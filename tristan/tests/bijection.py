from graphs.graphIO import loadgraph, writeDOT
from tristan.isomorphisms import bijection, colordict
from tristan.refinement import hopcroft

"""
Test if bijection works.
"""
l = loadgraph('../../test_grafen/colorref_smallexample_2_49.grl', readlist=True)
hopcroft(l[0][1])
hopcroft(l[0][2])
print(bijection(colordict(l[0][1]),colordict(l[0][2])))