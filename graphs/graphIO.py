"""
Includes functions for reading and writing graphs, in a very simple readable format.
 loadgraph:		reads from files
 inputgraph:	reads from terminal input / stdin
 savegraph:		writes to files
 printgraph:	writes to terminal / stdout
 writeDOT:		writes in .dot format; can be used for visualization.
 
The other functions are internal, to implement the above functions.  

The graph objects returned by loadgraph and inputgraph are by default constructed using the <graph> class in the module
basicgraphs.py, but by using an optional argument you can use your own graph class (provided that it supports the same
methods/interface).

This module also supports edge weighted graphs: edges should/will have an (integer) attribute <weight>. 
"""
# Version: 30-01-2015, Paul Bonsma
# updated 30-01-2015: writeDOT also writes color information for edges.
# updated 2-2-2015: writeDOT can also write directed graphs.
# updated 5-2-2015: no black fill color used, when more than numcolors**2 vertices.

from graphs import basicgraphs

defaultcolorscheme = "paired12"
numcolors = 12


# defaultcolorscheme="piyg11"
# numcolors=11

# defaultcolorscheme="spectral11"
# numcolors=11

def readgraph(graphclass, readline):
    """
    For internal use.
    :param readline:
    :param graphclass:
    """
    options = []
    while True:
        try:
            s = readline()
            n = int(s)
            g = graphclass(n)
            break
        except ValueError:
            if len(s) > 0 and s[-1] == '\n':
                options.append(s[:-1])
            else:
                options.append(s)
    s = readline()
    edgelist = []
    try:
        while True:
            comma = s.find(',')
            if ':' in s:
                colon = s.find(':')
                edgelist.append((int(s[:comma]), int(s[comma + 1:colon]), int(s[colon + 1:])))
            else:
                edgelist.append((int(s[:comma]), int(s[comma + 1:]), None))
            s = readline()
    except Exception:
        pass
    for edge in edgelist:
        # print("Adding edge (%d,%d)"%(edge[0],edge[1]))
        e = g.addedge(g[edge[0]], g[edge[1]])
        if edge[2] is not None:
            e.weight = edge[2]
    if s != '' and s[0] == '-':
        return g, options, True
    else:
        return g, options, False


def readgraphlist(graphclass, readline):
    """
    For internal use.
    :param readline:
    :param graphclass:
    """
    options = []
    l = []
    contin = True
    while contin:
        g, newoptions, contin = readgraph(graphclass, readline)
        options += newoptions
        l.append(g)
    return l, options


def loadgraph(filename, graphclass=basicgraphs.graph, readlist=False):
    """
    Reads the file <filename>, and returns the corresponding graph object.
    Optional second argument: you may use your own <graph> class, instead of
    the one from basicgraphs.py (default).
    Optional third argument: set to True if you want to read a list of graphs, and
    options included in the file.
    In that case, the output is a 2-tuple, where the first item is a list of graphs,
    and the second is a list of options (strings).
    :param readlist: boolean to determine if it is one graph or a list of graphs
    :param graphclass: graph class of basicgraphs.py
    :param filename: File of the graph(list) to be loaded
    """
    readfile = open(filename, 'rt')

    def readln():
        s = readfile.readline()
        while len(s) > 0 and s[0] == '#':
            s = readfile.readline()
        return s

    if readlist:
        gl, options = readgraphlist(graphclass, readln)
        readfile.close()
        return gl, options
    else:
        g, options, tmp = readgraph(graphclass, readln)
        readfile.close()
        return g  # ,options


def inputgraph(graphclass=basicgraphs.graph, readlist=False):
    """
    Reads a graph from stdin, and returns the corresponding graph object.
    Optional first argument: you may use your own <graph> class, instead of
     the one from basicgraphs.py.
    Optional second argument: set to True if you want to read a list of graphs, and
    options included in the file.
    In that case, the output is a 2-tuple, where the first item is a list of graphs,
    and the second is a list of options (strings).
    :param graphclass:
    :param readlist:
    """
    def readln():
        s = input()
        while len(s) > 0 and s[0] == '#':
            s = input()
        return s

    if readlist:
        gl, options = readgraphlist(graphclass, readln)
        return gl, options
    else:
        g, options, tmp = readgraph(graphclass, readln)
        return g  # ,options


