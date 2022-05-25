class Solution:
    def maxDistance(self, nums1: List[int], nums2: List[int]) -> int:
        result = 0
        n1 = len(nums1)
        n2 = len(nums2)
        i = 0
        j = 0
        
        while i < n1 and j < n2:
            if i <= j and nums1[i] <= nums2[j]:
                result = max(result, j - i)
                j += 1
                continue
            else:
                i += 1
            
            if i > j:
                j = i
        return result

        