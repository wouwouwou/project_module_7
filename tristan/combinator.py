from tristan.isomorphisms import isomorphisms


def combinator(graphlist, count=False):
    """
    Compares a list of graphs to each other in an efficient way.
    :param graphlist:
    :param count:
    :return:
    """

    # Queuelist
    w = []
    # Resultlist
    res = []

    # Building w[0]-list
    wzero = [[], -1]
    for g in range(len(graphlist[0])):
        wzero[0].append(g)
    w.append(wzero)

    i = 0

    # Add w[0][0][0] as first result
    res.append([[], -1])
    res[i][0].append(w[i][0][0])

    # Loop w[i]
    while i < len(w):
        # Pick g1 the first item of w[i]
        g1 = w[i][0][0]

        # Loop w with w[i][0] != w[j][0]
        for j, g2 in enumerate(w[i][0], 1):
            if g2 != g1:

                # Check if counting of automorphisms is required and not already known
                if count and w[i][1] == -1:
                    result = isomorphisms(graphlist[0][g1], graphlist[0][g2], count)
                else:
                    result = isomorphisms(graphlist[0][g1], graphlist[0][g2], False)

                # If automorphisms/isomorphisms are found
                if result > 0:
                    # Add result if #automorphisms wasn't found
                    if w[i][1] == -1:
                        w[i][1] = result
                        res[i][1] = result

                    # Add graph to these isomorphism class
                    res[i][0].append(g2)
                # Graphs are not isomorphic
                else:
                    # Check if new entry in w must be made.
                    if len(w) <= i + 1:
                        w.append([[], -1])
                        res.append([[g2], -1])
                    w[i+1][0].append(g2)
        i += 1

    # Print the result
    for i in res:
        print(i)