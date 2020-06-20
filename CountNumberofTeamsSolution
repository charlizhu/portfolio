class Solution(object):
    def numTeams(self, r):
        """
        :type rating: List[int]
        :rtype: int
        """
        retVal = 0
        
        for i in range(0,len(r)):
            for j in range(i+1, len(r)):
                for k in range(j+1, len(r)):
                    if (r[i] > r[j] > r[k]) or (r[i] < r[j] < r[k]):
                        retVal += 1
                        
        return retVal
