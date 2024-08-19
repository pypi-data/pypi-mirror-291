#!/usr/bin/env python3
import argparse
import re
import sys
import os
import sys
# pip
from cryptography.fernet import Fernet
# local
from . import KEY_ENVIRONMENT_VARIABLE, encrypt_string, decrypt_markdown

def main():
    ap = argparse.ArgumentParser(description="pipe content into this script and it will be encrypted")
    action = ap.add_mutually_exclusive_group(required=True)
    action.add_argument("-e", "--encrypt", action="store_true", help="encrypt the input text")
    action.add_argument("-d", "--decrypt", action="store_true", help="instead of encrypting the input search for encrypted blocks and decrypt them")
    ap.add_argument("-k", "--key", default=os.getenv(KEY_ENVIRONMENT_VARIABLE), help=f"the key to encrypt the data with. The default is the content of the {KEY_ENVIRONMENT_VARIABLE} environment variable. If an empty string is passed, a new key is generated and prefixed to the output")
    args = ap.parse_args()

    if args.key:
        key = args.key
    else:
        key = Fernet.generate_key().decode()
        print("[*] Encrypted with key:", key, file=sys.stderr)


    text_input = sys.stdin.read()
    if args.decrypt:
        cipher = Fernet(key.encode())
        decrypted_text, counter_success, counter_errors = decrypt_markdown(text_input, cipher, lambda message: print(f"[-] {message}", file=sys.stderr))
        if counter_success + counter_errors > 0:
            if counter_success > 0:
                print(decrypted_text)
                print(f"[*] Decrypted {counter_success} blobs", file=sys.stderr)
            if counter_errors > 0:
                print(f"[-] Failed to decrypt {counter_success} blobs", file=sys.stderr)
        else:
            print(f"[!] The input contained no encrypted blobs", file=sys.stderr)
            exit(1)
    elif args.encrypt:
        print(encrypt_string(text_input, key))
    else:
        print("[!] BUG: Unknown action")
        exit(1)

if __name__ == "__main__":
    main()
