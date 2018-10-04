

class Node(object):
    def __init__(self,name,parents):
        self.name = name
        self.parents = parents
        self.children = []
        self.CPT = {}

