from flask import Flask
import os
import cv2
import pytesseract

app = Flask(__name__)

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\patzanov\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

@app.route('/')
def process_photos():
    photos_dir = 'photos'
    output_file = 'output.txt'
    text_data = []

    # Ensure the photos directory exists
    if not os.path.exists(photos_dir):
        return "Photos directory does not exist."

    # Read all files in the photos directory
    for filename in os.listdir(photos_dir):
        file_path = os.path.join(photos_dir, filename)
        if os.path.isfile(file_path):
            # Read the image using OpenCV
            image = cv2.imread(file_path)
            # Perform OCR using Tesseract
            text = pytesseract.image_to_string(image)
            text_data.append(f"Text from {filename}:\n{text}\n")

    # Write the extracted text to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(text_data)

    return f"App ausgeführt. Daten gespeichert unter: {os.path.abspath(output_file)}"

# filepath: /c:/Users/patzanov/Desktop/flask_app/app.py
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)