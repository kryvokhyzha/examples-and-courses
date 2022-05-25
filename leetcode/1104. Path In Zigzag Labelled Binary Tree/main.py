class Solution:
    def pathInZigZagTree(self, label: int) -> List[int]:
        result = []
        row_idx = math.floor(math.log(label, 2))
        parent_node_idx = label
        
        while row_idx >= 0:
            result.insert(0, parent_node_idx)
            t = math.floor(parent_node_idx / 2)
            row_idx -= 1
            
            # (max number of current level + min number of current level) - current number
            parent_node_idx = (2 ** row_idx) + (2 ** (row_idx + 1)) - t - 1
        
        return result
