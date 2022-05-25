class Solution:
    def numberOfArithmeticSlices(self, nums: List[int]) -> int:
        result = 0
        prev = 0
        for idx in range(2, len(nums)):
            if nums[idx-1] - nums[idx-2] == nums[idx] - nums[idx-1]:
                prev += 1
            else:
                prev = 0
            result += prev
        return result