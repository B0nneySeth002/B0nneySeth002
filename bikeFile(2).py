""" bike.py
 David Liben-Nowell
 Anna Rafferty
 Sneha Narayan
 Tom Finzell
 This program analyzes bike share data 
 Code was finished by Bonney Seth.
"""

""" Reads a file of bike share data and calculates statistics
    about the data.
"""

# This is the name of the small data file. A small data file is useful
# for testing and making sure everything works. After you complete the
# first parts of the assignment, change the line below to use the
# bigger data file - its name is "2015MayBikeShareData.csv"
bikeShareFileName = "2015MayBikeShareData (2).csv"

# The block of code below attempts to open the file with the bike share
# data. If an IOError (input/output error) occurs, it prints an error
# message and exits the program, since the rest of the program needs
# to be able to read the file. If you get an error, check that you
# haven't changed the name of the file and make sure if appears in the
# same directory as bike.py.
try:
    file = open(bikeShareFileName)
except IOError:
    print("ERROR!", bikeShareFileName, "doesn't appear in the current directory.")
    exit(1)

print(file.readline())

# make an empty list container and name it firstList
firstList =[]

# these are used to find the total number of bikes that are coming and leaving the 19th St & Constitution Ave NW
leavingThe19thSt = 0
comingIntoThe19th = 0


''' ab is a variable to access the splitting of the comma separated values in the line of each document 
also we create the for loop to iterate through each line in the document to obtain the time for each ride

We use both if and if not fif else because we want to obtain both the number of bikes 
leaving and coming to the 19th St & Constitution Ave NW
'''
# because it is a csv data we have to split it with respect to comma. 


for line in file:
    ab = line.split(",")
    '''In this case we are apppending all the elements with index[0] from ab into the firstList container'''
    firstList.append(ab[0])
    if ab[2] == "19th St & Constitution Ave NW":
        leavingThe19thSt += 1
    if ab[4] == "19th St & Constitution Ave NW":
        comingIntoThe19th += 1
            

'''now in this block of code we create a for loop that can access each of the bike rate
convert it into an integer and ddo the final average for all the millisecond time calculation
'''

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