# The isBadVersion API is already defined for you.
# @param version, an integer
# @return a bool
# def isBadVersion(version):

"""
Solution I wrote to the isBadVersion question on Leetcode
"""

class Solution(object):
    def firstBadVersion(self, n):
        """
        :type n: int
        :rtype: int
        """
        
        lowerbound = 0
        upperbound = n
        
        while (lowerbound < upperbound):
            testval = lowerbound + (upperbound - lowerbound)//2
            if (isBadVersion(testval)):
                upperbound = testval
            else:
                lowerbound = testval + 1
                
        return upperbound
            
        
