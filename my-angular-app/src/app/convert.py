from PIL import Image
import numpy as np

# read the text file
with open('imag.txt', 'r') as f:
    data = eval(f.read())

# convert the list to a numpy array
data_arr = np.array(data, dtype=np.uint8)

# reshape the array to get the image dimensions
height, width, channels = data_arr.shape
data_arr = data_arr.reshape((height, width, 3))

# create an image from the array
img = Image.fromarray(data_arr)

# save the image to disk
img.save('TestOutput.png')