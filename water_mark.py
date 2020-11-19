from datetime import datetime
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont



class WaterMark:
	"""Class contain all the method for water mark"""

	def water_mark(image_path, url, ref_id):
		pos = (0, 10)
		pos1 = (350, 700)
		text = url
		text2 = ref_id + " " + str(datetime.now().time())
		photo = Image.open(image_path)
		# make the image editable
		drawing = ImageDraw.Draw(photo)
		black = (3, 8, 12)
		font = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 15)
		font2 = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 30)
		drawing.rectangle((0,10,1300,30), fill='white')
		drawing.rectangle((0,700,1290,1250), fill='white')
		drawing.text(pos, text, fill=black, font=font)
		drawing.text(pos1, text2, fill=black, font=font2)
		photo.save(image_path)



