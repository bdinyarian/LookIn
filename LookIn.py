import os
import re
import codecs
import mimetypes
from tqdm import tqdm
from tabulate import tabulate
from colorama import Fore, Style
from concurrent.futures import ThreadPoolExecutor

# Display ASCII Art header
def print_header():
    print("""
 ▄█        ▄██████▄   ▄██████▄     ▄█   ▄█▄  ▄█  ███▄▄▄▄   
███       ███    ███ ███    ███   ███ ▄███▀ ███  ███▀▀▀██▄ 
███       ███    ███ ███    ███   ███▐██▀   ███▌ ███   ███ 
███       ███    ███ ███    ███  ▄█████▀    ███▌ ███   ███ 
███       ███    ███ ███    ███ ▀▀█████▄    ███▌ ███   ███ 
███       ███    ███ ███    ███   ███▐██▄   ███  ███   ███ 
███▌    ▄ ███    ███ ███    ███   ███ ▀███▄ ███  ███   ███ 
█████▄▄██  ▀██████▀   ▀██████▀    ███   ▀█▀ █▀    ▀█   █▀  
▀                                 ▀                        
    """)
   
# Predefined regex patterns
PREDEFINED_PATTERNS = {
    'IP Address': r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',
    'Social Security': r'\b\d{3}-\d{2}-\d{4}\b',
    'Credit Card': r'\b(?:\d{4}-){3}\d{4}\b|\b\d{16}\b',
    'Email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
    'URL': r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
    'Hex Value': r'#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})',
    'Date (YYYY-MM-DD)': r'(19|20)\d{2}-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])',
    'Phone Number': r'\(?([0-9]{3})\)?([ .-]?)([0-9]{3})\2([0-9]{4})',
    'ZIP Code': r'[0-9]{5}(?:-[0-9]{4})?',
    'UUID': r'\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b',
    'MAC Address': r'\b(?:[0-9a-fA-F]{2}[:-]){5}[0-9a-fA-F]{2}\b',
    'Bitcoin Address': r'\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b',
    'Hexadecimal': r'\b[0-9A-Fa-f]+\b',
    'Decimal': r'\b\d+\b',
    'Binary': r'\b[01]+\b'
}

# Reads a file and performs a search using a pattern
def read_file_and_search(pattern, file):
    search_results = {}
    try:
        with codecs.open(file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            for match in pattern.finditer(content):
                start = max(0, match.start() - 30)
                end = min(len(content), match.end() + 30)
                context = content[start:end]
                search_results.setdefault(file, []).append(context)
    except (IOError, OSError) as e:
        print(Fore.YELLOW + f"Warning: could not read file {file} due to {str(e)}" + Style.RESET_ALL)
    return search_results

# Determines whether to skip a file based on its MIME type
def skip_file(filename):
    mime, _ = mimetypes.guess_type(filename)
    if mime is None:
        return False
    return mime.startswith('audio/') or mime.startswith('video/') or mime.startswith('application/')

# Scans a directory and returns a list of readable files
def scan_directory():
    files = []
    for root, dirs, filenames in os.walk('.'):
        for filename in filenames:
            if not skip_file(filename):
                files.append(os.path.join(root, filename))
    return len(files), files

# Prints the main menu
def print_menu():
    print(Fore.GREEN + "\n1. Search Files")
    print(Fore.GREEN + "2. Exit\n")

# Prints the regex pattern selection menu
def print_regex_menu():
    table = [[str(i), k, v] for i, (k, v) in enumerate(PREDEFINED_PATTERNS.items(), start=1)]
    print(tabulate(table, headers=['Number', 'Pattern Name', 'Regex Pattern'], tablefmt='pretty'))

# Creates a search pattern from a regex string
def create_search_pattern(search_string):
    try:
        return re.compile(search_string)
    except re.error:
        print(Fore.RED + "Invalid regex. Falling back to simple string search." + Style.RESET_ALL)
        return re.compile(re.escape(search_string))

# Clears the console screen
def clear_screen():
    if os.name == 'nt':    # For Windows
        _ = os.system('cls')
    else:                  # For MacOS and Linux
        _ = os.system('clear')

# Main function
def main():
    clear_screen()
    print_header()
    total_files, files = scan_directory()
    if files:
        file_table = [[file] for file in files]
        print(tabulate(file_table, headers=[Fore.CYAN + f"Readible Files:   {total_files}\n"], tablefmt='pretty'))

    while True:
        print_menu()
        choice = input(Fore.GREEN + "Choose an option: ")
        if choice == '1':
            print('')
            print_regex_menu()
            print('')
            pattern_choice = input("Enter a number to choose a predefined regex, or enter your own pattern: ").strip()
            print('')
            if pattern_choice.isdigit() and int(pattern_choice) in range(1, len(PREDEFINED_PATTERNS) + 1):
                search_string = PREDEFINED_PATTERNS[list(PREDEFINED_PATTERNS.keys())[int(pattern_choice) - 1]]
            elif pattern_choice:
                search_string = pattern_choice
            else:
                print(Fore.RED + "Error: You must enter a non-empty string to search." + Style.RESET_ALL)
                continue
            pattern = create_search_pattern(search_string)
            with ThreadPoolExecutor() as executor:
                future_results = list(tqdm(executor.map(read_file_and_search, [pattern]*len(files), files), total=len(files)))
            results = {k: v for result in future_results for k, v in result.items()}
            if results:
                print(Fore.GREEN + "\nFound search string in the following files:" + Style.RESET_ALL)
                for filename, contexts in results.items():
                    print(Fore.CYAN + "\n" + filename + Style.RESET_ALL)
                    for context in contexts:
                        print(Fore.YELLOW + '    ' + context + Style.RESET_ALL)
            else:
                print(Fore.RED + "\nSearch string not found in any file." + Style.RESET_ALL)

        elif choice == '2':
            print(Fore.GREEN + "\nExiting the program. Goodbye!\n" + Style.RESET_ALL)
            break

        else:
            print(Fore.RED + "\nError: Invalid option chosen. Please choose a valid option.\n" + Style.RESET_ALL)

# Entry point of the script
if __name__ == '__main__':
    main()
