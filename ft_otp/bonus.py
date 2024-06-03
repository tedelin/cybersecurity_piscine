import time
import tkinter as tk
from PIL import ImageTk, Image
from tkinter import filedialog, messagebox
import segno
import string
import hmac
import hashlib
import argparse

parser = argparse.ArgumentParser(description="ft_otp generate one time password")
parser.add_argument("-g", type=str, metavar='filename', help="register a new key")
parser.add_argument("-k", type=str, metavar='filename', help="The key used to generate the one time password")
args = parser.parse_args()

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
	code.set(result)
	segno.make(result).save("code.png")
	img = ImageTk.PhotoImage(Image.open("code.png").resize((400, 400)))
	canva.create_image(0, 0, anchor="nw", image=img)
	canva.image = img
	return result

window = tk.Tk()
window.title("ft_otp")
window.geometry("500x500")
window.resizable(False, False)
while (1):
	key_file = filedialog.askopenfilename(title='Select the key file')
	with open(key_file, 'r') as f:
		hex_key = f.read()
	if len(hex_key) < 64:
		messagebox.showerror("Invalid Key", "error: key must be 64 hexadecimal characters.")
	if (all(c in string.hexdigits for c in hex_key) == 0):
		messagebox.showerror("Invalid Key", "error: key must be 64 hexadecimal characters.")
	else:
		break
key = open(key_file, 'r').read()
code = tk.StringVar()
totp_code = tk.Label(window, textvariable=code)
totp_code.pack()
generate_code = tk.Button(window, text="Generate", command=lambda : generate(key, 6))
generate_code.pack()
canva = tk.Canvas(window, width=400, height=400, bg="white")
canva.pack()
window.mainloop()
