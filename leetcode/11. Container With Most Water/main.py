class Solution:
    def maxArea(self, height: List[int]) -> int:
        to_index = 0
        from_index = len(height) - 1
        area = []
        
        while to_index < from_index:
            area.append((from_index - to_index) * min([height[to_index], height[from_index]]))
            
            if height[to_index] < height[from_index]:
                to_index += 1
            else:
                from_index -= 1
                
        return max(area)