'''A code by Bonney Seth and my partner Ramj.
This code is used to apply kernel features to a picture 
by accessing its pixels 
'''


from PIL import Image

class Picture:
    def __init__(self, filename):
        # Initialize the object
        self.im = Image.open(filename)  
        # Open the image using the provided filename
        self.pixel_buffer = self.im.load()  
        # Get a pixel buffer for the image for efficient access
        self.height = self.im.height  
        # Store the height of the image
        self.width = self.im.width  
        # Store the width of the image

    def loadImage(self, path):
        return Image.load(path)  
    # Load an image from a given path (Note: should use 'Image.open')

    def getHeight(self):
        return self.im.height  
    # Get the height of the image

    def getWidth(self):
        return self.im.width  
    # Get the width of the image

    def makeClone(self):
        return self.im.copy()  
    # Create a clone of the current image

    def getPixel(self, coordinates):
        return self.pixel_buffer[coordinates[0], coordinates[1]]  
    # Get the pixel color at specified coordinates

    def setPixel(self, coordinates, color):
        self.pixel_buffer[coordinates[0], coordinates[1]] = color  
        # Set the pixel color at specified coordinates

    def getNewPixel(self, kernel, coordinates):  
        # Calculate a new pixel color based on a weighted average
        # Create a 3x3 kernel with weighted values for neighboring pixels
        weightedValues = [[(0, 0, 0), (0, 0, 0), (0, 0, 0)],
                          [(0, 0, 0), (0, 0, 0), (0, 0, 0)],
                          [(0, 0, 0), (0, 0, 0), (0, 0, 0)]]

        for i in range(-1, 2):
            for j in range(-1, 2):
                try:
                    originalPixel = self.pixel_buffer[coordinates[0] + i, coordinates[1] + j]  
                    # Get the color of the neighboring pixel
                    
                    newPixel = (int(originalPixel[0] * kernel[i + 1][j + 1]),
                                int(originalPixel[1] * kernel[i + 1][j + 1]),
                                int(originalPixel[2] * kernel[i + 1][j + 1]))
                    weightedValues[i + 1][j + 1] = newPixel
                    # Calculate the new pixel color based on the kernel
                except IndexError:
                    continue

        weightedSumRGB = [0, 0, 0]
        for row in weightedValues:
            for weight in row:
                # Calculate the weighted sum of RGB values
                weightedSumRGB[0] += weight[0]
                weightedSumRGB[1] += weight[1]
                weightedSumRGB[2] += weight[2]

        # Ensure the RGB values are within the valid range [0, 255]
        weightedSumRGB[0] = min(255, max(0, int(weightedSumRGB[0])))
        weightedSumRGB[1] = min(255, max(0, int(weightedSumRGB[1])))
        weightedSumRGB[2] = min(255, max(0, int(weightedSumRGB[2])))

        return (weightedSumRGB[0], weightedSumRGB[1], weightedSumRGB[2])  
    # Return the new pixel color

    def applyFilter(self, kernel):
        buffer = []
        for i in range(self.im.height):
            buffer.append([])
            for j in range(self.im.width):
                buffer[i].append((0, 0, 0))
        
        for line in range(self.im.height):
            for pixel in range(self.im.width):
                buffer[line][pixel] = self.getNewPixel(kernel, [pixel, line])  
                # Apply the filter to the image

        for line in range(self.im.height):
            for pixel in range(self.im.width):
                self.pixel_buffer[pixel, line] = buffer[line][pixel]  
                # Update the image with the filtered values

def main():
    img = Picture("tst.jpeg")  
    # Create an instance of the Picture class with an image file
    img.applyFilter([[1/9, 1/9, 1/9],  
                     [1/9, 1/9, 1/9],
                     [1/9, 1/9, 1/9]])
    # Define a simple filter kernel
    img.im.show()  
    # Display the filtered image
    
    noeffect = Picture('tst.jpeg')
    noeffect.im.show()
    # Display the unfiltered image

if __name__ == "__main__":
    main()  # Call the main function when the script is executed
