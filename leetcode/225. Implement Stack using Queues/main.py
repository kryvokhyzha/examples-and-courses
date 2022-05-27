class MyStack:

    def __init__(self):
        self.queue = deque()
        
    def push(self, x: int) -> None:
        t = deque([x])
        t.extend(self.queue)
        self.queue = t
    
    def pop(self) -> int:
        return self.queue.popleft()

    def top(self) -> int:
        return self.queue[0]
        
    def empty(self) -> bool:
        return len(self.queue) == 0
        


# Your MyStack object will be instantiated and called as such:
# obj = MyStack()
# obj.push(x)
# param_2 = obj.pop()
# param_3 = obj.top()
# param_4 = obj.empty()