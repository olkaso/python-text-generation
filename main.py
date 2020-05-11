import argparse
import generate
import calculate


def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='mode')
    parser_generate = subparsers.add_parser('generate_text')
    parser_generate.add_argument('--input_file', help='file with probabilities', required=True)
    parser_generate.add_argument('--depth', type=int, help='max size for history when generating', required=True)
    parser_generate.add_argument('--tokens_number', type=int, help='length of generated text', required=True)
    parser_generate.add_argument('--output_file', help='file for generated text '
                                                       '(if not given, printing text to the screen)')
    parser_generate.add_argument('--paragraph_size', type=int, help='average size of the paragraph (100 by default)',
                                 default=100)
    parser_calc = subparsers.add_parser('calculate_probabilities')
    parser_calc.add_argument('--input_file', help='file with source text', required=True)
    parser_calc.add_argument('--output_file', help='file for probabilities', required=True)
    parser_calc.add_argument('--depth', type=int, help='max size for history when calculating', required=True)
    return parser.parse_args()


def main():
    args = parse_args()
    if args.mode == 'generate_text':
        generate.run_generation(args.input_file, args.depth, args.tokens_number, args.paragraph_size, args.output_file)
    elif args.mode == 'calculate_probabilities':
            calculate.run_calculation(args.input_file, args.output_file, args.depth)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
