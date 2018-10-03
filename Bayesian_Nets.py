'''
Bayesian Nets
This structure(s) will need to represent the nodes, edges,
and the conditional probability tables (CPTs) for each node.
You will need a way to represent whether each node is a query variable, evidence variable, or unknown.
'''


class Node(object):
    def __init__(self,name,parents,children):
        self.name = name
        self.parents = parents
        self.children = children
        self.CPT = {}


