import re
# a = 6
a = 6 + 1

if 5 !=2 and 5==6:
    print(2)

if(a < 5):
    print("a < 5")
elif (a > 5):
    print("a > 5")
else:
    print("a = 5")   


def checkA(a):
    """some func"""

    for i in range(2):
        if(a < 5):
            print("a < 5")
        elif (a > 5):
            print("a > 5")
        else:
            print("a = 5") 

checkA(a)