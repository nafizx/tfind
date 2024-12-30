import os
import chardet

# Fixed base folder path
base_path = '/storage/emulated/0/'

# ANSI escape codes for styling
class Style:
    HEADER = '\033[95m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    RESET = '\033[0m'

def detect_encoding(file_path):
    """Detect the encoding of a file."""
    try:
        with open(file_path, 'rb') as f:
            raw_data = f.read(4096)
            result = chardet.detect(raw_data)
            return result.get('encoding', 'utf-8')
    except Exception as e:
        print(f"{Style.FAIL}Error detecting encoding for {file_path}: {e}{Style.RESET}")
        return 'utf-8'

def extract_lines_with_keywords(folder, keywords):
    """Search for keywords in text files and write results to separate output files."""
    try:
        output_folder = os.path.join(folder, 'mals')
        os.makedirs(output_folder, exist_ok=True)

        output_files = {keyword: os.path.join(output_folder, f'{keyword}.txt') for keyword in keywords}
        found_lines = {keyword: set() for keyword in keywords}

        print(f"{Style.HEADER}Starting Keyword Extraction...{Style.RESET}\n")

        for root, _, files in os.walk(folder):
            for file in files:
                if file.endswith('.txt'):
                    file_path = os.path.join(root, file)
                    encoding = detect_encoding(file_path)

                    print(f"{Style.OKCYAN}Checking file: {file}{Style.RESET}")
                    file_line_count = 0

                    try:
                        with open(file_path, 'r', encoding=encoding, errors='replace') as f:
                            for line in f:
                                for keyword in keywords:
                                    if keyword.lower() in line.lower():
                                        found_lines[keyword].add(line.strip())
                                        file_line_count += 1
                    except Exception as e:
                        print(f"{Style.FAIL}Error reading file {file_path}: {e}{Style.RESET}")

                    print(f"{Style.OKGREEN}Lines containing keywords in {file}: {file_line_count}{Style.RESET}\n")

        for keyword, lines in found_lines.items():
            if lines:
                output_file = output_files[keyword]
                with open(output_file, 'w', encoding='utf-8') as out_f:
                    out_f.write('\n'.join(lines))
                print(f"{Style.OKGREEN}Keyword '{keyword}' extracted to {output_file}{Style.RESET}")
            else:
                print(f"{Style.WARNING}No lines found for '{keyword}'{Style.RESET}")

    except Exception as e:
        print(f"{Style.FAIL}An error occurred: {e}{Style.RESET}")

print(f"{Style.OKCYAN}Welcome to the Keyword Extractor!{Style.RESET}")
folder_name = input("Enter your folder name: ").strip()
folder_path = os.path.join(base_path, folder_name)

if not os.path.isdir(folder_path):
    print(f"{Style.FAIL}Invalid folder path: {folder_path}{Style.RESET}")
else:
    keywords = input("Enter your keywords (comma-separated): ").split(',')
    keywords = [keyword.strip() for keyword in keywords]
    extract_lines_with_keywords(folder_path, keywords)
