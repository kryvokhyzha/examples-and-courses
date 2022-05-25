class Solution:
    def findDuplicate(self, nums: List[int]) -> int:
        nums_set = set()
        
        for num in nums:
            if num in nums_set:
                return num
            else:
                nums_set.add(num)
        