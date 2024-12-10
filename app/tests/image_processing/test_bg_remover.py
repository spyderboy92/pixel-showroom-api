import os
import unittest
from app.image_processing.bg_remover import BackgroundRemover


class TestBackgroundRemover(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up paths for input and output directories."""
        cls.input_dir = os.path.join(os.path.dirname(
            __file__), '..', 'test_data', 'car')
        cls.output_dir = os.path.join(os.path.dirname(
            __file__),  '..', 'test_output', 'car')

        # Ensure the output directory exists
        os.makedirs(cls.output_dir, exist_ok=True)

    def test_remove_background_batch_jpeg(self):
        """Test background removal for multiple jpeg images."""
        # Get all .jpg/ .jpeg files in the input directory
        input_files = [f for f in os.listdir(
            self.input_dir) if f.endswith(('.jpg', '.jpeg'))]

        for input_file in input_files:
            input_path = os.path.join(self.input_dir, input_file)
            # Prefix output and change extension
            output_file_name = f"output_{input_file.rsplit('.', 1)[0]}.jpg.png"
            output_path = os.path.join(self.output_dir, output_file_name)

            # Process each file
            remover = BackgroundRemover(input_path, output_path)
            remover.remove_background()

            # Assert that the output file exists
            self.assertTrue(os.path.exists(output_path),
                            f"Output file {output_path} was not created.")

    def test_remove_background_batch_webp(self):
        """Test background removal for multiple webp images."""
        # Get all .webp files in the input directory
        input_files = [f for f in os.listdir(
            self.input_dir) if f.endswith('.webp')]

        for input_file in input_files:
            input_path = os.path.join(self.input_dir, input_file)
            # Prefix output and change extension
            output_file_name = f"output_{input_file.rsplit('.', 1)[0]}.webp.png"
            output_path = os.path.join(self.output_dir, output_file_name)

            # Process each file
            remover = BackgroundRemover(input_path, output_path)
            remover.remove_background()

            # Assert that the output file exists

    # Uncomment this if you want to clean up after the test
    # @classmethod
    # def tearDownClass(cls):
    #     """Clean up the output directory after tests."""
    #     for file in os.listdir(cls.output_dir):
    #         file_path = os.path.join(cls.output_dir, file)
    #         os.remove(file_path)


if __name__ == '__main__':
    unittest.main()
