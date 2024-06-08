""" bike.py
 David Liben-Nowell
 Anna Rafferty
 Sneha Narayan
 Tom Finzell
 This program analyzes bike share data 
 Code was finished by Bonney Seth.
"""

bikeShareFileName = "2015MayBikeShareData (2).csv"

try:
    file = open(bikeShareFileName)
except IOError:
    print("ERROR!", bikeShareFileName, "doesn't appear in the current directory.")
    exit(1)

# make empty list containers for our list of times and sorted lists
firstList = []
sortedByDeparture = []
sortedByArrival = []

def mergeSort(lst):
    n = len(lst)
    
    if n <= 0:
        raise ValueError
    
    if n == 1:
        return lst[0]
    
    if n % 2 == 1:
        if lst[-1] < lst[-2]:
            lst[-2] = lst[-1]
        return mergeSort(lst[:n-1])
    
    # this only happens if n is even
    half = int(n / 2)
    pre = lst[:half + 1]
    post = lst[half + 1:]
    return merge(pre, post)
    
def merge(pre, post):
    lp = 0
    rp = 0
    merged = []
    while True:
        if lp == len(pre):
            while rp < len(post):
                merged.append(post[rp])
            return merged
        elif rp == len(post):
            while lp < len(pre):
                merged.append(pre[lp])
            return merged
        else:
            if pre[lp] < post[rp]:
                merged.append(pre[lp])
                lp += 1
            else:
                merged.append(post[rp])
                rp += 1
            

# these are used to find the total number of bikes that are coming and leaving the 19th St & Constitution Ave NW
leavingThe19thSt = 0
comingIntoThe19th = 0

# because it is a csv data we have to split it with respect to comma. 
for line in file:
    ab = line.split(",")
    '''In this case we are apppending all the elements with index[0] from ab into the firstList container'''
    firstList.append(ab[0])
    if ab[2] == "19th St & Constitution Ave NW":
        leavingThe19thSt += 1
    if ab[4] == "19th St & Constitution Ave NW":
        comingIntoThe19th += 1

Container1 = 0
for i in firstList:
    Container1 += int(str(i))

actualCalculation = Container1 / len(ab)
UnitConversion = (actualCalculation / 60) / 1000

# Here I am just converting the calculation to two decimal place
unitConversion = '{0:0.2f}'.format(UnitConversion)

# These print statements produce the output 
print('The average time of bike ride is:', unitConversion,'minutes' )
print(leavingThe19thSt, 'bikes left from 19th St & Constitution Ave NW')
print(comingIntoThe19th, 'bikes came into 19th St & Constitution Ave NW')

# Files should always be closed when you are done with them.
file.close()
