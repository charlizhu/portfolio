"""
This is some Python code which I have written to solve the Two Sum problem on Leetcode for my own practice.
"""

class Solution(object):
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        allitems = len(nums)

        firstnum = -100
        secondnum = -100
        test = 0

        for x in range(0, allitems-1):
            want = target - nums[x]
            newlist = nums[(x+1):allitems]
            if want in newlist:
                firstnum = x
                secondnum = newlist.index(want)+(x+1)
            else:
                continue
                    
        return (firstnum,secondnum)
