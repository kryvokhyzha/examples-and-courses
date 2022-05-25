class Solution:
    def isUgly(self, n: int) -> bool:
        
        if n <= 0:
            return False
        
        while (n % 30) == 0:
            n /= 30
        
        while (n % 15) == 0:
            n /= 15
            
        while (n % 10) == 0:
            n /= 10
        
        while (n % 6) == 0:
            n /= 6

        while (n % 5) == 0:
            n /= 5
            
        while (n % 3) == 0:
            n /= 3
        
        while (n % 2) == 0:
            n /= 2
            
        return n == 1
