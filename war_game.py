#!/usr/bin/python3

import sys

DEBUG=False
ListOfEnemies = []
Groups = []

# War Game
# A war is being fought between two countries, A and B. As a loyal citizen of C, you
# decide to help your country by secretly attending the peace talks between A and B.
# There are n other people at the talks, but you do not know which person belongs to
# which country. You can see people talking to each other, and by observing their
# behavior during occasional one-to-one conversations you can guess if they are
# friends or enemies.
# Your country needs to know whether certain pairs of people are from the same
# country, or whether they are enemies. You can expect to receive such questions
# from your government during the peace talks, and will have to give replies on the
# basis of your observations so far.
#
# Now, more formally, consider a black box with the following operations:



def setFriends(x,y):
    """ Shows that x and y are from the same country """
    global Groups

    g1 = searchGroup(x)
    g2 = searchGroup(y)
    
    # if they are in the same group, do nothing
    if g1 != -1 and (g1 == g2):
        return
    # if none of them are in any group, then create new group
    if g1 == -1 and g2 ==  -1:
        Groups.append([x,y])
        return
    # if x is not part of a group, then add it to the same group as y
    if g1 == -1:
        Groups[g2].append(x)
        return
    # if y is not part of a group, then add it to the same group as x
    if g2 == -1:
        Groups[g1].append(y)
        return

    e1 = searchEnemyOf(g1)
    e2 = searchEnemyOf(g2)
    # cannot be friends because they are enemies in some other way
    if e1 == e2:
        return -1

    mergeGroups(g1, e1, g2, e2, True)


def setEnemies(x,y):
    """ Shows that x and y are from different countries """
    global ListOfEnemies
    global Groups

    g1 = searchGroup(x)
    g2 = searchGroup(y)

    # if they are in the same group (it means they are friends), they cannot be enemies
    if g1 != -1 and (g1 == g2):
        return -1
    # if none of them are in any group, then create two groups
    if g1 == -1 and g2 == -1:
        Groups.append([x])
        Groups.append([y])
        ListOfEnemies.append([len(Groups)-1, len(Groups)-2])
        return

    e1 = searchEnemyOf(g1)
    e2 = searchEnemyOf(g2)
    # if x is not part of a group, then add it to a groups of y's enemy
    if g1 == -1:
        if e2 == -1:
            Groups.append([x])
            ListOfEnemies.append([g2, len(Groups)-1])
        else:
            enemyX, enemyY = ListOfEnemies[e2]
            if g2 == enemyX:
                Groups[enemyY].append(x)
            else:
                Groups[enemyX].append(x)
        return

    # if y is not part of a group, then add it to a groups of x's enemy
    if g2 == -1:
        if e1 == -1:
            Groups.append([y])
            ListOfEnemies.append([g1, len(Groups)-1])
        else:
            enemyA, enemyB = ListOfEnemies[e1]
            if g1 == enemyA:
                Groups[enemyB].append(y)
            else:
                Groups[enemyA].append(y)
        return

    if e1 == -1 and e2 == -1:
        ListOfEnemies.append([g1, g2])
        return

    mergeGroups(g1, e1, g2, e2, False)


def areFriends(x,y):
    """ Returns true if you are sure that x and y are friends """
    g1 = searchGroup(x)
    if y in Groups[g1]:
        return True
    else:
        return False

def areEnemies(x,y):
    """ Returns true if you are sure that x and y are enemies """
    g1 = searchGroup(x)
    g2 = searchGroup(y)
    if g1 == -1 or g2 == -1:
        return False
    elif g1 == g2:
       return False

    e1 = searchEnemyOf(g1)
    e2 = searchEnemyOf(g2)
    if e1 == -1 or e2 == -1 or e1 != e2:
        return False
    else:
        return True

# The first two operations should signal an error if they contradict your former
# knowledge. The two relations “friends” (denoted by ∼) and “enemies” (denoted by
# ∗) have the following properties:

# ∼ is an equivalence relation: i.e.,
# 1. If x ∼ y and y ∼ z, then x ∼z (The friends of my friends are my friends as well.)
# 2. If x ∼ y, then y ∼ x (Friendship is mutual.)
# 3. x ∼ x (Everyone is a friend of himself.)

# ∗ is symmetric and irreflexive:
# 1. If x ∗ y then y ∗ x (Hatred is mutual.)
# 2. Not x ∗ x (Nobody is an enemy of himself.)
# 3. If x ∗ y and y ∗ z then x ∼ z (A common enemy makes two people friends.)
# 4. If x ∼ y and y ∗ z then x ∗ z (An enemy of a friend is an enemy.)

#Operations setFriends(x,y) and setEnemies(x,y) must preserve these properties.


