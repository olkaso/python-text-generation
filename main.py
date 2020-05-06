import argparse
import generate
import calculate

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='mode')
parser_generate = subparsers.add_parser('generate_text')
parser_generate.add_argument('--input_file', help='file with probabilities', required=True)
parser_generate.add_argument('--depth', type=int, help='max size for history when generating', required=True)
parser_generate.add_argument('--tokens_number', type=int, help='length of generated text', required=True)
parser_generate.add_argument('--output_file', help='file for generated text '
                                                   '(if not given, printing text to the screen)')
parser_calc = subparsers.add_parser('calculate_probabilities')
parser_calc.add_argument('--input_file', help='file with source text', required=True)
parser_calc.add_argument('--output_file', help='file for probabilities', required=True)
parser_calc.add_argument('--depth', type=int, help='max size for history when calculating', required=True)
args = parser.parse_args()

if args.mode == 'generate_text':
    with open(args.input_file, 'rb') as in_file:
        generate.run_generation(in_file, args.depth, args.tokens_number, args.output_file)

elif args.mode == 'calculate_probabilities':
    with open(args.input_file, 'r') as in_file:
        with open(args.output_file, 'wb') as out_file:
            calculate.run_calculation(in_file, out_file, args.depth)
else:
    parser.print_help()
