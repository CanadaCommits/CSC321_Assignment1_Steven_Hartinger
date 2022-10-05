from tarfile import BLOCKSIZE
import os
from Crypto.Util.Padding import pad, unpad

BLOCKSIZE = 16

#generate key 16 bytes
key = bytearray(os.urandom(BLOCKSIZE))
print (key)

# Open the Image
with open("mustang.bmp", "rb") as imageFile:
    mustangRead = imageFile.read()
    mustangArray = bytearray(mustangRead)

# Open the Image of choice, Dump all binary of BMP file
with open("cp-logo.bmp", "rb") as imageFile:
    logoRead = imageFile.read()
    logoArray = bytearray(logoRead)

# BMP Header size (start of pixel data)

def splitArrayInBlocks(givenArray, initSize, endSize):
    givenArray = givenArray[initSize:endSize]
    return givenArray

#for replacing header
def append_header(givenBytearray):
 for s in range(54):
        givenBytearray[0:53] = mustangArray[0:53]

# performing XOR operation on each value of bytearray
def decryptBMPFile(givenBytearray):
    print("DECRYPTING......")
    print("GivenArray length: ", len(givenBytearray))
    initCounter = 0
    count = 16
    tempArray = bytearray()
    for index in range(int(len(givenBytearray)/16)):
        splitArray = splitArrayInBlocks(givenBytearray, initCounter, count)
        
        for i in range(len(splitArray)):
            m = splitArray[i] ^key[i]
            tempArray.append(m)
        initCounter = count
        count = count + 16
    print("Decrypt tempArray Length", len(tempArray))
    append_header(tempArray)

    return tempArray

def encryptBMPFile(givenBytearray):
    print("ENCRYPTING......")
    print("GivenArray length: ", len(givenBytearray))
    initCounter = 0
    count = 16
    tempArray = bytearray()
    splitArray = splitArrayInBlocks(givenBytearray,0, count)

    for index in range(int(len(givenBytearray)/16)):
        splitArray = splitArrayInBlocks(givenBytearray, initCounter, count)
        
        for i in range(len(splitArray)):
            c = splitArray[i] ^ key[i]
            tempArray.append(c)
        initCounter = count
        count = count + 16
    print("Decrypt tempArray Length", len(tempArray))
    append_header(tempArray)

    return pad(tempArray, BLOCKSIZE)

def write_encryped_file(givenArray, path):
    f = open(path, "wb")
    f.write(encryptBMPFile(givenArray))
    f.close()

def write_decrypted_file(givenArray, path):
    f = open(path, "wb")
    f.write(decryptBMPFile(givenArray))
    f.close()


write_encryped_file(mustangArray, "ECB_mustang_encrypted.bmp")
write_decrypted_file(encryptBMPFile(mustangArray), "ECB_mustang_decrypted.bmp")





