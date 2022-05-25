class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        diffs = {}
        
        for i in range(len(nums)):
            if nums[i] in diffs:
                return [diffs[nums[i]], i]
            
            diffs.update({
                target - nums[i]: i
            })