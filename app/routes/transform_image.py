from flask_restx import Namespace, Resource, reqparse
from flask import request, jsonify, send_file
from werkzeug.datastructures import FileStorage

from app.image_processing.bg_applier import BackgroundApplier
from app.image_processing.bg_remover import BackgroundRemover
from io import BytesIO
import tempfile
import os

from app.image_processing.logo_adder import LogoAdder

# Define the upload namespace
api = Namespace(
    'CarImageProcess', description='Car Image upload and process', path='/')

# Define a parser for file upload
upload_image_parser = reqparse.RequestParser()
upload_image_parser.add_argument('image',
                                 type=FileStorage,
                                 location='files',
                                 required=True,
                                 help='Image (max 10MB)')


# Background Removal Resource under the upload namespace
@api.route('/remove-background')
class RemoveBackground(Resource):
    @api.doc(description='Upload an image, remove its background, and get the processed image.')
    @api.expect(upload_image_parser)
    def post(self):
        """Handle the image upload and background removal"""
        request_params = upload_image_parser.parse_args(
        )  # Parse the incoming request arguments

        # Get the uploaded file
        image_file = request_params['image']
        if not image_file:
            return jsonify({"error": "No image file provided"}), 400

        # Create a temporary file to save the uploaded image
        with tempfile.NamedTemporaryFile(delete=False) as temp_input_file:
            temp_input_file.write(image_file.read())
            temp_input_path = temp_input_file.name

        try:
            # Create a temporary file for the output
            temp_output_file = tempfile.NamedTemporaryFile(
                delete=False, suffix='.png')
            temp_output_path = temp_output_file.name
            temp_output_file.close()

            # Use BackgroundRemover with the input and output file paths
            remover = BackgroundRemover(temp_input_path, temp_output_path)
            remover.remove_background()

            # Open the output file and send it as a response
            with open(temp_output_path, 'rb') as f:
                output_image = f.read()

            # Send the processed image as a downloadable file
            return send_file(BytesIO(output_image), as_attachment=True, download_name='processed_image.png',
                             mimetype='image/png')

        except Exception as e:
            return jsonify({"error": str(e)}), 500

        finally:
            # Clean up temporary files
            if os.path.exists(temp_input_path):
                os.remove(temp_input_path)
            if os.path.exists(temp_output_path):
                os.remove(temp_output_path)


# Define a parser for file upload
logo_upload_parser = reqparse.RequestParser()
logo_upload_parser.add_argument(
    'image', type=FileStorage, location='files', required=True, help='Image (max 10MB)')
logo_upload_parser.add_argument(
    'logo', type=FileStorage, location='files', required=True, help='Logo image (max 10MB)')
logo_upload_parser.add_argument(
    'position', type=str, location='args', required=False, default='top-right', choices=['top-left', 'top-right', 'bottom-left', 'bottom-right'], help='Position to place the logo')


@api.route('/add-logo')
class AddLogo(Resource):
    @api.doc(description='Upload an image and logo, add the logo to the image at a specified location.')
    @api.expect(logo_upload_parser)
    def post(self):
        """Handle the image and logo upload and add logo to image"""
        request_params = logo_upload_parser.parse_args(
        )  # Parse the incoming request arguments

        # Get the uploaded image, logo, and position
        image_file = request_params['image']
        logo_file = request_params['logo']
        position = request_params['position']
        if not image_file or not logo_file:
            return jsonify({"error": "No image or logo file provided"}), 400

        # Create temporary files to save the uploaded image and logo
        with tempfile.NamedTemporaryFile(delete=False) as temp_input_file:
            temp_input_file.write(image_file.read())
            temp_input_path = temp_input_file.name

        with tempfile.NamedTemporaryFile(delete=False) as temp_logo_file:
            temp_logo_file.write(logo_file.read())
            temp_logo_path = temp_logo_file.name

        try:
            # Create a temporary file for the output
            temp_output_file = tempfile.NamedTemporaryFile(
                delete=False, suffix='.png')
            temp_output_path = temp_output_file.name
            temp_output_file.close()

            # Use LogoAdder with the input, logo, and output file paths
            logo_adder = LogoAdder(
                temp_input_path, temp_logo_path, temp_output_path)
            # Use the position from the request to place the logo
            logo_adder.add_logo(location=position)

            # Open the output file and send it as a response
            with open(temp_output_path, 'rb') as f:
                output_image = f.read()

            # Send the processed image as a downloadable file
            return send_file(BytesIO(output_image), as_attachment=True, download_name='image_with_logo.png',
                             mimetype='image/png')

        except Exception as e:
            return jsonify({"error": str(e)}), 500

        finally:
            # Clean up temporary files
            if os.path.exists(temp_input_path):
                os.remove(temp_input_path)
            if os.path.exists(temp_logo_path):
                os.remove(temp_logo_path)
            if os.path.exists(temp_output_path):
                os.remove(temp_output_path)


# Define a parser for file upload
background_upload_parser = reqparse.RequestParser()
background_upload_parser.add_argument(
    'image', type=FileStorage, location='files', required=True, help='Image (max 10MB)')
background_upload_parser.add_argument(
    'background', type=FileStorage, location='files', required=True, help='Background image (max 10MB)')


