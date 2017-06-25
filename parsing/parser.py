#
#
#
#
# def parser(image_link, web=False):
#     if web:  # if web is True, the image link is a web resource, so we need to download it first
#
#         # download the image from the corresponding link and save it as a temp file
#     else:
#
#
#
#
#
#
#
#
#
#
#
#
#
# if __name__ == '__main__':
#     parser('test_cases/img-001.jpg')




try:
    import Image
except ImportError:
    from PIL import Image
import pytesseract

# pytesseract.pytesseract.tesseract_cmd = '<full_path_to_your_tesseract_executable>'
# Include the above line, if you don't have tesseract executable in your PATH
# Example tesseract_cmd: 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'

print(pytesseract.image_to_string(Image.open('test_cases/function.jpg')))
