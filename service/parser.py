import argparse


class Parser:

    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-i', '--input', required=True)
        parser.add_argument('-o', '--output', required=True)
        args = parser.parse_args()
        self.input = args.input
        self.output = args.output
        
