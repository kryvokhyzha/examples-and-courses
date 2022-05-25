class Solution:
    def validMountainArray(self, arr: List[int]) -> bool:
        if len(arr) < 3:
            return False
        
        mode = '+'
        curr_element = arr[0]
        count = 0
        for element in arr[1:]:
            if element == curr_element:
                return False
            if mode == '+':
                if (element - curr_element) < 0:
                    if count == 0:
                        return False
                    mode = '-'
                count += 1
                curr_element = element
                continue
            else:
                if (element - curr_element) > 0:
                    return False
                curr_element = element
                continue
        return True if mode == '-' else False
