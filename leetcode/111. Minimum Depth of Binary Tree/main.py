# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
        

class Solution:
    def minDepth(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        
        if root.left is None and root.right is None:
            return 1
        l_depth = self.minDepth(root.left) if root.left is not None else math.inf
        r_depth = self.minDepth(root.right) if root.right is not None else math.inf
        return min(l_depth, r_depth) + 1
        