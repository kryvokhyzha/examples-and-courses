# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
        

class Solution:
    def isPalindrome(self, head: Optional[ListNode]) -> bool:
        next_element = head.next
        acc_list = [head.val]
        n = 1
        while next_element is not None:
            acc_list.append(next_element.val)
            next_element = next_element.next
            n += 1
        
        for i in range(n // 2):
            if acc_list[i] != acc_list[n - i - 1]:
                return False
        return True
