''' 
Code by Bonney Seth with help from my coding partner, Ramj.
This imports the necessary modules: 
graphics for creating graphical elements, random for generating random numbers, 
and math for mathematical functions.
'''
from graphics import *
import random
import math


'''This code makes a simulation of a broad day with sunny weather and
moving clouds
'''

# Function to create a cloud made of circles with similar radii
# and some kind of randomness 
def createCloud(numCircles, origin, chaos, color):
    newCloud = []
    for i in range(numCircles):
        # Create a circle at the specified origin with a small radius of 0.07
        circ = Circle(origin, 0.07)
        
        # Randomly move the circle within a defined chaos factor
        circ.move(random.random() / (10 / chaos), random.random() / (10 / chaos))
        circ.setFill(color)
        circ.setOutline(color)
        newCloud.append(circ)
    return newCloud

# Main function to run the moving scenes
def main():
    '''This prompts the user to input a speed value for the simulation. 
    The loop ensures that the input is a valid positive number.'''
    
    while True:
        userInput = input("Type a number for the speed:  ")
        try:
            userInput = float(userInput)
        except:
            continue
        if userInput > 0:
            break
    
    # This assigns the user-inputted speed to a variable.    
    simulationSpeed = userInput
     
        
    # This creates a graphics window with a specified title, size, and coordinates 
    win = GraphWin('The moving scene',1280,1280, autoflush=False)
    win.setCoords(0, 0, 1, 1)
    win.setBackground(color_rgb(217,231,255))
    
    # Create a sun object
    sunPos = Point(1, 1)
    sun = Circle(sunPos, 0.1)
    sun.setFill('yellow')
    sun.setOutline('white')
    sun.draw(win)
    
    # Create sun rays /arrow-like shapes around the sun
    '''This makes a list arrows and sets the number of arrows to 47
    Note: It can be any number '''
    
    arrows = []
    numArrows = 47
    for i in range(numArrows):
        
        # Calculate directions for the arrow from the sun itself
        offset = 2 * math.pi / numArrows
        p1 = Point(sunPos.getX() + math.cos(2 * math.pi + i * offset - math.pi + 0.05) / 8,
                   sunPos.getY() + math.sin(2 * math.pi + i * offset - math.pi + 0.05) / 8)
        p2 = Point(sunPos.getX() + math.cos(2 * math.pi + i * offset - math.pi + 0.05) * 10,
                   sunPos.getY() + math.sin(2 * math.pi + i * offset - math.pi + 0.05) * 10)
        
        # This creates a line (arrow) connecting the calculated points 
        # and adds it to the list of arrows.
        l = Line(p1, p2)
        l.setWidth(5)
        l.setOutline("yellow")
        l.draw(win)
        arrows.append(l)
    
    # This creates and displays 8 clouds using the createCloud function, 
    # positioning them at different heights
    
    clouds = []
    for i in range(8):
        cloud = createCloud(3, Point(1 / (i + 1), 0.75), 1, "white")
        for j in cloud:
            j.draw(win)
        clouds.append(cloud)
        cloud.append(max(random.random() / 1000, 0.0001))
        
    # Run the simulation loop  
    
    
    '''This initiates a loop that runs as long as the graphics window is open.
    '''  
    while win.isOpen():
        for cloud in clouds:
            speed = cloud[-1]
            for circle in cloud:
                # This ensures the circle being processed is not the speed indicator for the cloud
                if circle != speed:
                    
                # This checks if the circle has moved past the right edge of the screen, 
                # removes it from the cloud, and undraws it.
                    if circle.getP1().getX() > 1:
                        circle.undraw()
                        cloud.remove(circle)
                        continue
                    
                    
                # This moves the circle horizontally based on the simulation speed.
                    circle.move(speed * simulationSpeed, 0)
                    
                    
            '''This handles the replacement of clouds once they move off the screen. 
            It creates a new cloud and adds it to the list.
            '''
            
            if len(cloud) == 1:
                clouds.remove(cloud)
                replacementCloud = createCloud(3, Point(-0.25, 0.75), 1, "white")
                for c in replacementCloud:
                    c.draw(win)
                replacementCloud.append(random.random() / 100)
                clouds.append(replacementCloud)
    
        update(60) # slows down the loop to only 60 times per second

# Run the main function by calling it below        
main()