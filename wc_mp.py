import itertools
import string
import os
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-d', help='directory', dest='directory')
parser.add_argument('-f', help='file', dest='file')
args = parser.parse_args()


def map_reduce(i):
    intermidate = list()
    for value in i.values():
        intermidate.extend(mapper(value))
    groups = dict()

    for key, group in itertools.groupby(intermidate, key=lambda x: x[0]):
        groups[key] = list([y for x, y in group])

    return [reducer(intermediate_key, groups[intermediate_key]) for intermediate_key in groups]


def mapper(input_value):
    t = str.maketrans(dict.fromkeys(string.punctuation))
    return [(word, 1) for word in input_value.lower().translate(t).split()]


def reducer(intermediate_key, intermediate_value_list):
    return intermediate_key, sum(intermediate_value_list)


def main():
    if args.directory and args.file:
        print('choice only -d or -f')

    if args.directory:
        try:
            files = list()
            for file in os.listdir(args.directory):
                if file.split('.')[1] == 'txt':
                    files.append(file)

            if len(files) == 0:
                print('not text files in directory')
            else:
                i = {}
                for filename in files:
                    with open('{}/{}'.format(args.directory, filename)) as f:
                        i[filename] = f.read()

                result_count = map_reduce(i)

        except OSError:
            print('directory not found')

    if args.file:
        try:
            if args.file.split('.')[1] != 'txt':
                print('only .txt file')

            else:
                i = {}
                with open(args.file) as f:
                    i[args.file] = f.read()

                result_count = map_reduce(i)

        except OSError:
            print('file not found')

    for v in result_count:
        print('{} - {}'.format(v[0], v[1]))


if __name__ == '__main__':
    main()
