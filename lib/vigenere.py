from config import ALPHABET


def decrypt(key, message, alphabet):
    alphabet_str = ''.join(map(str, alphabet))
    plaintext = []

    key_index = 0
    for symbol in message:  # loop through each character in message
        num = alphabet_str.find(symbol)
        if num != -1:  # -1 means symbol was not found in LETTERS
            num -= alphabet_str.find(key[key_index])  # subtract if decrypting
            num %= len(alphabet_str)  # handle the potential wrap-around
            # add the encrypted/decrypted symbol to the end of translated.
            plaintext.append(alphabet_str[num])
            key_index += 1  # move to the next letter in the key
            if key_index == len(key):
                key_index = 0
        else:
            # The symbol was not in LETTERS, so add it to translated as is.
            plaintext.append(symbol)

    return ''.join(plaintext)
