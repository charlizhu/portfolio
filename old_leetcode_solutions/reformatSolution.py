class Solution(object):
    def reformat(self, s):
        """
        :type s: str
        :rtype: str
        """
        
        """
        Code I wrote to solve the Reformat String problem from Leetcode.
        """
        
        numStr = []
        charStr = []
        retStr = []
        
        for x in s:
            currently = ord(x)
            
            if (currently >= 48) & (currently <= 57):
                numStr.append(x)
            else:
                charStr.append(x)
                
        if (abs(len(numStr)-len(charStr))) == 1:
            counter = 0
            if len(numStr) > len(charStr):
                for x in range(0,len(charStr)):
                    retStr.append(numStr[x])
                    retStr.append(charStr[x])
                retStr.append(numStr[len(numStr)-1])
            else:
                for x in range(0,len(numStr)):
                    retStr.append(charStr[x])
                    retStr.append(numStr[x])
                retStr.append(charStr[len(charStr)-1])
        elif (len(numStr)-len(charStr)) == 0:
            for x in range(0,len(charStr)):
                retStr.append(numStr[x])
                retStr.append(charStr[x])
        else:
            return ""
                
        return retStr
