# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
        
        
class Solution:
    def insertionSortList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head.next is None:
            return head
        
        curr_element = head
        last_element = head
        while curr_element is not None and last_element is not None:
            # remove curr_element from List
            last_element.next = curr_element.next
            
            # start search position from head
            insert_place = head
            prev_insert_place = head
            while True:
                if curr_element.val < insert_place.val and insert_place is head:
                    curr_element.next = insert_place
                    head = curr_element
                    break
                elif curr_element.val < insert_place.val:
                    prev_insert_place.next = curr_element
                    curr_element.next = insert_place
                    break
                elif last_element is insert_place:
                    t = insert_place.next
                    insert_place.next = curr_element
                    curr_element.next = t
                    last_element = curr_element
                    break
                    
                prev_insert_place = insert_place
                insert_place = insert_place.next
            curr_element = last_element.next
        return head
        