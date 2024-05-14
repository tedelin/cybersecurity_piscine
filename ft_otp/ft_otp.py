import time
import string
import hmac
import hashlib
import argparse
from cryptography.fernet import Fernet

parser = argparse.ArgumentParser(description="ft_otp generate one time password")
parser.add_argument("-g", type=str, metavar='filename', help="register a new key")
parser.add_argument("-k", type=str, metavar='filename', help="The key used to generate the one time password")
args = parser.parse_args()
key = "N1sUo4OdYvEqA9Xuf1XBwcdBOwoBVqTMtQALNn96nD0="

def encrypt_key(key, plaintext):
    cipher = Fernet(key)
    encrypted_text = cipher.encrypt(plaintext.encode())
    return encrypted_text

def decrypt_key(key, ciphertext):
    cipher = Fernet(key)
    decrypted_text = cipher.decrypt(ciphertext).decode()
    return decrypted_text

def generate(key, codeDigits, time_step=30):
	result = ""
	time_counter = int(time.time()) // time_step
	time_counter_bytes = time_counter.to_bytes(8, byteorder='big')
	b_key = bytes.fromhex(key)
	b_hash = hmac.new(b_key, time_counter_bytes, hashlib.sha1).digest()
	offset = b_hash[-1] & 0xf
	binary = ((b_hash[offset] & 0x7f) << 24) | ((b_hash[offset + 1] & 0xff) << 16) | ((b_hash[offset + 2] & 0xff) << 8) | (b_hash[offset + 3] & 0xff)
	otp = binary % (10 ** codeDigits)
	result = str(otp)
	while (len(result) < codeDigits):
		result = "0" + result
	return result

def register_key(filename):
	try:
		with open(filename, 'r') as f:
			hex_key = f.read()
		if len(hex_key) < 64:
			print("./ft_otp: error: key must be 64 hexadecimal characters.")
			return
		if (all(c in string.hexdigits for c in hex_key) == 0):
			print("./ft_otp: error: key must be 64 hexadecimal characters.")
			return
		encrypted_key = encrypt_key(key, hex_key)
		with open("ft_otp.key", 'wb') as f:
			f.write(encrypted_key)
		print("Key was successfully saved in ft_otp.key.")
	except Exception as e:
		print("An error occurred: ", e)

if args.g:
	register_key(args.g)
elif args.k:
	try:
		with open(args.k, 'rb') as f:
			encrypted_key = f.read()
		hex_key = decrypt_key(key, encrypted_key)
		print(generate(hex_key, 6))
	except Exception as e:
		print("An error occurred: ", e)
