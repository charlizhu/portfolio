class Solution(object):
    def addDigits(self, num):
        """
        :type num: int
        :rtype: int
        """
        
        """
        Code I wrote for the Add Digits question on Leetcode.
        """
        
        if num < 10:
            return num

        while num >= 10:
            x = list(str(num))
            totalsum = 0
            
            for q in range(0,len(x)):
                totalsum = totalsum + int(x[q])
                
            if totalsum < 10:
                return totalsum
            else:
                myInst = Solution()
                return myInst.addDigits(totalsum)
            
