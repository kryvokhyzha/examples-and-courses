class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        result = nums[0]
        for n in nums[1:]:
            result ^= n
        return result
        