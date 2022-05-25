# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        if head is None:
            return False
        
        pointer1 = head.next
        pointer2 = head
        
        for _ in range(2):
            pointer2 = pointer2.next
            if pointer2 is None:
                return False
        
        while pointer1 is not pointer2:
            for _ in range(2):
                pointer2 = pointer2.next
                if pointer2 is None:
                    return False
            pointer1 = pointer1.next
        return True