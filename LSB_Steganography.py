#import image library 
from PIL import Image

#convert each character in data to its 8-bit ASCII binary representation
def convertToBinary(data):
    
    binaryList = []

    for i in data:
        # converts each integer into into an 8-bit string
        # '08b' ensures that all binary representations have 8-bits by padding with leading 0s
        binaryList.append(format(ord(i), '08b'))
    
    return binaryList

def modifyPixels(pixels, dataToEncode):

    #convert data to binary representation 
    binData = convertToBinary(dataToEncode)
    dataLength = len(binData)
    pixelIterator = iter(pixels)

    for i in range(dataLength):
        # extract 3 pixel values at a time 
        conPixel = [value for value in pixelIterator.__next__()[:3] +
                   pixelIterator.__next__()[:3]+ 
                   pixelIterator.__next__()[:3]]
        
        # iterate thourgh each bit in binData 
        # if binData is 0 and pixel value is odd, decrement by 1 to make it even 
        for j in range(0, 8):

            if(binData[i][j] == '0' and conPixel[j] % 2 != 0):
                conPixel[j] -= 1
            # if bin data is 1 and pixel value is even, adjust value to make it odd
            elif (binData[i][j] == '1' and conPixel[j] % 2 == 0):
                if(conPixel[j] != 0):
                    conPixel[j] -= 1
                else:
                    conPixel[j] += 1

        # Change the 9th pixel to signal end of message 
        # if its 0 end of message if 1 keep reading 
        if(i == dataLength - 1):
            if(conPixel[-1] % 2 == 0):
                if(conPixel[-1] != 0):
                    conPixel[-1] -= 1
                else:
                    conPixel[-1] += 1
        else:
            if(conPixel[-1] %2 != 0):
                conPixel[-1] -= 1

        #combine back into 3-pixel values 
        pixelTuple = tuple(conPixel)
        yield pixelTuple[0:3]
        yield pixelTuple[3:6]
        yield pixelTuple[6:9]
        
    

# encodes the given data into the image
def encode(image, data):

    #open image
    newImage = Image.open(image, 'r')

    imageWidth = newImage.size[0]

    # This initializes the coordinates (x, y) that represent the current pixel position in the image, 
    # starting from the top-left corner of the image.
    (x , y) = (0 , 0)

    # iterate through each pixel and get modifyed pixel data
    for pixel in modifyPixels(newImage.getdata(), data):  

        # place modifyed data into a new image
        newImage.putpixel((x, y), pixel)
        
        if(x == imageWidth - 1):
            x = 0
            y += 1
        else:
            x += 1

    split = image.split('.')
    #save as png to prevent pixel changes
    newImageName = split[0] + "_encoded.png" 
    newImage.save(newImageName)

# decode given image
def decode(imageFileName):

    image = Image.open(imageFileName, 'r')

    data = ''
    imageIterator = iter(image.getdata())

    while(True):
        pixels = [value for value in imageIterator.__next__()[:3]+
                  imageIterator.__next__()[:3]+
                  imageIterator.__next__()[:3]]
                
        binaryData = ''

        #read each LSB of pixel data and story in binaryData
        #if last pixel is 0 end message if 1 keep reading 
        for i in pixels[:8]:
            if(i%2 == 0):
                binaryData += '0'
            else:
                binaryData += '1'
    
        #convert binary data to ASCII
        data += chr(int(binaryData, 2))

        if((pixels[-1] % 2) == 1):
            return data
        
def main():

    choice = int(input("=== Steganography === \n" 
                       "Enter 1 to encode \n" 
                       "Enter 2 to decode \n"))
    
    if(choice == 1):
        image = input("Enter image name with extension: ")
        data = input("Enter string you wish to encode: ")
        encode(image, data)
    elif(choice == 2):
        image = input("Enter image name with extenstion you wish to decode: ")
        decodedMessage = decode(image)
        print(decodedMessage)
    else:
        print("Invaid Choice!")


if __name__ == "__main__":
    main()





        
                


