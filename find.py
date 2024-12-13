import os
import chardet

# Specify folder path and keywords
folder_path = r'/storage/emulated/0/december'  # Adjust to your Termux-accessible directory
keywords = ['facebook']  # Replace with your keywords
output_files = {keyword: os.path.join(folder_path, f'{keyword}.txt') for keyword in keywords}


def detect_encoding(file_path):
    """Detect the encoding of a file."""
    try:
        with open(file_path, 'rb') as f:
            raw_data = f.read(4096)  # Increase sample size for better detection
            result = chardet.detect(raw_data)
            return result.get('encoding', 'utf-8')  # Default to UTF-8 if uncertain
    except Exception as e:
        print(f"Error detecting encoding for {file_path}: {e}")
        return 'utf-8'  # Fallback to UTF-8


def extract_lines_with_keywords(folder, keywords, output_files):
    """Search for keywords in text files and write results to separate output files."""
    try:
        found_lines = {keyword: set() for keyword in keywords}

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
                        print(f"Error reading file {file_path}: {read_error}")

                    # Display the number of lines found for this file
                    print(f"Processing: {file_path}")
                    print(f"Total lines found: {total_lines_found}")

        # Write results to output files
        for keyword, lines in found_lines.items():
            if lines:
                output_file = output_files[keyword]
                try:
                    with open(output_file, 'w', encoding='utf-8') as out_f:
                        out_f.write('\n'.join(lines))
                    print(f"Task completed for '{keyword}'. {len(lines)} unique lines written to {output_file}")
                except Exception as write_error:
                    print(f"Error writing to {output_file}: {write_error}")
            else:
                print(f"No lines containing '{keyword}' found.")

    except Exception as e:
        print(f"An error occurred: {e}")


# Run the function
extract_lines_with_keywords(folder_path, keywords, output_files)
