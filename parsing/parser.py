import cv2
import numpy as np
from flask import Flask, request, json
from PIL import ImageEnhance
import os
import http.client, urllib.request, urllib.parse, urllib.error, base64, requests, time, json
from imgurpython import ImgurClient

client_id = 'd18cea4af0b4c75'
client_secret = 'e0dd972784aab4b0b4d39156f982d55c29b4d3b3'

AZURE_SUB_KEY = '99894b2c78f144ca80dc013e744a8da2'
AZURE_REQ_HEADERS = {
    # Request headers.
    # Another valid content type is "application/octet-stream".
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': AZURE_SUB_KEY,
}

imgur_client = ImgurClient(client_id, client_secret)

app = Flask(__name__)


@app.route("/")
def index():
    return 'HOME PAGE DUDE.'


@app.route("/upload", methods=['POST'])
def upload():
    image_file = request.data
    with open('../dump/temp.jpg', 'wb') as f:
        f.write(image_file)
    f.close()

    response = app.response_class(
        response=json.dumps('received ur img! thx.'),
        status=200,
        mimetype='html/text'
    )

    parse()
    return response


def parse():
    img_file = '../dump/temp.jpg'  # load the image
    o_img = cv2.cvtColor(cv2.imread(img_file), cv2.COLOR_BGR2GRAY)  # convert to grayscale
    o_rows, o_cols = o_img.shape  # original image height and width
    new_size_pixels = 500
    c_r_aspect = o_cols / o_rows

    if o_rows > o_cols:  # this if/else basically resizes images down in case they are super big
        image = cv2.resize(o_img, (int(c_r_aspect * new_size_pixels), new_size_pixels))
    else:
        r_c_aspect = 1 / c_r_aspect
        image = cv2.resize(o_img, (new_size_pixels, int(r_c_aspect * new_size_pixels)))

    rows, cols = image.shape  # rows = height of image; cols = width of image

    list_of_sections = []
    start = False
    for r in range(rows):
        min_so_far = 255
        for c in range(cols):
            if image[r, c] < min_so_far:
                min_so_far = image[r, c]

        if min_so_far < 100 and not start:
            start = True
            start_r = r
        elif min_so_far > 100 and start and r - start_r > 30:
            start = False
            end_r = r
            list_of_sections.append({'start': start_r - 10, 'end': end_r + 10})
        else:
            pass

    list_of_img_dicts = []

    for img_num, line in enumerate(list_of_sections):
        # cv2.line(image, (0, line['start']), (cols, line['start']), (0, 0, 0), thickness=1)
        # cv2.line(image, (0, line['end']), (cols, line['end']), (0, 0, 0), thickness=1)
        crop_img = image[line['start']:line['end'], 0:cols]
        list_of_img_dicts.append({'img': crop_img, 'indents': 0})

    # last_indent_pos = 0
    last_indent = 0
    indent_gap = 0 # number of pixels per indent
    code_start_pos = -1

    for img_num, img in enumerate(list_of_img_dicts):  # loop through to pass to azure
        transposed = img['img'].T
        hit_text = False
        for c_num, col in enumerate(transposed):
            if not hit_text:
                for row in col:
                    if row < 100 and not hit_text: # less than shade of 100
                        hit_text = True

                        if code_start_pos == -1:  # set code start
                            code_start_pos = c_num
                            img['indents'] = 0
                        else:
                            diff = abs(c_num - code_start_pos)
                            if indent_gap == 0: # set the initial indent gap
                                indent_gap = diff

                            print(diff, indent_gap)

                            if diff//indent_gap - last_indent > 1:
                                img['indents'] = last_indent+1
                            else:
                                img['indents'] = diff//indent_gap

                        last_indent = img['indents']
                    else:
                        pass
            else:
                break


        print('img-{}'.format(img_num), img['indents'])

        cv2.imshow('img-{}'.format(img_num), img['img'])
        cv2.imwrite('../dump/img-{}.jpg'.format(img_num), img['img'])

        # r = imgur_client.upload_from_path('../dump/img-{}.jpg'.format(img_num))
        # link_to_img = r['link']

        img['op_loc'] = send_to_azure('http://34.225.118.123:8080/img/img-{}.jpg'.format(img_num))


    print('All images sent to Azure. Waiting 10 seconds for processing.')
    time.sleep(10)

    # after this point, all processing should be complete for every picture we sent above
    # use the op locs and loop through to retrieve data from their server

    for img in list_of_img_dicts:
        # Execute the second REST API call and get the response.
        response = requests.request('GET', img['op_loc'], json=None, data=None, headers=AZURE_REQ_HEADERS, params=None)
        # 'data' contains the JSON data. The following formats the JSON data for display.
        parsed = json.loads(response.text)
        text_lines = parsed['recognitionResult']['lines']
        # print(parsed)

        actual_line = ''
        for line in text_lines:
            actual_line += (line['text'] + ' ')

        img['parsed'] = actual_line

        for _ in range(img['indents']):
            print('\t',end='')

        print(img['parsed'])
        # print(json.dumps(parsed, sort_keys=True, indent=2))

    cv2.imshow('', np.asarray(image))
    cv2.waitKey()

    return


def send_to_azure(i_link):
    ###############################################
    #### Update or verify the following values. ###
    ###############################################

    uri_base = 'https://westus.api.cognitive.microsoft.com'

    # The URL of a JPEG image containing handwritten text.
    body = {'url': i_link}
    # For printed text, set "handwriting" to false.
    params = {'handwriting': 'true'}

    try:
        # This operation requrires two REST API calls. One to submit the image for processing,
        # the other to retrieve the text found in the image.
        #
        # This executes the first REST API call and gets the response.
        response = requests.request('POST', uri_base + '/vision/v1.0/RecognizeText', json=body, data=None,
                                    headers=AZURE_REQ_HEADERS, params=params)

        # Success is indicated by a status of 202.
        if response.status_code != 202:
            # if the first REST API call was not successful, display JSON data and exit.
            parsed = json.loads(response.text)
            print("Error:")
            print(json.dumps(parsed, sort_keys=True, indent=2))
            exit()

        # The 'Operation-Location' in the response contains the URI to retrieve the recognized text.
        operationLocation = response.headers['Operation-Location']

        # Note: The response may not be immediately available. Handwriting recognition is an
        # async operation that can take a variable amount of time depending on the length
        # of the text you want to recognize. You may need to wait or retry this GET operation.

        return operationLocation

    except Exception as e:
        print('Error:')
        print(e)

        ####################################


if __name__ == '__main__':
    parse()
    # app.run()
