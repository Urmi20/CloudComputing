from wand.image import Image


class ImageMagick:
    def image_thumbnail(self, image_name):  # An extra argument has to be included for the thumbnail name
        with Image(filename=image_name) as original:
            with original.convert('png') as self.converted:
                self.converted.transform(resize='320x240>')
                self.converted.save(filename="thumb.png")  # This has to be dynamic
