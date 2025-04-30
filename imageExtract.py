# -*- coding: utf-8 -*-
"""
Created on Tue Apr 29 15:48:05 2025

@author: srava
"""

import os
from PIL import Image, ImageEnhance, ImageOps
import pytesseract
import re
import csv

# Specify the Tesseract.exe path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Initialize a list to store the extracted data
data = []

# Initialize the CSV header
header = ["FileName", "Place", "Latitude", "Longitude", "Timestamp"]

def crop_bottom(img, fraction=0.25):
    w, h = img.size
    return img.crop((0, int(h * (1 - fraction)), w, h))

#specify the folder where images are saved
folder_path = r"D:\EarthAnalytics\LacunaImageExtract"

for filename in os.listdir(folder_path):
    if filename.lower().endswith((".jpg", ".png", ".jpeg")):
        image_path = os.path.join(folder_path, filename)
        img = Image.open(image_path)
        img = crop_bottom(img)

        img = img.convert('L')
        img = ImageEnhance.Contrast(img).enhance(2.0)
        img = img.point(lambda x: 0 if x < 150 else 255, '1')
        img = ImageOps.invert(img.convert('L'))

        text = pytesseract.image_to_string(img, config='--psm 6')

        place_match = re.search(r'([A-Z][a-z]+(?:,?\s*[A-Z][a-z]+)*,\s*India)', text)
        lat_match = re.search(r'Lat\s*([\d\.]+[°]?)', text, re.IGNORECASE)
        lon_match = re.search(r'Long\s*([\d\.]+[°]?)', text, re.IGNORECASE)
        timestamp_match = re.search(r'\d{2}/\d{2}/\d{4}\s+\d{1,2}:\d{2}\s*(?:AM|PM)?\s*GMT\s*[+-]\d{2}:\d{2}', text, re.IGNORECASE)
        
        place = place_match.group(1) if place_match else 'Not found'
        latitude = lat_match.group(1) if lat_match else 'Not found'
        longitude = lon_match.group(1) if lon_match else 'Not found'
        timestamp = timestamp_match.group(0) if timestamp_match else 'Not found'
            
        print(f"\n🖼️ File: {filename}")
        print(f"Place: {place_match.group(1) if place_match else 'Not found'}")
        print(f"Latitude: {lat_match.group(1) if lat_match else 'Not found'}")
        print(f"Longitude: {lon_match.group(1) if lon_match else 'Not found'}")
        print(f"Timestamp: {timestamp_match.group(0) if timestamp_match else 'Not found'}")

        # Append the extracted data to the list
        data.append([filename, place, latitude, longitude, timestamp])


# After the loop, write the data to a CSV file
csv_file = "extracted_data.csv"

with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)  # Write the header
    writer.writerows(data)   # Write the extracted data

print(f"Data has been written to {csv_file}")



"""
# Providing the tesseract executable 
# location to pytesseract library 
pytesseract.tesseract_cmd = path_to_tesseract 
# configurations
config = ('-l eng --oem 1 --psm 3')
# Passing the image object to image_to_string() function 
# This function will extract the text from the image 
text = pytesseract.image_to_string(img,config=config) 
 
# Displaying the extracted text 
print(text.strip())"""
