class Solution:
    def minStartValue(self, nums: List[int]) -> int:
        start_value = math.inf
        cum_sum = 0
        
        for num in nums:
            cum_sum += num
            start_value = min(start_value, cum_sum)
        return 1 - start_value if start_value < 1 else 1
