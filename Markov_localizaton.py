#Exercise 0: Uniform distribution
#This creates a function that returns a list of n elements representing a
#uniform distribution

n = 5
def init_p(n):
    places = []
    for i in range(n):
        places.append(1/n)
    return places

p = init_p(n)

print('\nThe uniform distribution:')
print(p)

#Exercise 1: Create sense function
#This creates a function that returns the modified distribution after sensing Z

world = ['green', 'red', 'red', 'green', 'green']
pHit = 0.6
pMiss = 0.2

def sense(p, Z):
    pCopy = []
    if Z == 'red':
        for i in range(len(world)):
            if world[i] == 'red':
                pCopy.append(p[i] * pHit)
            else:
                pCopy.append(p[i] * pMiss)
    if Z == 'green':
        for i in range(len(world)):
            if world[i] == 'green':
                pCopy.append(p[i] * pHit)
            else:
                pCopy.append(p[i] * pMiss)
                
    summary = sum(pCopy)
    for i in range(len(pCopy)):
        pCopy[i] = pCopy[i] / summary
    return pCopy

print('\nThe sense function called with red parameter:')
print(sense(p, 'red'))
print('\nThe sense function called with green parameter:')
print(sense(p, 'green'))

#Exercise 2: Exact motion
#This creates a function that returns the modified distribution after the robot
#has moved U cells to the right. The list will be shifted to the right by U
#units cyclicly.

def move_exact(p, U):
    shift = U % len(p)
    p_new = []
    for i in range(len(p)):
        if (i + shift) >= (len(p)):
            p_new.insert(i + shift - len(p), p[i])
        else:
            p_new.insert(i + shift, p[i])
    return p_new
            
p = sense(p, 'red')
p = move_exact(p, 2)

print('\nThe p list after the move_exact function:')
print(p)

#Exercise 3: Inexact motion
#This creates a function that returns the modified distribution after the robot
#has moved approximately U cells to the right

pExact = 0.8 #probability of moving exactly U cells
pOvershoot = 0.1 #probability of moving U+1 cells
pUndershoot = 0.1 #probability of moving U-1 cells

def move_inexact(p, U):
    q = []
    for i in range(len(p)):
        s = pExact * p[(i-U) % len(p)]
        s = s + pOvershoot * p[(i-U-1) % len(p)]
        s = s + pUndershoot * p[(i-U+1) % len(p)]
        q.append(s)
    return q
    
'''
def move_inexact(p, U):
    shift = U % len(p)
    shiftOver = U+1 % len(p)
    shiftUnder = U-1 % len(p)
    
    p_new = [0 for i in range(n)]
    p_matrix = [[0]*n for i in range(n)]
    
    for i in range(len(p)): 
        if (i + shift) >= (len(p)):
            p_matrix[i][i + shift - len(p)] = p[i] * pExact
        else:
            p_matrix[i][i + shift] = p[i] * pExact

        if (i + shiftOver) >= (len(p)):
            p_matrix[i][i + shiftOver - len(p)] = p[i] * pOvershoot
        else:
            p_matrix[i][i + shiftOver] = p[i] * pOvershoot
            
        if (i + shiftUnder) >= (len(p)):
            p_matrix[i][i + shiftUnder - len(p)] = p[i] * pUndershoot
        else:
            p_matrix[i][i + shiftUnder] = p[i] * pUndershoot
    
    for i in range(len(p_matrix)):
        for j in range(len(p_matrix)):
            p_new[j] += p_matrix[i][j]
    
    return p_new
'''
    
p = init_p(n) #reinitializes the p to basic uniform distribution
p = sense(p, 'red')
p = move_inexact(p, 1)

print('\nThe p list after the move_inexact function:')
print(p)

#Exercise 4: Multiple sensing and motions
#Given the lists of senses and motions, this function calculates the
#probability distribution that shows where the robot might be after two inexact
#movements. Creates a cycle in which the robot senses first then moves
#according to the lists.

measurements = ['red', 'green'] #the robot first sees 'red' then 'green'
motions = [1, 1] #the robot moves twice to the right
p = init_p(n) #reinitializes the p to basic uniform distribution

#The cycle that moves the robot according to the lists
for i in range(len(measurements)):
    p = sense(p, measurements[i])
    p = move_inexact(p, motions[i])
    message = '\nThe p list after sensing ' + measurements[i] + ' and moving ' + str(motions[i]) + ' to the right:'
    print(message)
    print(p)






















