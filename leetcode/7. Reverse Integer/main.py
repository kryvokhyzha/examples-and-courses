class Solution:
    def reverse(self, x: int) -> int:
        max_int = 2 ** 31 - 1
        min_int = -2 ** 31
        
        result = str(x)[::-1]
        if result[-1] == '-':
            result = '-' + result[:-1]
        result = int(result)
        
        if result > min_int and result < max_int:
            return result
        else:
            return 0
        