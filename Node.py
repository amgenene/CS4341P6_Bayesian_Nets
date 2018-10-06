

class Node(object):
    def __init__(self,name):
        self.name = name
        self.parents = []
        self.children = []
        self.CPT = []
        self.query_list = []
        self.status = None


