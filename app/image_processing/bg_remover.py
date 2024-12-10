from rembg import remove


class BackgroundRemover:
    """
    pip install rembg pillow onnxruntime
    """

    def __init__(self, input_image_path, output_image_path):
        self.input_image_path = input_image_path
        self.output_image_path = output_image_path

    def remove_background(self):
        """
        Removes the background from the input image and saves the result.
        rembg uses ML model to remove backgrund(like U-Net)
        The model is loaded and executed using onnxruntime, which is optimized for running machine learning models.
        ls -lh ~/.u2net --> u2net.onnx (168MB)
        Output format is png:
         1. Less lossless than jpeg
         2. supports transparent background
        """
        try:
            with open(self.input_image_path, 'rb') as input_file, open(self.output_image_path, 'wb') as output_file:
                input_image = input_file.read()
                output_image = remove(input_image)
                output_file.write(output_image)
            print(f"Background removed and saved to {self.output_image_path}")
        except Exception as e:
            print(f"An error occurred: {e}")
