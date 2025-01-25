from flask import Flask
import os
import cv2
import pytesseract
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\patzanov\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

@app.route('/')
def process_photos():
    photos_dir = 'Photos'
    output_file = 'output.txt'
    text_data = []

    # Ensure the photos directory exists
    if not os.path.exists(photos_dir):
        logging.error("Photos directory does not exist.")
        return "Photos directory does not exist."

    # Read all files in the photos directory
    for filename in os.listdir(photos_dir):
        file_path = os.path.join(photos_dir, filename)
        if os.path.isfile(file_path):
            try:
                # Read the image using OpenCV
                image = cv2.imread(file_path)

                # Check if the image is read correctly
                if image is None:
                    logging.warning(f"Could not read image {filename}")
                    text_data.append(f"Could not read image {filename}\n")
                    continue

                # Perform OCR using Tesseract
                text = pytesseract.image_to_string(image)
                text_data.append(f"Text from {filename}:\n{text}\n")
            except Exception as e:
                logging.error(f"Error processing {filename}: {e}")
                text_data.append(f"Error processing {filename}: {e}\n")

    # Write the extracted text to the output file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.writelines(text_data)
    except Exception as e:
        logging.error(f"Error writing to output file: {e}")
        return f"Error writing to output file: {e}"

    logging.info(f"App executed. Data saved to: {os.path.abspath(output_file)}")
    return f"App executed. Data saved to: {os.path.abspath(output_file)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
