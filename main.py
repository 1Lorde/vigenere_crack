from config import CIPHER_FILENAME
from lib.utils import read_file
from lib.vigenere_analysis import analyze_ciphertext

if __name__ == '__main__':
    ciphertext = read_file(CIPHER_FILENAME)

    analyze_ciphertext(ciphertext)