def writegraphlist(gl, writeline, options=None):
    """
    For internal use.
    :param options:
    :param writeline:
    :param gl:
    """
    # we may only write options that cannot be seen as an integer:
    if options is None:
        options = []
    for S in options:
        try:
            x = int(S)
        except ValueError:
            writeline(str(S))
    for i in range(len(gl)):
        g = gl[i]
        n = len(g.V())
        writeline('# Number of vertices:')
        writeline(str(n))
        # Give the vertices (temporary) labels from 0 to n-1:
        nl = {}
        for j in range(n):
            nl[g[j]] = j
        writeline('# Edge list:')
        for e in g.E():
            if hasattr(e, 'weight'):
                writeline(str(nl[e.tail()]) + ',' + str(nl[e.head()]) + ':' + str(e.weight))
            else:
                writeline(str(nl[e.tail()]) + ',' + str(nl[e.head()]))
        if i + 1 < len(gl):
            writeline('--- Next graph:')


def savegraph(gl, filename, options=None):
    """
    Saves the given graph <GL> in the given <filename>.
    Optional last argument: a list of options that will be included in the
    file header.
    Alternatively, <GL> may be a list of graphs, which are then all written to the
    file.
    :param options:
    :param filename:
    :param gl:
    """
    if options is None:
        options = []

    writefile = open(filename, 'wt')

    def writeln(s):
        writefile.write(s + '\n')

    if type(gl) is list:
        writegraphlist(gl, writeln, options)
    else:
        writegraphlist([gl], writeln, options)
    writefile.close()


def printgraph(gl, options=None):
    """
    Writes the given graph <GL> to Stdout.
    Optional last argument: as list of options that will be included in the
    header.
    Alternatively, <GL> may be a list of graphs, which are then all written.
    :param options:
    :param gl:
    """
    if options is None:
        options = []

    def writeln(s):
        print(s)

    if type(gl) is list:
        writegraphlist(gl, writeln, options)
    else:
        writegraphlist([gl], writeln, options)


def writeDOT(g, filename, directed=False):
    """
    Writes the given graph <G> in .dot format to <filename>.
    If vertices contain attributes <label>, <colortext> or <colornum>, these are also
    included in the file.
    (<Colortext> should be something like "Blue"/"Magenta"/"Khaki"/"Peachpuff"/"Olivedrab",...
    and a <colornum> should be an integer.)
    If edges contain an attribute <weight> (integer), these are also included in the
    file.
    Optional argument: <directed>. If True, then the edges are written as directed edges.
    Google GraphViz for more information on the .dot format.
    :param directed:
    :param g:
    :param filename:
    """
    writefile = open(filename, 'wt')
    if directed:
        writefile.write('digraph G {\n')
    else:
        writefile.write('graph G {\n')
    name = {}
    nextname = 0
    for v in g.V():
        name[v] = nextname
        nextname += 1
        options = 'penwidth=3,'
        if hasattr(v, 'label'):
            options += 'label="' + str(v.label) + '",'
        if hasattr(v, 'colortext'):
            options += 'color="' + v.colortext + '",'
        elif hasattr(v, 'colornum'):
            options += 'color=' + str(v.colornum % numcolors + 1) + ', colorscheme=' + defaultcolorscheme + ','
            if v.colornum >= numcolors:
                options += 'style=filled,fillcolor=' + str((v.colornum // numcolors) % numcolors + 1) + ','
        if len(options) > 0:
            writefile.write('    ' + str(name[v]) + ' [' + options[:-1] + ']\n')
        else:
            writefile.write('    ' + str(name[v]) + '\n')
    writefile.write('\n')

    for e in g.E():
        options = 'penwidth=2,'
        if hasattr(e, 'weight'):
            options += 'label="' + str(e.weight) + '",'
        if hasattr(e, 'colortext'):
            options += 'color="' + e.colortext + '",'
        elif hasattr(e, 'colornum'):
            options += 'color=' + str(e.colornum % numcolors + 1) + ', colorscheme=' + defaultcolorscheme + ','
        if len(options) > 0:
            options = ' [' + options[:-1] + ']'
        if directed:
            writefile.write('    ' + str(name[e.tail()]) + ' -> ' + str(name[e.head()]) + options + '\n')
        else:
            writefile.write('    ' + str(name[e.tail()]) + '--' + str(name[e.head()]) + options + '\n')

    writefile.write('}')
    writefile.close()
