from PIL import Image


def decodeLzw(compressed):
    dict_size = 256
    dictionary = {}
    for i in range(dict_size):
        dictionary[i] = chr(i)

    if compressed:
        w = chr(compressed.pop(0))

    result = [w]

    for k in compressed:
        if k in dictionary:
            entry = dictionary[k]
        elif k == len(dictionary):
            entry = w + w[0]
        result.append(entry)

        dictionary[dict_size] = w + entry[0]
        dict_size += 1

        w = entry

    return ''.join(result)


if __name__ == '__main__':
    img = Image.open('output.png')
    pixelMap = img.load()

    # extracting the length of compressed message
    compressed_len = 1  # there is extra character in encoded_version
    for i in range(0, 8):
        compressed_len = compressed_len + (pixelMap[0, i][0] % 4) * (4 ** (7 - i))

    compressed = []

    curr_code = 0
    code_ctr = 0
    loop_ctr = 0
    for i in range(0, img.size[0]):
        for j in range(0, img.size[1]):
            if loop_ctr > compressed_len * 8:
                break;

            if code_ctr == 8:
                compressed.append(curr_code)
                curr_code = (pixelMap[i, j][0] % 4) * (4 ** 7)
                code_ctr = 1
            else:
                curr_code = curr_code + (pixelMap[i, j][0] % 4) * (4 ** (7 - code_ctr))
                code_ctr = code_ctr + 1
            loop_ctr = loop_ctr + 1

        if loop_ctr > compressed_len * 8:
            break;

    n = len(compressed) - 1
    compressed[0], compressed[n] = compressed[n], compressed[0]
    compressed.pop(n)
    print(decodeLzw(compressed))