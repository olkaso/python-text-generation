import argparse
import generate
import calculate
parser = argparse.ArgumentParser()
parser.add_argument('mode', type=str, help='calculate_probabilities or generate_text')
parser.add_argument('--input_file', type=str, help='input file')
parser.add_argument('--output_file', type=str, help='output file')
parser.add_argument('--depth', type=int, help='depth')
parser.add_argument('--tokens_number', type=int, help='length of generated text')
args = parser.parse_args()

if args.mode == 'generate_text':
    in_file = open(args.input_file, 'rb')
    generate.run(in_file, args.depth, args.tokens_number, args.output_file)
    in_file.close()

elif args.mode == 'calculate_probabilities':
    in_file = open(args.input_file, 'r')
    out_file = open(args.output_file, 'wb')
    calculate.run(in_file, out_file, args.depth)
    in_file.close()
    out_file.close()
else:
    print('Incorrect mode')

