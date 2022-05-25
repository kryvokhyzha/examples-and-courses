class Solution:
    def decrypt(self, code: List[int], k: int) -> List[int]:
        if k == 0:
            return [0] * len(code)
        
        result = []
        n = len(code)
        left_idx, right_idx = (1, k+1) if k >= 0 else (k, 0)
        partial_sum = sum(code[1: k+1] if k > 0 else code[k:])
        for i in range(n):
            result.append(partial_sum)
            partial_sum += code[(right_idx + i) % n]
            partial_sum -= code[(left_idx + i) % n]
            
        return result 
