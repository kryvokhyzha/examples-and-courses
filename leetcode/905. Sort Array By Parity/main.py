class Solution:
    def sortArrayByParity(self, nums: List[int]) -> List[int]:
        result = deque()
        for num in nums:
            if num % 2 == 0:
                result.appendleft(num)
            else:
                result.append(num)
        return list(result)
        