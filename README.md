## LSB_Steganography

LSB_Steganography is a command line application that takes in a specified image and a string that is to be encoded in that image. 
The application changes the least significant bit of each pixels RGB value to hide the given data.
Each character of the input string is converted into its binary representation and stored in a list.
The application then works in batchs of 9 pixels at a time. Iterating over each bit in the list and storing it in each 
pixel vaule. The image is then saved and the changes to the image are indistinguishable to the human eye.







