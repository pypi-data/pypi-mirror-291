import argparse
import os
from auto_code.md_bot import MarkdownBot


def main():
    """Main entry point for the Auto Code CLI Tool."""
    parser = argparse.ArgumentParser(description="Back End Bot CLI Tool")
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Front end focused refinement
    parser_front_end = subparsers.add_parser('refine')
    
    parser_front_end.add_argument('--dir', type=str, help='Directory containing files')
    parser_front_end.add_argument('--ext', type=str, help='File extension to load')
    parser_front_end.add_argument('--file', type=str, help='Full file path')

    args = parser.parse_args()

    auto_code = MarkdownBot() # Call class 

    if args.command == 'refine':

        if args.file:
            assert os.path.isfile(args.file), f"Error: The specified file '{args.file}' does not exist."
            file_list = [args.file]
        else:
            assert os.path.isdir(args.dir), f"Error: The specified directory '{args.dir}' does not exist."
            assert args.ext, "Error: File extension must be provided when specifying a directory."
            file_list = auto_code.get_files(args.dir, args.ext)
        auto_code.refine(file_list)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()