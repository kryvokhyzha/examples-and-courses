# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
        

class Solution:
    def traverse(self, root):
        if root is None:
            return 0
        l_depth = self.traverse(root.left)
        r_depth = self.traverse(root.right)
        current_diameter = l_depth + r_depth
        self.diameter = max(current_diameter, self.diameter)
        return max(l_depth, r_depth) + 1
        
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        self.diameter = 0
        self.traverse(root)
        return self.diameter
