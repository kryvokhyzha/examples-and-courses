class Solution:
    def countAndSay(self, n: int) -> str:
        if n == 1:
            return '1'
        
        seq = self.countAndSay(n-1)
        cur_number = seq[0]
        counter = 1
        result = ''
        
        for number in seq[1:]:
            if number == cur_number:
                counter += 1
                continue
            else:
                result += f'{counter}{cur_number}'
                cur_number = number
                counter = 1
        result += f'{counter}{cur_number}'
        return result
        