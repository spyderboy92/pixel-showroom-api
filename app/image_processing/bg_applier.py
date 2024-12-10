from PIL import Image


class BackgroundApplier:
    """
    A class to apply a background image to a car image with the background removed.
    pip install pillow
    """

    def __init__(self, car_image_path, background_image_path, output_image_path):
        self.car_image_path = car_image_path
        self.background_image_path = background_image_path
        self.output_image_path = output_image_path

    def apply_background(self):
        """
        Applies the background image to the car image with removed background.
        """
        try:
            # Open the background image and car image (with removed background)
            background = Image.open(self.background_image_path).convert(
                "RGBA")  # Ensure background is RGBA
            # Ensure car image is RGBA (to preserve transparency)
            car_image = Image.open(self.car_image_path).convert("RGBA")

            # Resize background to fit the car image size (optional, you can skip resizing)
            background = background.resize(
                car_image.size, Image.Resampling.LANCZOS)

            # Paste the car image on top of the background, preserving transparency
            # Use car image as a mask to preserve its transparency
            background.paste(car_image, (0, 0), car_image)

            # Save the final output image
            # Save as PNG to preserve transparency
            background.save(self.output_image_path, format="PNG")

            print(f"Background applied and saved to {self.output_image_path}")
        except Exception as e:
            print(f"An error occurred: {e}")
