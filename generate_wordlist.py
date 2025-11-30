#!/usr/bin/env python3
"""Generate a comprehensive word list with unique letters only."""

import os

def generate_unique_letter_words():
    """Extract 4-letter words with unique letters from words_alpha.txt"""
    words_with_unique_letters = []
    
    input_file = 'words_alpha.txt'
    
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found")
        return []
    
    with open(input_file, 'r') as f:
        for line in f:
            word = line.strip().upper()
            # Check if it's 4 letters and all letters are unique
            if len(word) == 4 and len(set(word)) == 4 and word.isalpha():
                words_with_unique_letters.append(word)
    
    # Sort for consistency
    words_with_unique_letters.sort()
    
    print(f"Found {len(words_with_unique_letters)} words with unique letters")
    
    # Write to new file
    output_file = 'valid_words.txt'
    with open(output_file, 'w') as f:
        for word in words_with_unique_letters:
            f.write(word + '\n')
    
    print(f"Saved to {output_file}")
    print(f"First 20 words: {words_with_unique_letters[:20]}")
    print(f"Last 20 words: {words_with_unique_letters[-20:]}")
    
    return words_with_unique_letters

if __name__ == '__main__':
    generate_unique_letter_words()
