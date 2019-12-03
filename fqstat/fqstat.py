#!/usr/bin/env python3

# standard library
import sys
import argparse
import pathlib

# 3rd-party
from Bio import SeqIO


# helper functions
def err(*args, **kwargs) -> None:
    """Standard error output wrapper for print.

    Returns:
        None
    """
    print(*args, file=sys.stderr, **kwargs)

def search(root_dir: pathlib.Path, pattern: str) -> list:
    """Generic pathlib glob wrapper.

    Args:
        root_dir: Path (pathlib) object that serves as the starting point of 
                  the search.
        pattern: str used to match path(s) or file(s).

    Returns:
        A list of matched paths.
    """
    try:
        return list(root_dir.glob(pattern))
    except AttributeError:
        err('Error: search: root_dir is not a Path object.')
        raise
    except TypeError:
        err('Error: search: Path.glob may have returned an invalid value.')
        raise
    except Exception:
        err('Error: search: An unexpected error occurred.')
        raise

def fqstat(root_dir: pathlib.Path, pattern: str, num_nucleotides: int, verbose: bool) -> None:
    matched_files = search(root_dir, pattern)

    print(f'file\tpercent_gt_{num_nucleotides}')
    for filename in matched_files: # filename is a Path object
        with open(filename, 'r') as f:
            total_records = 0 # used to track the total number of records, due to SeqIO.parse returning a generator, can't use len()
            total_targets = 0 # used to track the records which contain greater than num_nucleotides
            
            # each record is a Bio.SeqRecord.SeqRecord object 
            # see https://biopython.org/DIST/docs/api/Bio.SeqRecord.SeqRecord-class.html
            for record in SeqIO.parse(f, "fastq"):
                total_records += 1 # increment the total number of records
                if len(record.seq) > num_nucleotides: # if sequence contains greater than num_nuceoltides
                    total_targets += 1 

            percent = total_targets/total_records
            print(f'{filename.stem}\t{percent}')

def cli() -> None:
    """Main entry-point for the fqstat command-line interface.

    Returns:
        None
    """
    # initialize the command-line argument parser
    parser = argparse.ArgumentParser(
        description="Example: fqfinder '.' - recursively search the current directory",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter, # enables showing defaults upon -h
    )

    # register arguments to the parser object
    # positional arguments
    parser.add_argument(
        'root_dir', # name of the positional argumentn
        type=lambda p: pathlib.Path(p).absolute(), # enforce it is a valid Path object, then convert it to an absolute path
        help="folder in which the search will begin",
    )

    # flags
    parser.add_argument(
        '--pattern', # name of the optional flag
        type=str,
        default='**/*.fastq', # by default, ** will cause Path.glob to recursively search
        help="a pattern used to match files",
    )
    parser.add_argument(
        '--nucleotides',
        type=int,
        default=30,
        metavar='INT', # the placeholder value that'll be shown in -h
        dest='num_nucleotides', # change keyword that will be used in the code
        help="minimum number of nucleotides",
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help="provide additional information",
    )
    

    # parse argv and return a Namespace object containing the keywords and their values
    args = parser.parse_args()

    # call the core program
    fqstat(args.root_dir, args.pattern, args.num_nucleotides, args.verbose)

if __name__ == '__main__':
    cli()
