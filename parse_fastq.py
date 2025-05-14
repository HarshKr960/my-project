#!/usr/bin/env python3

import sys

def parse_fastq(fastq_file):
    """Parse a FASTQ file and print basic statistics."""
    try:
        with open(fastq_file, 'r') as f:
            read_count = 0
            total_bases = 0
            headers = []

            while True:
                header = f.readline().strip()
                seq = f.readline().strip()
                plus = f.readline().strip()
                qual = f.readline().strip()

                if not qual:
                    break  # End of file

                read_count += 1
                total_bases += len(seq)
                if read_count <= 5:
                    headers.append(header)

            print(f"Total reads: {read_count}")
            print(f"Average read length: {total_bases / read_count if read_count else 0:.2f}")
            print("First few read headers:")
            for h in headers:
                print(f"  {h}")

    except FileNotFoundError:
        print(f"Error: File '{fastq_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <input.fastq>")
        sys.exit(1)

    fastq_path = sys.argv[1]
    parse_fastq(fastq_path)