@api.route('/apply-background')
class ApplyBackground(Resource):
    @api.doc(description='Upload an image (car without background) and a background image, apply the car on the background.')
    @api.expect(background_upload_parser)
    def post(self):
        """Handle the image and background upload and apply the car to the new background"""
        request_params = background_upload_parser.parse_args(
        )  # Parse the incoming request arguments

        # Get the uploaded image and background
        image_file = request_params['image']
        background_file = request_params['background']
        if not image_file or not background_file:
            return jsonify({"error": "No image or background file provided"}), 400

        # Create temporary files to save the uploaded image and background
        with tempfile.NamedTemporaryFile(delete=False) as temp_input_file:
            temp_input_file.write(image_file.read())
            temp_input_path = temp_input_file.name

        with tempfile.NamedTemporaryFile(delete=False) as temp_background_file:
            temp_background_file.write(background_file.read())
            temp_background_path = temp_background_file.name

        try:
            # Create a temporary file for the output
            temp_output_file = tempfile.NamedTemporaryFile(
                delete=False, suffix='.png')
            temp_output_path = temp_output_file.name
            temp_output_file.close()

            # Use BackgroundApplier with the car image and background file
            background_applier = BackgroundApplier(
                temp_input_path, temp_background_path, temp_output_path)
            background_applier.apply_background()

            # Open the output file and send it as a response
            with open(temp_output_path, 'rb') as f:
                output_image = f.read()

            # Send the processed image as a downloadable file
            return send_file(BytesIO(output_image), as_attachment=True, download_name='car_with_background.png',
                             mimetype='image/png')

        except Exception as e:
            return jsonify({"error": str(e)}), 500

        finally:
            # Clean up temporary files
            if os.path.exists(temp_input_path):
                os.remove(temp_input_path)
            if os.path.exists(temp_background_path):
                os.remove(temp_background_path)
            if os.path.exists(temp_output_path):
                os.remove(temp_output_path)


multi_upload_parser = reqparse.RequestParser()
multi_upload_parser.add_argument(
    'car_image', type=FileStorage, location='files', required=True, help='Car image (max 10MB)')
multi_upload_parser.add_argument(
    'logo', type=FileStorage, location='files', required=False, help='Logo image (max 10MB)')
multi_upload_parser.add_argument(
    'background', type=FileStorage, location='files', required=False, help='Background image (max 10MB)')
multi_upload_parser.add_argument(
    'logo_position', type=str, location='args', required=False, default='top-right', choices=['top-left', 'top-right', 'bottom-left', 'bottom-right'], help='Position to place the logo')

# Combined Process Resource under the upload namespace
@api.route('/process-car-image')
class ProcessCarImage(Resource):
    @api.doc(description='Upload a car image, optional logo, and optional background. The image is processed accordingly.')
    @api.expect(multi_upload_parser)
    def post(self):
        """Handle the upload of car image, logo, and background and process them accordingly"""
        request_params = multi_upload_parser.parse_args()  # Parse the incoming request arguments

        # Get the uploaded files
        car_image_file = request_params['car_image']
        logo_file = request_params['logo']
        background_file = request_params['background']
        logo_position = request_params['logo_position']

        if not car_image_file:
            return jsonify({"error": "Car image is required"}), 400

        # Create temporary files to save the uploaded car image, logo, and background
        with tempfile.NamedTemporaryFile(delete=False) as temp_car_file:
            temp_car_file.write(car_image_file.read())
            temp_car_path = temp_car_file.name

        temp_background_path = None
        temp_logo_path = None
        temp_output_path = None

        try:
            # Step 1: Remove the background from the car image
            temp_removed_bg_path = tempfile.NamedTemporaryFile(delete=False, suffix='.png').name
            remover = BackgroundRemover(temp_car_path, temp_removed_bg_path)
            remover.remove_background()

            # Step 2: If background is provided, apply it to the car image after background removal
            if background_file:
                with tempfile.NamedTemporaryFile(delete=False) as temp_background_file:
                    temp_background_file.write(background_file.read())
                    temp_background_path = temp_background_file.name

                # Create a temporary file for the output after applying the background
                temp_output_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
                temp_output_path = temp_output_file.name
                temp_output_file.close()

                # Use BackgroundApplier to apply the car image (without background) on the background
                background_applier = BackgroundApplier(temp_removed_bg_path, temp_background_path, temp_output_path)
                background_applier.apply_background()

                # Clean up temporary background file after processing
                if os.path.exists(temp_background_path):
                    os.remove(temp_background_path)
            else:
                # If no background is provided, use the car image after background removal
                temp_output_path = temp_removed_bg_path

            # Step 3: If logo is provided, add the logo to the car image (with background, if applied)
            if logo_file:
                with tempfile.NamedTemporaryFile(delete=False) as temp_logo_file:
                    temp_logo_file.write(logo_file.read())
                    temp_logo_path = temp_logo_file.name

                # Use LogoAdder to add the logo to the car image (with or without background)
                logo_adder = LogoAdder(temp_output_path, temp_logo_path, temp_output_path)
                logo_adder.add_logo(location=logo_position)

                # Clean up temporary logo file after processing
                if os.path.exists(temp_logo_path):
                    os.remove(temp_logo_path)

            # Read the final processed image and send it as a response
            with open(temp_output_path, 'rb') as f:
                output_image = f.read()

            # Send the processed image as a downloadable file
            return send_file(BytesIO(output_image), as_attachment=True, download_name='final_image.png',
                             mimetype='image/png')

        except Exception as e:
            return jsonify({"error": str(e)}), 500

        finally:
            # Clean up temporary files after all operations are done
            if os.path.exists(temp_car_path):
                os.remove(temp_car_path)
            if os.path.exists(temp_removed_bg_path):
                os.remove(temp_removed_bg_path)
            if os.path.exists(temp_output_path):
                os.remove(temp_output_path)