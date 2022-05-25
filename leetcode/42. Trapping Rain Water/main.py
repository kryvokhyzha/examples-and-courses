class Solution:
    def trap(self, height: List[int]) -> int:
        result = 0
        max_poss_height = 0
        left, right = 0, len(height) - 1
        
        while left < right:
            if height[left] < height[right]:
                max_poss_height = max(height[left], max_poss_height)
                result += max_poss_height - height[left]
                left += 1
            else:
                max_poss_height = max(height[right], max_poss_height)
                result += max_poss_height - height[right]
                right -= 1
        return result
        