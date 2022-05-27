class Solution:
    def removeDuplicates(self, s: str, k: int) -> str:
        chars_deque = deque()
        
        for char in s:
            if not chars_deque:
                chars_deque.append([char, 1])
                continue
                
            if char == chars_deque[-1][0]:
                chars_deque[-1][1] += 1
                if k == chars_deque[-1][1]:
                    chars_deque.pop()
            else:
                chars_deque.append([char, 1])
        
        result = ''
        for pair in chars_deque:
            result += pair[0] * pair[1]
        return result
        