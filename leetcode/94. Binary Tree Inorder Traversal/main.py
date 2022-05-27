# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
        
        
class Solution:
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        if not root:
            return []
        
        stack, result = [], [] 
        while True:
            while root:
                stack.append(root)
                root = root.left
            if not stack:
                return result
            prev_node = stack.pop()
            result.append(prev_node.val)
            root = prev_node.right
        
        
# class Solution:
#     def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
#         if not root:
#             return []
            
#         return self.inorderTraversal(root.left) + [root.val] + self.inorderTraversal(root.right)
