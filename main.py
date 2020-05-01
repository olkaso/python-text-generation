import argparse
import generate
import calculate

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='mode')
parser_generate = subparsers.add_parser('generate_text')
parser_generate.add_argument('input_file', help='file with probabilities')
parser_generate.add_argument('depth', type=int, help='max size for history when generating')
parser_generate.add_argument('tokens_number', type=int, help='length of generated text')
parser_generate.add_argument('--output_file', help='file for generated text '
                                                   '(if not given, printing text to the screen)')
parser_calc = subparsers.add_parser('calculate_probabilities')
parser_calc.add_argument('input_file', type=str, help='file with source text')
parser_calc.add_argument('output_file', type=str, help='file for probabilities')
parser_calc.add_argument('depth', type=int, help='max size for history when calculating')
args = parser.parse_args()

if args.mode == 'generate_text':
    with open(args.input_file, 'rb') as in_file:
        generate.run(in_file, args.depth, args.tokens_number, args.output_file)

elif args.mode == 'calculate_probabilities':
    with open(args.input_file, 'r') as in_file:
        with open(args.output_file, 'wb') as out_file:
            calculate.run(in_file, out_file, args.depth)
else:
    print('Incorrect mode')
