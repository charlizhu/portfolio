"""
This is some Python code I have written to solve the Reverse Integer problem on Leetcode for my own practice.
"""

class Solution(object):
    def reverse(self,x):

    
        if x == 0:
            return 0

        isneg = 0

        if x < 0:
            isneg = 1
            x = x * -1

        y = []
        q = []

        z = [int(k) for k in str(x)]

        for k in range(len(z) - 1, -1, -1):
            y.append(z[k])
 
        print(len(y))

        count = 0

        for k in range(0, len(y)):
            print(k)

            if y[k] != 0:
                print('a' + str(y[k]))
                break
            if y[k] == 0:
                count = count + 1

        for w in range(count, len(y)):
            q.append(y[w])

        print(q)

        result = ''
        for element in q:
            result += str(element)

        result = int(result)    
        
        if isneg == 1:
            result = (result) * -1
            
                
        if (result > 2147483647):
            return 0
        
        if (result < -2147483648):
            return 0  

        return result
