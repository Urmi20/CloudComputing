from wand.image import Image
from app.tools.fileTools import FileManager


class ImageTransform:

    @staticmethod
    def make_transformations(image_full_path):
        f_mgr = FileManager()
        extension = f_mgr.get_file_extension(image_full_path)
        with Image(filename=image_full_path) as img:

            # Generating thumbnail
            with img.clone() as transformation:
                factor = transformation.height/200
                transformation.resize(int(transformation.width/factor), int(transformation.height/factor))
                full_path_thumb = f_mgr.directory + f_mgr.gen_unique_file_name('thumbnail') + extension
                transformation.save(filename=full_path_thumb)

            # Generating warm colors
            with img.clone() as transformation:
                transformation.evaluate(operator='rightshift', value=1, channel='blue')
                transformation.evaluate(operator='leftshift', value=1, channel='red')
                full_path_warm = f_mgr.directory + f_mgr.gen_unique_file_name('warm') + extension
                transformation.save(filename=full_path_warm)

            # Generating black and white
            with img.clone() as transformation:
                transformation.type = 'grayscale'
                full_path_bw = f_mgr.directory + f_mgr.gen_unique_file_name('b&w') + extension
                transformation.save(filename=full_path_bw)

            # Generating high contrast
            with img.clone() as transformation:
                transformation.contrast_stretch(black_point=0.1, white_point=1.0, channel='all_channels')
                full_path_high_contrast = f_mgr.directory + f_mgr.gen_unique_file_name('high contrast') + extension
                transformation.save(filename=full_path_high_contrast)

            filename_map = {
                "thumbnail": FileManager.extract_filename(full_path_thumb),
                "warm": FileManager.extract_filename(full_path_warm),
                "b&w": FileManager.extract_filename(full_path_bw),
                "high contrast": FileManager.extract_filename(full_path_high_contrast)
            }

            return filename_map
