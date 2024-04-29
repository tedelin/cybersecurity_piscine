import time
import hmac
import hashlib
# import argparse

# parser = argparse.ArgumentParser(description="Spider extract all the images from a website")
# parser.add_argument("-g", type=str, default=5, metavar='N', help="The maximum number of levels to extract images")
# parser.add_argument("-k", type=str, default=5, metavar='N', help="The maximum number of levels to extract images")
# args = parser.parse_args()

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

key = "5cc2008fe6aaeb554debe6de19bc4ac3833f02468612726afe3a381c325bdfb6"
print(generate(key, 6))