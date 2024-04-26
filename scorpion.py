from PIL import Image
import sys

for img_file in sys.argv[1:]:
	try:
		img = Image.open(img_file)
		metadata = img.info
		print(metadata)
		exif_data = img._getexif()
		if exif_data:
			print("Exif Data:")
			for tag, value in exif_data.items():
				print(f"Tag: {tag}, Value: {value}")
		else:
			print("No Exif data found.")
		
	except IOError:
		print("Cannot open", img_file)