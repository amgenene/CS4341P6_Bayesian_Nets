class Node(object):
    def __init__(self,name):
        self.name = name
        self.parents = []
        self.children = []
        self.CPT = []
        self.status = None
        self.accepted = None
        self.temporal_status = None