#===============================  HELPER FUNCTIONS =========================================
# Suppose you have a group of people A = [1,2] B = [4,5] and they are enemies
# Suppose you have other two groups of people C = [6,7] D = [8,9] and they are enemies
# In the Group list you will have Group = [[1,2],[6,7],[8,9],[4,5]] 
# and ListOfEnemies = [[0,3], [1,2]], which means that group A might be a friend of C or D.
# If you call setFriend(1,6), it means that group A and group C will become friends and therefore
# group B and D friends automatically.
# [0 - 3]
# [1 - 2]
# You merge group 0 and group 1 into group 1 because they are now friends.
# You merge group 3 and group 2 into group 2 because they are now friends.
# the ListOfEnemies = [[2,3]
# Group = [[],[],[1,2,6,7],[4,5,8,9]
# In case of setEnemy(1,6) group A and D become friends and B and C as well
def mergeGroups(g1, e1, g2, e2, friends):
    global ListOfEnemies
    global Groups

    if e1 == -1:
        g1, g2 = g2, g1
        e1, e2 = e2, e1   
 
    enemyA, enemyOfA = ListOfEnemies[e1]
    enemyX, enemyOfX = ListOfEnemies[e2]
    
    
    if enemyA == g1:
        if friends == False:
            enemyA, enemyOfA = enemyOfA, enemyA

        if e2 == -1:
            Groups[enemyA].extend( Groups[g2] )
            Groups[g2] = []
            return

        if enemyX == g2:
            Groups[enemyA].extend( Groups[enemyX] )
            Groups[enemyOfA].extend( Groups[enemyOfX] )
        else:
            Groups[enemyA].extend( Groups[enemyOfX] )
            Groups[enemyOfA].extend( Groups[enemyX] )
    else:
        if friends == False:
            enemyA, enemyOfA = enemyOfA, enemyA

        if e2 == -1:
            Groups[enemyOfA].extend( Groups[g2] )
            Groups[g2] = []
            return

        if enemyX == g2:
            Groups[enemyOfA].extend( Groups[enemyX] )
            Groups[enemyA].extend( Groups[enemyOfX] )
        else:
            Groups[enemyOfA].extend( Groups[enemyOfX] )
            Groups[enemyA].extend( Groups[enemyX] )
    Groups[enemyX] = []
    Groups[enemyOfX] = []
    ListOfEnemies[e2] = []
    return

# returns then index of the group, otherwise -1 (not found)
def searchGroup(x):
    for i in range(len(Groups)):
        if x in Groups[i]:
            return i
    return -1

# returns then index of the group of enemies, otherwise -1 (not found)
def searchEnemyOf(g):
    for i in range(len(ListOfEnemies)):
        if g in ListOfEnemies[i]:
            return i
    return -1

def validateN(n):
    if n <= 0 or n > 10000:
        raise ValueError("n is between 1 - 10000")

def validatePeople(n, p1, p2):
    if p1 < 0 or p1 >= n:
        raise ValueError("parameter {0} should be less than {1}".format(p1, n))
    if p2 < 0 or p1 >= n:
        raise ValueError("parameter {0} should be less than {1} ".format(p2, n))

def validateOperation(c):
    if c <= 0 or c >= 5:
        raise ValueError("Invalid operation {0}, c is between 1 - 4".format(c))

def parseDataFromFile(filename):
    n = 0
    operations = []
    print("Reading data from file {0}".format(filename))
    with open(filename,'r') as f:
        n = f.readline()
        n = int(n.replace('\n',''))
        validateN(n)
        for line in f:
            line = line.replace('\n','')
            datos = line.split(' ')
            if len(datos) != 3:
                raise ValueError("Faltan argumentos: operacion personaN personaM")
            c = int(datos[0])
            p1 = int(datos[1])
            p2 = int(datos[2])
            if c == 0 and p1 == 0 and p2 == 0:
                break

            validateOperation( c )
            validatePeople(n, p1, p2)
            operations.append([c, p1, p2])

    return operations
 
def doOperation(op, person1, person2):
    if op == 1:
        func_name="setFriends"
        res = setFriends(person1, person2)
    if op == 2:
        func_name="setEnemies"
        res = setEnemies(person1, person2)
    if op == 3:
        func_name="areFriends"
        res = areFriends(person1, person2)
    if op == 4:
        func_name="areEnemies"
        res = areEnemies(person1, person2)

    if DEBUG==True:
        print("=========================================")
        print("{0}({1},{2}) ".format(func_name, person1, person2), end="")
        print("output = {0}".format(res))
        print("Groups")
        print(Groups)
        print("Enemies")
        print(ListOfEnemies)
    return res

#===============================  INPUT  ================================================
#
#The first line contains a single integer, n, the number of people. Each subsequent
#line contains a triple of integers, c x y, where c is the code of the operation,		
#
# c=1, setFriends
# c=2, setEnemies
# c=3, areFriends
# c=4, areEnemies
#
# and x and y are its parameters, integers in the range [0, n) identifying two different
# people. The last line contains 0 0 0.
# All integers in the input file are separated by at least one space or line break. There
# are at most 10,000 people, but the number of operations is unconstrained.

# Sample Input
# 10
# 1 0 1
# 1 1 2
# 2 0 5
# 3 0 2
# 3 8 9
# 4 1 5
# 4 1 2
# 4 8 9
# 1 8 9
# 1 5 2
# 3 5 2
# 0 0 0

def main():
    global DEBUG

    if len(sys.argv) == 2:
        testFile = sys.argv[1]
    elif len(sys.argv) == 3:
        testFile = sys.argv[1]
        if sys.argv[2] == '-D':
            DEBUG=True
    else:
        testFile = "wargame_input01.txt"

    output = []
    operations = parseDataFromFile(testFile)

    if DEBUG==True:
        for op in operations:
            print(op)

    for op in operations:
        res = doOperation(op[0], op[1], op[2])
        if res == True:
            res = 1
        if res == False:
            res = 0
        if res != None:
            output.append(res)
    print("=========================================")
    print("output: {0}".format(output))


#=====================================  MAIN  ==========================================
if __name__ == "__main__":
    main()
#===============================  OUTPUT ================================================

# For every areFriends and areEnemies operation write “0” (meaning no) or “1”
# (meaning yes) to the output. For every setFriends or setEnemies operation which
# conflicts with previous knowledge, output a “-1” to the output; such an operation
# should produce no other effect and execution should continue. A successful
# setFriends or setEnemies gives no output.
# All integers in the output file must be separated by one line break.

# Sample Output
# 1
# 0
# 1
# 0
# 0
# -1
# 0
