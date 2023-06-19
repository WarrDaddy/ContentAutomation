import os
import json
from google.cloud import vision_v1p3beta1 as vision

# Path to the configuration file
config_path = 'config_vision_ai.json'

# Load or initialize configuration
if os.path.exists(config_path):
    with open(config_path, 'r') as file:
        config = json.load(file)
else:
    config = {
        'credentials_path': input("Enter the path to your Google Cloud Vision API credentials JSON file: "),
        'folder_path': input("Enter the path to the folder containing the images: ")
    }
    with open(config_path, 'w') as file:
        json.dump(config, file)

# Validate that the provided paths exist
assert os.path.exists(config['credentials_path']), "The provided Google Cloud Vision API credentials file does not exist."
assert os.path.exists(config['folder_path']), "The provided folder does not exist."

# Initialize the client
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = config['credentials_path']
client = vision.ImageAnnotatorClient()

# Function to extract text from an image using Google Cloud Vision API
def extract_text_from_image(image_path):
    # Open the image file
    with open(image_path, 'rb') as img:
        # Read the image as bytes
        image_bytes = img.read()

    # Create an image instance
    image = vision.Image(content=image_bytes)

    # Perform text detection
    response = client.text_detection(image=image)
    annotations = response.text_annotations

    # Extract the text
    if annotations:
        return annotations[0].description

    return ''

# Create an output folder if it doesn't exist
output_folder = 'Image-Extration-Output'
os.makedirs(output_folder, exist_ok=True)

# Iterate over all the files in the folder
for filename in os.listdir(config['folder_path']):
    # Full path to the image file
    image_path = os.path.join(config['folder_path'], filename)

    # Check if the file is an image
    if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.jpeg'):
        # Extract text from the image
        extracted_text = extract_text_from_image(image_path)

        # Output file path for the current image
        output_file = os.path.join(output_folder, f'{os.path.splitext(filename)[0]}.txt')

        # Write the extracted text to the output file
        with open(output_file, 'w') as file:
            file.write(extracted_text if extracted_text else '')

        print(f'Text extracted from {filename} and saved to {output_file}.')
