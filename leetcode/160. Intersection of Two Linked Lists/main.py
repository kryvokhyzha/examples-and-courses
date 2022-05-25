# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

class Solution:
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> Optional[ListNode]:
        headA_start = headA
        headB_start = headB
        endA = False
        endB = False
        while headA is not headB:
            headA = headA.next
            headB = headB.next
            if headA is None:
                if not endA:
                    headA = headB_start
                    endA = True
                else:
                    return None

            if headB is None:
                if not endB:
                    headB = headA_start
                    endB = True
                else:
                    return None
        return headA
            