import os
import chardet

# Specify folder path
folder_path = r'/storage/emulated/0/december'  # Adjust to your Termux-accessible directory

# ANSI escape codes for styling
class Style:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'  # Reset to default

def detect_encoding(file_path):
    """Detect the encoding of a file."""
    try:
        with open(file_path, 'rb') as f:
            raw_data = f.read(4096)  # Increase sample size for better detection
            result = chardet.detect(raw_data)
            return result.get('encoding', 'utf-8')  # Default to UTF-8 if uncertain
    except Exception as e:
        print(f"{Style.FAIL}Error detecting encoding for {file_path}: {e}{Style.RESET}")
        return 'utf-8'  # Fallback to UTF-8

def extract_lines_with_keywords(folder, keywords):
    """Search for keywords in text files and write results to separate output files."""
    try:
        output_files = {keyword: os.path.join(folder, f'{keyword}.txt') for keyword in keywords}
        found_lines = {keyword: set() for keyword in keywords}

        # Stylish header
        print(f"{Style.HEADER}{Style.BOLD}Starting Keyword Extraction...{Style.RESET}\n")

        # Walk through all files in the folder
        for root, _, files in os.walk(folder):
            for file in files:
                if file.endswith('.txt'):
                    file_path = os.path.join(root, file)
                    total_lines_found = 0

                    # Detect encoding
                    encoding = detect_encoding(file_path)

                    # Read the file and search for keywords
                    try:
                        with open(file_path, 'r', encoding=encoding, errors='replace') as f:
                            for line in f:
                                for keyword in keywords:
                                    if keyword.lower() in line.lower():
                                        found_lines[keyword].add(line.strip())
                                        total_lines_found += 1
                    except Exception as read_error:
                        print(f"{Style.FAIL}Error reading file {file_path}: {read_error}{Style.RESET}")

                    # Display the number of lines found for this file
                    print(f"{Style.OKBLUE}Processing: {file_path}{Style.RESET}")
                    print(f"{Style.OKGREEN}Total lines found: {total_lines_found}{Style.RESET}\n")

        # Write results to output files
        for keyword, lines in found_lines.items():
            if lines:
                output_file = output_files[keyword]
                try:
                    with open(output_file, 'w', encoding='utf-8') as out_f:
                        out_f.write('\n'.join(lines))
                    print(f"{Style.OKCYAN}Task completed for '{Style.BOLD}{keyword}{Style.RESET}{Style.OKCYAN}'. {len(lines)} unique lines written to {output_file}{Style.RESET}")
                except Exception as write_error:
                    print(f"{Style.FAIL}Error writing to {output_file}: {write_error}{Style.RESET}")
            else:
                print(f"{Style.WARNING}No lines containing '{keyword}' found.{Style.RESET}")

    except Exception as e:
        print(f"{Style.FAIL}An error occurred: {e}{Style.RESET}")

# Get keywords from the user
print(f"{Style.BOLD}{Style.OKCYAN}Welcome to the Keyword Extractor!{Style.RESET}")
keywords = input(f"{Style.BOLD}Enter your keywords (comma-separated): {Style.RESET}").split(',')
keywords = [keyword.strip() for keyword in keywords]  # Remove extra spaces

# Run the function
extract_lines_with_keywords(folder_path, keywords)
