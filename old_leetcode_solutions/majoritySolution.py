class Solution(object):
    def majorityElement(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        """
        Code I wrote to solve the Majority Element question on Leetcode.
        """
        
        nums.sort()
        
        temp = 1
        
        if len(nums) == 1:
            return nums[0]
        
        for x,y in enumerate(nums):
            if x+1 >= len(nums):
                return y
            if nums[x + 1] == y:
                temp = temp + 1
            if nums[x + 1] != y:
                temp = 1
            if temp > (len(nums)//2):
                return y

                
        
