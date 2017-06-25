import cv2
import numpy as np
from flask import Flask, request
from PIL import ImageEnhance

app = Flask(__name__)



@app.route("/upload", methods=['POST'])
def image_upload():
    if request.method == 'GET':
        return 'not the right method'

    return 'nice.'


def parse():

    img_file = 'test_cases/foo.jpg' # load the image

    # o_img = cv2.imread(img_file)
    o_img = cv2.cvtColor(cv2.imread(img_file), cv2.COLOR_BGR2GRAY) # convert to grayscale
    o_rows, o_cols = o_img.shape

    if o_rows > o_cols:
        c_r_aspect = o_cols / o_rows
        NEW_ROWS = 500
        image = cv2.resize(o_img, (int(c_r_aspect * NEW_ROWS), NEW_ROWS))
    else:
        r_c_aspect = o_rows / o_cols
        NEW_COLS = 500
        image = cv2.resize(o_img, (NEW_COLS, int(r_c_aspect*NEW_COLS)))

    rows, cols = image.shape

    print('img rows: {}, img width: {}'.format(rows, cols))

    list_of_sections = []
    start = False
    for r in range(rows):
        min_so_far = 255
        for c in range(cols):
            if image[r, c] < min_so_far:
                min_so_far = image[r, c]

        if min_so_far < 50 and not start:
            start = True
            start_r = r
        elif min_so_far > 50 and start and r - start_r > 30:
            start = False
            end_r = r
            list_of_sections.append({'start': start_r-10, 'end': end_r+10})
        else:
            pass

    list_of_img_dicts = []

    for img_num, line in enumerate(list_of_sections):
        # cv2.line(image, (0, line['start']), (cols, line['start']), (0, 0, 0), thickness=1)
        # cv2.line(image, (0, line['end']), (cols, line['end']), (0, 0, 0), thickness=1)
        # print(line['start'], line['end'])
        crop_img = image[line['start']:line['end'], 0:cols]
        list_of_img_dicts.append({'img': crop_img, 'indents': 0})


    for img_num, img in enumerate(list_of_img_dicts):  # loop through to pass to azure
        cv2.imshow('img {}'.format(img_num), img['img'])


        # cv2.imwrite('{}.jpg'.format(img_num), crop_img)



    # avg_shades_of_rows = np.average(image, axis=0)
    # avg_img_shade = np.average(avg_shades_of_rows, axis=0)
    # print('avg shade of image: {}'.format(avg_img_shade))

    # avg_shades = []
    # for r in range(rows):
    #     sum_shade_of_row = 0
    #     for c in range(cols):
    #         sum_shade_of_row += image[r,c]
    #     avg_shade_of_row = sum_shade_of_row / cols
    #     avg_shades.append(avg_shade_of_row)
    #
    # avg_shade = sum(avg_shades)/len(avg_shades)
    # print(avg_shade)

    # list_of_sections = []
    # start = False
    # for r in range(rows):
    #     avg_shade_of_row = avg_shades[r]
    #     if avg_shade_of_row < avg_shade and not start:
    #         start = True
    #         start_r = r
    #     elif avg_shade_of_row > avg_shade and start:
    #         start = False
    #         end_r = r
    #         list_of_sections.append({'start': start_r-10, 'end': end_r+10})
    #     else:
    #         pass


    #
    # print(list_of_sections)
    # for line in list_of_sections:
    #     cv2.line(image, (0, line['start']), (cols, line['start']), (0, 0, 0), thickness=1)
    #     cv2.line(image, (0, line['end']), (cols, line['end']), (0, 0, 0), thickness=1)

    cv2.imshow('', np.asarray(image))
    cv2.imwrite('nice.jpg', image)

    cv2.waitKey()

    return






if __name__ == '__main__':
    # app.run()
    parse()

# def parser(image_link, web=False):
#     if web:  # if web is True, the image link is a web resource, so we need to download it first
#
#         # download the image from the corresponding link and save it as a temp file
#     else:

#
# try:
#     import Image
# except ImportError:
#     from PIL import Image
# import pytesseract
#
# # pytesseract.pytesseract.tesseract_cmd = '<full_path_to_your_tesseract_executable>'
# # Include the above line, if you don't have tesseract executable in your PATH
# # Example tesseract_cmd: 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'
#
# print(pytesseract.image_to_string(Image.open('test_cases/function.jpg')))
