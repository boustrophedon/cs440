class Queue(object):
    def __init__(self):
        self.front = None
        self.back = None
        self.count = 0

    def enqueue(self, n):
        if self.front is None:
            self.front = Node(n)
            self.back = self.front
        else:
            self.back.next = Node(n)
            self.back = self.back.next
        self.count += 1

    def dequeue(self):
        result = self.front
        self.front = self.front.next
        self.count -= 1
        return result

    def isempty(self):
        if self.count == 0:
            return True
        return False

class Node(object):
    def __init__(self, n):
        self.data = n
        self.next = None
