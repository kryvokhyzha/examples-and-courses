# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
        

class Solution:
    def trevers(self, root):
        if root is None:
            return 0, []
        
        if root.left is None and root.right is None:
            return root.val, [1]
        
        left_val, left_mults = self.trevers(root.left)
        right_val, right_mults = self.trevers(root.right)
        
        left_mults.extend(right_mults)
        left_mults = [m*10 for m in left_mults]
        result = sum([m*root.val for m in left_mults]) + left_val + right_val
        
        return result, left_mults
        
    def sumNumbers(self, root: Optional[TreeNode]) -> int:
        result, _ = self.trevers(root)
        return result
        