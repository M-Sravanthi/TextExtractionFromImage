# TextExtractionFromImage

This code extracts text information from a jpg, png or jpeg images captures by GPS camera.

1. First download and install the tesseract-OCR file from https://github.com/UB-Mannheim/tesseract/wiki
2. After installation, specify the path to tesseract.exe in the code. 
3. Specifty the path to saved images in the code.
4. The code assumes the text information is in the bottom 25% of the image and hence first crops the image to that and then searches for the text using regex expressions. Modify for other images accordingly.
