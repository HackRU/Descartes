import cv2
import numpy as np
from PIL import ImageEnhance



def parse():

    img_file = 'C:/test_cases/nice.jpg' # load the image
    o_img = cv2.cvtColor(cv2.imread(img_file), cv2.COLOR_BGR2GRAY) # convert to grayscale
    o_rows, o_cols = o_img.shape # original image height and width
    new_size_pixels = 500
    c_r_aspect = o_cols / o_rows

    if o_rows > o_cols:  # this if/else basically resizes images down in case they are super big
        image = cv2.resize(o_img, (int(c_r_aspect * new_size_pixels), new_size_pixels))
    else:
        r_c_aspect = 1/c_r_aspect
        image = cv2.resize(o_img, (new_size_pixels, int(r_c_aspect*new_size_pixels)))

    rows, cols = image.shape  # rows = height of image; cols = width of image

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
    parse()
