import argparse


def main():
    print('===command_line===')
    parser = argparse.ArgumentParser()
    parser.add_argument('-x', '--xm', type=str, default='xm')
    args = parser.parse_args()
    print(args)
