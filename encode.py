import math
from PIL import Image


def encodeLzw(uncompressed):
    dict_size = 256
    dictionary = {}
    for i in range(dict_size):
        dictionary[chr(i)] = i

    w = ""
    for c in uncompressed:
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            encoded_version.append(dictionary[w])
            dictionary[wc] = dict_size
            dict_size += 1
            w = c

    if w:
        encoded_version.append(dictionary[w])

    # appending length of list as first element
    N = len(encoded_version)
    encoded_version.append(N)
    encoded_version[0], encoded_version[N] = encoded_version[N], encoded_version[0]


encoded_version = []

# int length is taken to be 16 bits
if __name__ == "__main__":
    input_string = input("Enter a string to encode: ")
    encodeLzw(input_string)
    encoded_bin_version = []  # final list to insert in image each entry is 16-bit string
    for i in range(0, len(encoded_version)):
        current_string = '{0:016b}'.format(encoded_version[i])
        for j in range(0, 8):  # parsing current string into 8 parts
            encoded_bin_version.append(current_string[2 * j:2 * j + 2])

    ctr = 0
    n = len(encoded_bin_version) - 1

    im = Image.open('input.png')
    pixelMap = im.load()

    img = Image.new(im.mode, im.size)
    pixelsNew = img.load()

    for i in range(0, img.size[0]):
        for j in range(0, img.size[1]):
            if ctr > n:
                pixelsNew[i, j] = pixelMap[i, j]
            else:
                original_pixel = pixelMap[i, j][0]  # changing the value of red pixel
                encoded_pixel = 4 * math.floor(original_pixel / 4) + int(encoded_bin_version[ctr], 2)
                pixelsNew[i, j] = (encoded_pixel, pixelMap[i, j][1], pixelMap[i, j][2])
                ctr = ctr + 1

    img.save('output.png')
    img.close()
    im.close()
