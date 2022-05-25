class Solution:

    def __init__(self, w: List[int]):
        self.w_sum = sum(w)
        self.n = len(w)
        last_w = 0
        self.w_accum = []
        for i in range(self.n):
            self.w_accum.append(last_w + w[i])
            last_w = self.w_accum[i]
        
    def pickIndex(self) -> int:
        rand = self.w_sum * random.uniform(0, 1)
        return Solution.left_search(self.w_accum, 0, self.n-1, rand)
            
    @staticmethod
    def left_search(arr, low, high, x):
        mid = (high + low) // 2
        
        if low >= high:
            return low
        elif arr[mid] < x:
            return Solution.left_search(arr, mid + 1, high, x)
        else:
            return Solution.left_search(arr, low, mid, x)


# Your Solution object will be instantiated and called as such:
# obj = Solution(w)
# param_1 = obj.pickIndex()