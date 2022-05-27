class MyQueue:

    def __init__(self):
        self.stack = deque()

    def push(self, x: int) -> None:
        self.stack.append(x)
        
    def pop(self) -> int:
        t = deque()
        while self.stack:
            element = self.stack.pop()
            t.append(element)
        element = t.pop()
        while t:
            self.stack.append(t.pop())
        return element
        
    def peek(self) -> int:
        t = deque()
        while self.stack:
            element = self.stack.pop()
            t.append(element)
        while t:
            self.stack.append(t.pop())
        return element

    def empty(self) -> bool:
        return len(self.stack) == 0


# Your MyQueue object will be instantiated and called as such:
# obj = MyQueue()
# obj.push(x)
# param_2 = obj.pop()
# param_3 = obj.peek()
# param_4 = obj.empty()