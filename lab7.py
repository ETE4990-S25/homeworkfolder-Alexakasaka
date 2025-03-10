import os
import hashlib

# finding the hash of the file
def calculate_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

#going through the directory
def find_duplicate_files(root_dir):
    files = {}
    file_dict={}
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename not in files:
                files[filename] = []
            files[filename].append(os.path.join(dirpath, filename))
    return file_dict

#comparing the files
def compare_files(file_paths):
    identical_files = []
    if len(file_paths) > 1:
        checksums = {}
            checksum = calculate_md5(file_path)
            if checksum not in checksums:
                checksums[checksum] = []
            checksums[checksum].append(file_path)
        for paths in checksums.values():
            if len(paths) > 1:
                identical_files.append(paths)
    return identical_files

def main():
    root_dir = input("Enter the root directory to search: ")
    
    # Find files with identical names
    files_with_identical_names = find_files_with_identical_names(root_dir)
    
    # Compare files and output identical files (autofilled by copilot)
    all_identical_files = []
    for file_paths in files_with_identical_names.values():
        identical_files = compare_files(file_paths)
        if identical_files:
            all_identical_files.extend(identical_files)
    
    # Output the results
    if all_identical_files:
        print("Identical files found:")
        for group in all_identical_files:
            print("\n".join(group))
            print()
    else:
        print("No identical files found.")
    
if __name__ == "__main__":
    main()