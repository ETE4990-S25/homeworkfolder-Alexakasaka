import os
import hashlib

def calculate_checksum(file_path, algorithm='sha256'):
    hash_func = hashlib.new(algorithm)
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                hash_func.update(chunk)
        return hash_func.hexdigest()
    except (PermissionError, FileNotFoundError):
        return None

def find_files_by_name(directory):
    file_dict = {}
    for root, _, files in os.walk(directory):
        for file in files:
            if file in file_dict:
                file_dict[file].append(os.path.join(root, file))
            else:
                file_dict[file] = [os.path.join(root, file)]
    return file_dict

def find_identical_files(file_dict):
    identical_files = {}
    for file_name, paths in file_dict.items():
        if len(paths) > 1:
            checksums = {}
            for path in paths:
                checksum = calculate_checksum(path)
                if checksum:
                    if checksum in checksums:
                        checksums[checksum].append(path)
                    else:
                        checksums[checksum] = [path]
            for checksum, identical_paths in checksums.items():
                if len(identical_paths) > 1:
                    identical_files[file_name] = identical_paths
    return identical_files

def main_menu():
    while True:
        print("\nFile System Duplicate Finder")
        print("1. Search for duplicate files")
        print("2. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            directory = input("Enter directory to scan: ")
            if os.path.isdir(directory):
                file_dict = find_files_by_name(directory)
                identical_files = find_identical_files(file_dict)
                if identical_files:
                    print("\nIdentical files found:")
                    for file_name, paths in identical_files.items():
                        print(f"\n{file_name}:")
                        for path in paths:
                            print(f"  {path}")
                else:
                    print("No identical files found.")
            else:
                print("Invalid directory. Try again.")
        elif choice == '2':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please select again.")

if __name__ == "__main__":
    main_menu()