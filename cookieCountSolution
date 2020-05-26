class Solution(object):

    def findContentChildren(self, g, s):
        """
        :type g: List[int]
        :type s: List[int]
        :rtype: int
        """
        
        #myInst = Solution()
        
        g.sort()
        s.sort()
        

        #temp = -1
        count = 0
        indexKey = 0
        
        for x in range(0,len(s)):
            #if temp == 0:
                #break
            for y in range(indexKey,len(g)):
                if g[y] <= s[x]:
                    indexKey = y + 1
                    count = count + 1
                    break
                else:
                    #temp = 0
                    break

                    
        return count 
