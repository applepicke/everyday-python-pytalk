import math
import random
import sys


def read_insults(filename):
    columns = [[], [], []]
    with open(filename) as f:
        for line in f:
            items = line.split()
            for i, col in enumerate(columns):
                col.append(items[i])

    return columns


def randomize(column):
    return column[int(math.floor(random.random() * len(column)))]


def main():
    prefix = 'You are a'

    if len(sys.argv) > 1:
        prefix = '%s is a' % sys.argv[1]

    items = [randomize(i) for i in read_insults('insults.txt')]

    if items[0].startswith(('a', 'e', 'i', 'o', 'u')):
        prefix += 'n'

    phrase = ' '.join([prefix] + items)
    print '{0}.'.format(phrase)


if __name__ == '__main__':
    main()
