from flask import Flask, render_template_string
import os
import cv2
import pytesseract
import logging

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = (
    r'C:\Users\patzanov\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
)

@app.route('/')
def process_photos():
    photos_dir = 'photos'
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
                    logging.error(f"Error reading image {filename}")
                    continue

                # Perform OCR using Tesseract
                text = pytesseract.image_to_string(image)
                text_data.append(f"Text from {filename}:\n{text}\n")
            except Exception as e:
                logging.error(f"Error processing file {filename}: {e}")

    # Render the text data in the browser
    html_template = """
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <title>OCR Results</title>
      </head>
      <body>
        <h1>OCR Results</h1>
        <pre>{{ text_data }}</pre>
      </body>
    </html>
    """
    return render_template_string(html_template, text_data="\n".join(text_data))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)