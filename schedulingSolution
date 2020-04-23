class Solution(object):
    def twoCitySchedCost(self, temp):
        """
        :type costs: List[List[int]]
        :rtype: int
        """
        
        """
        Code I wrote to solve the Two City Scheduling problem on Leetcode.
        """
        
        for x in range(0,len(temp)):
            temp[x].insert(0,abs(temp[x][0] - temp[x][1]))
            
        temp.sort()
        
        maxVal = len(temp)//2
        
        count1 = 0
        count2 = 0
        total = 0
        
        for y in range(len(temp)-1,-1,-1):
            if (temp[y][1]>temp[y][2]) & (count2 < maxVal):
                total = total + temp[y][2]
                count2 = count2 + 1
            elif (temp[y][1]<temp[y][2]) & (count1 < maxVal):
                total = total + temp[y][1]
                count1 = count1 + 1
            elif (count1 >= maxVal):
                total = total + temp[y][2]
                count2 = count2 + 1
            else:
                total = total + temp[y][1]
                count1 = count1 + 1
                
        return total
