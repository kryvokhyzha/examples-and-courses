class Solution:
    def isValid(self, s: str) -> bool:
        open_set = '({['
        pairs = {'(': ')', '[': ']', '{': '}'}
        open_queue = deque()
        
        for some_char in s:
            if some_char in open_set:
                open_queue.append(some_char)
            else:
                if len(open_queue) == 0:
                    return False
                open_char = open_queue.pop()
                if pairs[open_char] != some_char:
                    return False
        return len(open_queue) == 0
                    
        