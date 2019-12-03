#!/usr/bin/env python3

# standard library
import sys
import argparse
import pathlib
import json

# 3rd-party
from Bio import SeqIO
from prettytable import PrettyTable


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

def fqstat(root_dir: pathlib.Path, pattern: str, num_nucleotides: int, quiet: bool) -> None:
    """Recursively find FastQ files and report the percent of records with 
       nucleotides greater than a provided value per file. Stores results in
       a JSON file.

    Args:
        root_dir: Path (pathlib) object that serves as the starting point of 
                  the search.
        pattern: str used to match path(s) or file(s).
        num_nucleotides: int number of nucleotides used as the cutoff point.
        quiet: bool to prevent printing result table.

    Returns:
        None
    """
    matched_paths = search(root_dir, pattern)
    if not matched_paths: # quickly check if we should even begin the rest of the program
        sys.exit('No files found.')

    data = {} # will be used to store the data collected from all of the found files
    for path in matched_paths: # path is a pathlib.Path object
        with open(path, 'r') as f:
            total_records = 0 # used to track the total number of records, due to SeqIO.parse returning a generator, can't use len()
            total_targets = 0 # used to track the records which contain nucleotides greater than num_nucleotides
            
            # each record is a Bio.SeqRecord.SeqRecord object 
            # see https://biopython.org/DIST/docs/api/Bio.SeqRecord.SeqRecord-class.html for more information
            for record in SeqIO.parse(f, "fastq"):
                total_records += 1 # increment the total number of records
                if len(record.seq) > num_nucleotides: # if sequence contains greater than num_nuceoltides
                    total_targets += 1

            # get the filename, without the .fastq extension
            key = path.stem

            # store data into dictionary
            data[key] = {
                'path': str(path), # convert Path object to a str for serialization
                'total_targets': total_targets,
                'total_records': total_records,
                'percent': round(total_targets/total_records, 4), 
            }
        
    # write data to json file
    with open(f'scan-{num_nucleotides}_nucleotides.json', 'w') as f:
        json.dump(data, f) # convert dictionary to json file

    if not quiet:
        table = PrettyTable() # library to provide a fancy table for easy reading

        # initialize the header row 
        table.field_names = [ 
            'File',
            'Total Targets',
            'Total Records',
            f'Percent (> {num_nucleotides} Nucleotides)',
        ]

        # append rows to the table object
        for key, value in data.items(): 
            table.add_row([
                key,
                value['total_targets'],
                value['total_records'],
                f"{value['percent']*100}%", # convert to easily readable percentage
            ])

        print(table) # display results table

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
        dest='num_nucleotides', # set the keyword from nucleotides to num_nucleotides that will be used in the code
        help="cutoff number of nucleotides",
    )
    parser.add_argument(
        '--quiet',
        action='store_true', # false by default, using --quiet disables printing results
        help="do not print results",
    )

    # parse argv and return a Namespace object containing the keywords and their values
    args = parser.parse_args()

    # call the core program
    fqstat(args.root_dir, args.pattern, args.num_nucleotides, args.quiet)

if __name__ == '__main__':
    cli()
