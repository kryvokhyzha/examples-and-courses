# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
        

class Solution:
    def oddEvenList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head is None or head.next is None:
            return head
        even_head = head.next
        even_tail = even_head
        even_next = None
        odd_head = head
        odd_tail = odd_head
        odd_next = even_head.next if even_head else None
        
        while odd_next:
            odd_tail.next = odd_next
            odd_tail = odd_next
            if odd_next.next:
                even_next = odd_next.next
                even_tail.next = even_next
                even_tail = even_next
                odd_next = even_next.next
            else:
                even_tail.next = None
                break
        
        odd_tail.next = even_head
        return odd_head
