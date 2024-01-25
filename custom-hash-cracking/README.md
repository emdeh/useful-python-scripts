# Salted Hash Cracking Demo Tool

## Description
This tool is essentially replicates functionality that is very much available in tools like Hashcat.

It demonstrates the process of cracking salted hashes. The tool:

1. Take a known salt and a hash (the salted hash you've recovered).
2. Uses this salt to hash each password from a given wordlist.
3. Compares each of these newly generated hashes against the recovered salted hash.
4. If a match is found, it indicates that the corresponding password from the wordlist is the original password for the recovered hash.


Functionality:

- **Custom Salt Handling:** The script accepts a custom salt, which is crucial for accurately replicating the original hashing process.

- **Wordlist-Based Cracking:** Users can supply a wordlist, which the script iterates through. This simulates a dictionary attack, a common method in password cracking.

- **Hash Comparison:** For each word in the wordlist, the script applies the salt, hashes the result, and compares it against the provided salted hash. This showcases how password recovery tools match hashed passwords.

## Installation
Clone this repository and navigate into the directory.

## Usage
Run the script with the following command:

`python3 script.py -t [HASH_TYPE] -s [SALT] -H [HASH] -w [WORDLIST_PATH]`

Replace `[HASH_TYPE]`, `[SALT]`, `[HASH]`, and `[WORDLIST_PATH]` with your desired values.

## Requirements
Python 3.x

## Example

Use the salt `9876` and the following hashes for testing

This hash should return a password from the wordlist: `$SHA256$9876$ZjfPC_4ZwwfAG7mrDiWWPlCJlXMNC3RWbbfOLyLQ4QE=`

This hash should fail to return a password fro the wordlist: `$SHA256$9876$6YujZBSqHaQiWDuYTuk56PMcpx41LeoVXwsBKbP1jcs=`



