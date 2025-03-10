import os
import hashlib
from collections import defaultdict

def calculate_hash(filepath):
    """Calculate SHA-256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        # Read the file in chunks to handle large files efficiently
        for chunk in iter(lambda: f.read(4096), b""):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()

def find_duplicates(directory):
    """Recursively find duplicate files in a directory."""
    # Dictionary to store hash -> list of file paths
    hash_dict = defaultdict(list)
    
    # Walk through directory recursively
    for root, dirs, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            try:
                # Calculate hash and store filepath
                file_hash = calculate_hash(filepath)
                hash_dict[file_hash].append(filepath)
            except (IOError, OSError):
                print(f"Error reading file: {filepath}")
                continue
    
    # Return only entries with duplicates (more than one file path)
    return {k: v for k, v in hash_dict.items() if len(v) > 1}

def display_menu():
    """Display the main menu."""
    print("\n=== Duplicate File Finder ===")
    print("1. Search for duplicate files")
    print("2. Exit")
    return input("Enter your choice (1-2): ")

def main():
    while True:
        choice = display_menu()
        
        if choice == "1":
            directory = input("\nEnter the directory path to search: ")
            
            # Verify directory exists
            if not os.path.isdir(directory):
                print("Error: Invalid directory path!")
                continue
                
            print(f"\nSearching for duplicates in {directory}...")
            duplicates = find_duplicates(directory)
            
            # Display results
            if duplicates:
                print("\nFound duplicate files:")
                for file_hash, file_list in duplicates.items():
                    print(f"\nDuplicate files (Hash: {file_hash}):")
                    for filepath in file_list:
                        print(f"  - {filepath}")
                print(f"\nTotal sets of duplicates found: {len(duplicates)}")
            else:
                print("\nNo duplicate files found.")
                
        elif choice == "2":
            print("Exiting program...")
            break
            
        else:
            print("Invalid choice! Please select 1 or 2.")

if __name__ == "__main__":
    main()