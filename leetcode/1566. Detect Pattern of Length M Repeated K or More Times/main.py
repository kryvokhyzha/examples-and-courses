class Solution:
    def containsPattern(self, arr: List[int], m: int, k: int) -> bool:
        for left_idx in range(len(arr) - m):
            right_idx = left_idx + m
            if arr[left_idx:left_idx + m * k] == arr[left_idx:right_idx] * k:
                return True
        return False