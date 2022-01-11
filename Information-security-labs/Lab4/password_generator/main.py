from itertools import product
import string
from tqdm import tqdm


def allwords(chars, length):
    for letters in product(chars, repeat=length):
        yield ''.join(letters)

def main(min_length, max_length):
    lat_letters = list(string.ascii_letters)
    cyr_letters = list('АаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя')
    ar_operation = list('+-/*')
    chars = lat_letters + cyr_letters + ar_operation

    lat_letters = set(lat_letters)
    cyr_letters = set(cyr_letters)
    ar_operation = set(ar_operation)
    with open('wordlist.txt', 'w') as file:
        for wordlen in tqdm(range(min_length, max_length)):
            for word in allwords(chars, wordlen):
                if lat_letters.intersection(set(word)) and cyr_letters.intersection(set(word)) and ar_operation.intersection(set(word)):
                    file.write(word+'\n')

if __name__ == "__main__":
    min_length, max_length = 0, 5 

    main(min_length, max_length)
