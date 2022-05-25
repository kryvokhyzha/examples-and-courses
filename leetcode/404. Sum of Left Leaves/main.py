# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
        

class Solution:
    def traverse(self, root, if_left_node=False):
        if root is None:
            return 0
        
        if root.left is None and root.right is None:
            return root.val if if_left_node else 0
        
        l_sum = self.traverse(root.left, True)
        r_sum = self.traverse(root.right, False)
        return l_sum + r_sum
    
    
    def sumOfLeftLeaves(self, root: Optional[TreeNode]) -> int:
        return self.traverse(root)
        