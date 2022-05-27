class Solution:
    def sortColors(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        counts = Counter(nums)
        result = [0]*counts[0] + [1]*counts[1] + [2]*counts[2]
        
        for idx, num in enumerate(result):
            nums[idx] = num 
        