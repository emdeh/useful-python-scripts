import argparse
import hashlib
import base64
import os

def cryptBytes(hash_type, salt, value):
    """
    Hashes a given value (password) using a specified hash type and salt.

    :param hash_type: The type of hash algorithm to use (e.g., SHA1, MD5).
    :param salt: The salt to be used in the hashing process.
    :param value: The value (password) to be hashed.
    :return: A string representation of the salted and hashed value.
    """
    if not hash_type:
        hash_type = "SHA256"  # Default hash type changed to SHA256 for better security demonstration
    if not salt:
        # Generate a random salt if none is provided (not used in this script but useful for testing/learning)
        salt = base64.urlsafe_b64encode(os.urandom(16)).decode('utf-8')

    hash_obj = hashlib.new(hash_type)
    hash_obj.update(salt.encode('utf-8'))
    hash_obj.update(value)
    hashed_bytes = hash_obj.digest()
    result = f"${hash_type}${salt}${base64.urlsafe_b64encode(hashed_bytes).decode('utf-8').replace('+', '.')}"
    return result

def main():
    parser = argparse.ArgumentParser(
        description='Hash Cracking Educational Tool',
        epilog=('Example Usage:\n'
                '  Single hash: python3 hash-cracker.py -t SHA256 -s 9876 -H \'exampleHash\' -w /path/to/wordlist.txt\n'
                '  Multiple hashes: python3 hash-cracker.py -t SHA256 -s 9876 -H /path/to/hashfile.txt -w /path/to/wordlist.txt\n\n'
                'Notes:\n'
                '  - Encapsulate inline hashes with single quotes to ensure correct parsing, especially if they contain special characters.\n'),
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('-t', '--hash-type', help='Type of the hash (e.g., SHA1, MD5)', required=True)
    parser.add_argument('-s', '--salt', help='Salt for the hash', required=True)
    parser.add_argument('-H', '--hash', help='The salted hash to be compared against', required=True)
    parser.add_argument('-w', '--wordlist', help='Path to the wordlist file', required=True)

    args = parser.parse_args()

    # Check if the provided hash is a file path
    if os.path.isfile(args.hash):
        with open(args.hash, 'r') as file:
            hashes = [line.strip() for line in file]
    else:
        hashes = [args.hash]

    for search_hash in hashes:
        found = False
        with open(args.wordlist, 'r', encoding='latin-1') as password_list:
            for password in password_list:
                value = password.strip()
                hashed_password = cryptBytes(args.hash_type, args.salt, value.encode('utf-8'))

                if hashed_password == search_hash:
                    print(f'Found Password: {value}, Hash: {hashed_password}')
                    found = True
                    break

        if not found:
            print(f"Password not found for hash: {search_hash}")

if __name__ == "__main__":
    main()
