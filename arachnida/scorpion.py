from PIL import Image, ExifTags
import sys

file_extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]
if len(sys.argv) < 2:
	print("Usage: python scorpion.py <image_file1> <image_file2> ...")
	sys.exit(1)
for img_file in sys.argv[1:]:
	try:
		if (img_file.endswith(tuple(file_extensions)) == False):
			print(f"{img_file} extension not supported")
			continue
		img = Image.open(img_file)
		metadata = img.info
		info_dict = {
			"Filename": img.filename,
			"Image Size": img.size,
			"Image Height": img.height,
			"Image Width": img.width,
			"Image Format": img.format,
			"Image Mode": img.mode,
			"Image is Animated": getattr(img, "is_animated", False),
			"Frames in Image": getattr(img, "n_frames", 1)
		}
		for label,value in info_dict.items():
			print(f"{label:25}: {value}")
		exif_data = img.getexif()
		if exif_data:
			for tag, value in exif_data.items():
				if tag in ExifTags.TAGS:
					print(f"{ExifTags.TAGS[tag]}: {value.decode() if isinstance(value, bytes) else value}")
				else:
					print(f"{tag}: {value}")
		else:
			print(f"No Exif data found for {img_file}")
		print("-----------------------------------")
		img.close()
		
	except IOError:
		print("Failed to open", img_file)