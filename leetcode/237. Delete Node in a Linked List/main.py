# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

class Solution:
    def deleteNode(self, node):
        """
        :type node: ListNode
        :rtype: void Do not return anything, modify node in-place instead.
        """
        
        prev_node = None
        while node and node.next:
            prev_node = node
            node.val = node.next.val
            node = node.next
        prev_node.next = None
        