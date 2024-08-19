import os
import re
# pip dependencies
from cryptography.fernet import Fernet

# Pattern: {ENCRYPTED:some-base64-value==} or the same in URL encoded
# I think this was necessary for when I encrypt contents in places like a link (a.href)
_OPEN_CURLY = "(?:{|%7B|%7b)"
_COLON = "(?::|%3A|%3a)"
_EQUAL = "(?:=|%3D|%3d)"
_CLOSE_CURLY = "(?:}|%7D|%7d)"
ENCRYPTION_REGEX = re.compile(f'{_OPEN_CURLY}ENCRYPTED{_COLON}([a-zA-Z0-9-+_/]+{_EQUAL}*){_CLOSE_CURLY}')

KEY_ENVIRONMENT_VARIABLE = "MKDOCS_ENCRYPT_SOURCE_KEY"

def encrypt_string(text: str, key: str):
    # This already returns a base64 encoded string
    encrypted = Fernet(key).encrypt(text.encode()).decode()

    return "{ENCRYPTED:%s}".replace("%s", encrypted)


def decrypt_markdown(markdown, cipher_suite, error_callback):
    """
    This function searches an input text (`markdown`) for encypted blobs and decrypts them with the given cipher (`cipher_suite`).
    If the decryption fails, error_callback is called with a message string describing the error. You can set it to `print`, `logger.error` or something similar.
    When all blobs have been replaced, the function returns the markdown with all decrypted blobs and counters for how many blobs were decrypted and how many failed on the site.
    The return data is expressed as a tuple (decrypted_markdown: str, counter_success: int, counter_error: int)
    """
    decrypted_markdown = markdown
    counter_success = 0
    counter_error = 0

    for match in ENCRYPTION_REGEX.finditer(markdown):
        encrypted_text = match.group(1).replace("%3D", "=").replace("%3d", "=")
        try:
            # Decrypt the text
            decrypted_text = cipher_suite.decrypt(encrypted_text).decode()
            # Replace the encrypted text in the markdown with the decrypted text
            decrypted_markdown = decrypted_markdown.replace(match.group(0), decrypted_text)
            counter_success += 1
        except Exception as e:
            error_callback(f"Error decrypting blob '{match.group(0)}': {e}")
            counter_error += 1

    return (decrypted_markdown, counter_success, counter_error)
