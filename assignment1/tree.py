class Tree(object):
    def __init__(self, puzzle):
        self.root = None
        self.puzzle = puzzle
        self.inner_matrix = []
        for r in range(0, puzzle.n):
            l = []
            for c in range(0, puzzle.n):
                l.append(0)
            self.inner_matrix.append(list(l))

    def insert(self, x, y, step):
        if self.root is None:
            self.root = Node(x, y, step)
            return
        ptr = self.root
        while step > ptr.step and ptr.firstChild is not None:
            ptr = ptr.firstChild
        if step != ptr.step:
            ptr.firstChild = Node(x, y, step)
        else:
            while ptr.nextSibling is not None:
                ptr = ptr.nextSibling
            ptr.nextSibling = Node(x, y, step)

    def __str__(self):
        return self.print_tree(self.root)

    def print_tree(self, ptr):
        if ptr is not None and ptr.firstChild is None:
            return '' + str(ptr) + self.print_tree(ptr.nextSibling)
        elif ptr is not None:
            return '' + str(ptr) + self.print_tree(ptr.nextSibling) + '\n' + self.print_tree(ptr.firstChild)
        else:
            return ''


class Node(object):
    def __init__(self, x, y, step):
        self.data = (x,y)
        self.step = step
        self.firstChild = None
        self.nextSibling = None

    def __str__(self):
        return '[ ' + str(self.data) + ': ' + str(self.step) + ' ] -> '