import os
import chardet

def find_non_utf8_files(base_dir, log_dir, replace_originals=False):
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                with open(file_path, 'rb') as f:
                    data = f.read()
                    encoding = chardet.detect(data)['encoding']
                    if encoding != 'utf-8':
                        print(f"Non-UTF-8 file found: {file_path} (encoding: {encoding})")
                        log_file_path = os.path.join(log_dir, f"{file}_non_utf8.txt")
                        utf8_file_path = os.path.join(log_dir, f"{file}_utf8.txt")

                        # Save a copy of the original non-UTF-8 file
                        with open(log_file_path, 'wb') as log_file:
                            log_file.write(data)

                        # Convert the file to UTF-8 and save a copy
                        try:
                            with open(file_path, 'r', encoding=encoding) as original_file:
                                utf8_content = original_file.read()

                            if replace_originals:
                                with open(file_path, 'w', encoding='utf-8') as utf8_file:
                                    utf8_file.write(utf8_content)
                            else:
                                with open(utf8_file_path, 'w', encoding='utf-8') as utf8_file:
                                    utf8_file.write(utf8_content)
                        except UnicodeDecodeError:
                            print(f"Error: Could not convert file {file_path} to UTF-8. Skipping this file.")

if __name__ == "__main__":
    base_dir = input("Enter the directory path to search for non-UTF-8 files: ").strip()
    log_dir = input("Enter the log directory path to store the results: ").strip()
    replace_choice = input("Do you want to replace original files with UTF-8 converted files? (yes/no): ").strip().lower()

    replace_originals = replace_choice == 'yes'
    find_non_utf8_files(base_dir, log_dir, replace_originals)
