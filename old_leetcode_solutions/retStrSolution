class Solution(object):
    def compiling(self, myStr):
        retStr = []
        for x in range(0, len(myStr)):
            if myStr[x] != '#':
                print(myStr[x])
                retStr.append(myStr[x])
            else:
                if (len(retStr) != 0):
                    retStr.pop(len(retStr)-1)
                    
        return retStr
        
        
    def backspaceCompare(self, S, T):
        """
        :type S: str
        :type T: str
        :rtype: bool
        """
        
        myInst = Solution()
        
        if (myInst.compiling(S) == myInst.compiling(T)):
            return 1
        return 0
