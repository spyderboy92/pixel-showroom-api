from PIL import Image


class LogoAdder:
    """
    A class to add a logo to an image at a specified location.
    pip install pillow
    """

    def __init__(self, input_image_path, logo_path, output_image_path):
        self.input_image_path = input_image_path
        self.logo_path = logo_path
        self.output_image_path = output_image_path

    def add_logo(self, location="top-left"):
        """
        Adds the logo to the input image at the specified location.

        :param location: The position to place the logo.
                         Options: 'top-left', 'top-right', 'bottom-left', 'bottom-right', 'center'
        """
        try:
            # Open the input image (car) and the logo image
            # Convert car image to RGBA (for transparency handling)
            image = Image.open(self.input_image_path).convert("RGBA")
            # Convert logo to RGBA (to preserve transparency)
            logo = Image.open(self.logo_path).convert("RGBA")

            # Resize the logo (optional, scale based on the input image size)
            # Adjust logo size to be 1/7th of the image width
            max_logo_width = image.width // 7
            # Resize logo using LANCZOS filter
            logo.thumbnail((max_logo_width, max_logo_width),
                           Image.Resampling.LANCZOS)

            # Determine the logo position
            positions = {
                "top-left": (10, 10),
                "top-right": (image.width - logo.width - 10, 10),
                "bottom-left": (10, image.height - logo.height - 10),
                "bottom-right": (image.width - logo.width - 10, image.height - logo.height - 10),
                "center": ((image.width - logo.width) // 2, (image.height - logo.height) // 2),
            }

            # Default to 'top-left' if location is invalid
            position = positions.get(location, (10, 10))

            # Paste the logo onto the car image, maintaining transparency
            # Use the logo as the mask to preserve transparency
            image.paste(logo, position, logo)

            # Save the output image as PNG (to preserve transparency)
            image.save(self.output_image_path, format="PNG")

            print(f"Logo added and saved to {self.output_image_path}")
        except Exception as e:
            print(f"An error occurred: {e}")
