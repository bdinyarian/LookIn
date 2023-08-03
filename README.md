# File Scanner

A Python script that searches for predefined and custom regular expressions within readable files of a directory.

The script currently supports a predefined set of regular expression patterns including IP addresses, Social Security numbers, credit card numbers, emails, URLs, hex values, dates, phone numbers, ZIP codes, UUIDs, MAC addresses, Bitcoin addresses, hexadecimal numbers, decimal numbers, and binary numbers.

## Usage

1. Run the script:

    ```shell
    python LookIn.py
    ```

2. The script will start by scanning the directory and list out the readable files.
3. You will be presented with two options:

    - `Search Files`
    - `Exit`

4. If you choose to search files, you'll be presented with a list of predefined regular expressions or you can enter your own.
5. The script will then scan all files in the directory and print any matches it finds.

## Requirements

Python 3.6+ is required to run the script. The following Python packages are also required:

- `os`
- `re`
- `codecs`
- `mimetypes`
- `tqdm`
- `tabulate`
- `colorama`
- `concurrent.futures`

## Note

The script ignores files of type `audio/`, `video/`, and `application/`. Adjust the `skip_file` function if you want to change the types of files that are ignored.
