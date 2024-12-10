import unittest
import os
from app.image_processing.logo_adder import LogoAdder  # Adjust path as necessary


class TestLogoAdder(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up paths for input and output directories."""
        cls.car_input_dir = os.path.join(
            os.path.dirname(__file__), '..', 'test_data', 'car')
        cls.logo_input_dir = os.path.join(
            os.path.dirname(__file__), '..', 'test_data', 'logo')
        cls.car_output_dir = os.path.join(
            os.path.dirname(__file__), '..', 'test_output', 'car')

        # Ensure the output directory exists
        os.makedirs(cls.car_output_dir, exist_ok=True)

    def test_add_logo_to_multiple_cars(self):
        """
        Test adding the logo to multiple car images.
        """
        # Get all car images in the input directory
        car_files = [f for f in os.listdir(
            self.car_input_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        logo_file = "logo1.png"
        logo_path = os.path.join(self.logo_input_dir, logo_file)

        for car_file in car_files:
            input_car_path = os.path.join(self.car_input_dir, car_file)
            output_file_name = f"output_{car_file}_{logo_file}"
            output_car_path = os.path.join(
                self.car_output_dir, output_file_name)

            # Process each file
            logo_adder = LogoAdder(input_car_path, logo_path, output_car_path)
            logo_adder.add_logo(location="top-right")

            # Assert that the output file exists
            self.assertTrue(os.path.exists(output_car_path),
                            f"Output file {output_car_path} was not created.")

    def test_invalid_logo_location(self):
        """
        Test adding the logo with an invalid location.
        """
        car_file = "car1.jpg"
        input_car_path = os.path.join(self.car_input_dir, car_file)
        logo_path = os.path.join(
            self.logo_input_dir, "pixel-showroom-logo.avif")
        output_car_path = os.path.join(
            self.car_output_dir, f"output_{car_file}")

        # Process the file with an invalid location
        logo_adder = LogoAdder(input_car_path, logo_path, output_car_path)
        logo_adder.add_logo(location="invalid-location")

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
