#!/usr/bin/env python3

import sys
import random
import string
import argparse

def generate_random_sequence(length, seed=None):
    """Generate a random sequence of letters with optional seed for reproducibility"""
    if seed is not None:
        random.seed(seed)
    letters = string.ascii_letters
    sequence = ''.join(random.choice(letters) for _ in range(length))
    split_sequence = '\n'.join(sequence[i:i+80] for i in range(0, len(sequence), 80))
    return split_sequence

def main():
    parser = argparse.ArgumentParser(description="Generate random letter sequences")
    parser.add_argument("-l", "--length", type=int, required=True,
                      help="Length of the sequence to generate")
    parser.add_argument("-s", "--seed", type=int, default=None,
                      help="Seed value for reproducible results")
    
    args = parser.parse_args()
    
    if args.length <= 0:
        print("Error: Length must be a positive integer", file=sys.stderr)
        sys.exit(1)
        
    sequence = generate_random_sequence(args.length, args.seed)
    print(sequence)

if __name__ == "__main__":
    main()
