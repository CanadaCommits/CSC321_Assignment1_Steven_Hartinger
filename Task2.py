
from operator import truediv
from pydoc import plain
from tarfile import BLOCKSIZE

from tarfile import BLOCKSIZE
import os
from typing import final
from Crypto.Util.Padding import pad, unpad

import urllib
import urllib.parse

import binascii
import codecs



BLOCKSIZE = 16

#generate key 16 bytes
key = bytearray(os.urandom(BLOCKSIZE))
print (key)
iv = bytearray(os.urandom(BLOCKSIZE))

def splitArrayInBlocks(givenArray, initSize, endSize):
    givenArray = givenArray[initSize:endSize]
    return givenArray

# performing XOR operation on each value of bytearray
def decryptString(givenBytearray):
    print("DECRYPTING......")
    print("GivenArray length: ", len(givenBytearray))
    initCounter = 0
    count = 16
    tempArray = bytearray()
    newIV = iv
    for index in range(int(len(givenBytearray)/16)):
        tempIV = bytearray()
        splitArray = splitArrayInBlocks(givenBytearray, initCounter, count)
        
        for i in range(len(splitArray)):
            #get plaintext
            x1 = splitArray[i] ^ key[i]
            m1 = x1 ^ newIV[i]
            tempArray.append(m1)
          

            #get new IV for next round
            tempIV.append(splitArray[i])
        newIV = tempIV    
        initCounter = count
        count = count + 16
    print("Decrypt tempArray Length", len(tempArray))
    return tempArray

def encryptString(givenBytearray):
    print("ENCRYPTING......")
    print("GivenArray length: ", len(givenBytearray))
    initCounter = 0
    count = 16
    tempArray = bytearray()
    newIV = iv
    splitArray = splitArrayInBlocks(givenBytearray,0, count)

    for index in range(int(len(givenBytearray)/16)):
        tempIV = bytearray()
        splitArray = splitArrayInBlocks(givenBytearray, initCounter, count)
        
        for i in range(len(splitArray)):
            x1 = splitArray[i] ^ newIV[i]
            y1 = x1 ^ key[i]
            tempIV.append(y1)
            tempArray.append(y1)
        newIV = tempIV    
        initCounter = count
        count = count + 16
    return tempArray

def flipBit(ciphertext):
    #the byte you change in a ciphertext will ONLY affect a byte at the same offset of next plaintext. Our target is at offset 10
    preBlock = splitArrayInBlocks(ciphertext, 0,16)
    decryptBlock = preBlock[10] ^ 97 # a in ascii table
    newCipher = decryptBlock ^ 59
    ciphertext[10] = newCipher


    #for second semicollon offset  => 6 OFFSET
    preBlock2 = splitArrayInBlocks(ciphertext, 16,32)
    decryptBlock2 = preBlock2[5] ^ 97 # a in ascii table
    newCipher2 = decryptBlock2 ^ 59 #semicollon in ascii table
    ciphertext[21] = newCipher2
    return ciphertext

    

def submit():
    stringArray = "userid=456;userdata="
    userInput = "aadmin-truea"
    appendString = ";session-id=31337"

    finalString = stringArray + userInput + appendString
    finalString = urllib.parse.quote(finalString)

    print('finalString', finalString)
    plaintext = bytearray(finalString, 'utf-8')
    print(plaintext)
    ciphertext = encryptString(pad(plaintext, BLOCKSIZE))
    return ciphertext

def verify():
    ciphertext= submit()
    ciphertext = flipBit(ciphertext)

    newPlaintext = decryptString(ciphertext)
    print("26.stelle",newPlaintext[26])
    print("Plaintext", newPlaintext)


    if b';admin-true;' in newPlaintext:
        print("TRUE")
        return True
    else:
        print("FALSE")
        return False
    

verify()
    















