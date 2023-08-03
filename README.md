# File Scanner

A Python script that searches for predefined and custom regular expressions within readable files of a directory.
![image](https://github.com/bdinyarian/LookIn/assets/21012337/98cc182d-dfa2-4888-a519-956b50972f0b)

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
![image](https://github.com/bdinyarian/LookIn/assets/21012337/499475b1-51a4-4572-9695-20c203e1f0eb)

## Requirements

pip install tqdm tabulate colorama

Python 3.6+ is required to run the script.

## Note

The script ignores files of type `audio/`, `video/`, and `application/`. Adjust the `skip_file` function if you want to change the types of files that are ignored.
