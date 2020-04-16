"""
This is some Python code I have written to solve the Palindrome Number problem on Leetcode.
"""

class Solution(object):
    def isPalindrome(self, x):
        """
        :type x: int
        :rtype: bool
        """
        
        if (x < 0):
            return 0
        
        y = [int(k) for k in str(x)]
        
        maxVal = len(y)//2
        
        for q in range(0,maxVal + 1):
            if (y[q] != y[len(y) - 1 - q]):
                return 0
            
        return 1
        
