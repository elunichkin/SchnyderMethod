class TreeNode:
    def __init__(self, parent=None, children=None, label=None):
        self.parent = parent
        self.children = children if children is not None else []
        self.label = label
        self.depth = parent.depth + 1 if parent is not None else 1

    def add_child(self, child):
        if child not in self.children:
            self.children.append(child)
            child.parent = self

    def get_subtree_size(self):
        size = 1
        for child in self.children:
            size += child.get_subtree_size()
        return size