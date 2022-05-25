class Solution:
    def findLengthOfLCIS(self, nums: List[int]) -> int:
        length = 1
        max_length = -1
        for idx in range(len(nums) - 1):
            if nums[idx] < nums[idx+1]:
                length += 1
            else:
                max_length = max(max_length, length)
                length = 1
        return max(max_length, length)