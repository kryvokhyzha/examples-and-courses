class Solution:
    def findNthDigit(self, n: int) -> int:
        # 9 99 999
        #12345678910111213141516171819202122...9899100101102103
        
        start = 1
        depth = 1
        step = 9
        
        while (n > depth * step):
            n -= depth * step
            depth += 1
            step *= 10
            start *= 10
        
        start += (n - 1) // depth
        return str(start)[(n-1) % depth]
