import unittest
import os

from app.image_processing.bg_applier import BackgroundApplier


class TestBackgroundApplier(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up paths for input and output directories."""
        cls.car_input_dir = os.path.join(os.path.dirname(
            __file__), '..', 'test_data', 'bg_removed_car')
        cls.background_input_dir = os.path.join(
            os.path.dirname(__file__), '..', 'test_data', 'background')
        cls.car_output_dir = os.path.join(
            os.path.dirname(__file__), '..', 'test_output', 'car')

        # Ensure the output directory exists
        os.makedirs(cls.car_output_dir, exist_ok=True)

    def test_add_bg_to_multiple_cars(self):
        """
        Test adding the logo to multiple car images.
        """
        # Get all car images in the input directory
        car_files = [f for f in os.listdir(
            self.car_input_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        bg_file = "bg2.jpg"
        bg_path = os.path.join(self.background_input_dir, bg_file)

        for car_file in car_files:
            input_car_path = os.path.join(self.car_input_dir, car_file)
            output_file_name = f"output_{car_file}_{bg_file}"
            output_car_path = os.path.join(
                self.car_output_dir, output_file_name)

            # Process each file
            bg_applier = BackgroundApplier(
                input_car_path, bg_path, output_car_path)
            bg_applier.apply_background()

            # Assert that the output file exists
            self.assertTrue(os.path.exists(output_car_path),
                            f"Output file {output_car_path} was not created.")

    def test_invalid_bg_location(self):
        """
        Test adding the logo with an invalid location.
        """
        car_file = "car1.jpg"
        input_car_path = os.path.join(self.car_input_dir, car_file)
        logo_path = os.path.join(
            self.background_input_dir, "pixel-showroom-logo.avif")
        output_car_path = os.path.join(
            self.car_output_dir, f"output_{car_file}")

        # Process the file with an invalid location
        bg_applier = BackgroundApplier(
            input_car_path, logo_path, output_car_path)
        bg_applier.apply_background()

        # Assert that the output file exists
        self.assertTrue(os.path.exists(output_car_path),
                        f"Output file {output_car_path} was not created.")

    # @classmethod
    # def tearDownClass(cls):
    #     """Clean up all output files after tests."""
    #     for file in os.listdir(cls.car_output_dir):
    #         file_path = os.path.join(cls.car_output_dir, file)
    #         if os.path.isfile(file_path):
    #             os.remove(file_path)


if __name__ == "__main__":
    unittest.main()
