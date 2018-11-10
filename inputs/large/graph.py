import networkx as nx
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from networkx.algorithms import community


def draw_graph():


    G = nx.random_regular_graph(2, 500)


    # draw graph
    pos = nx.shell_layout(G)
    nx.draw(G, pos)

    # show graph
    # plt.show()
    print(G.edges())
    # print()
    # print(list(c))
    # nx.write_gml(G, "large.gml")
    nx.write_gml(G, "large.gml", nx.readwrite.gml.literal_stringizer)



# draw example
# graph = [(20, 21),(21, 22),(22, 23), (23, 24),(24, 25), (25, 20)]
draw_graph()
