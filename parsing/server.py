import cv2
import numpy as np
from flask import Flask, request, json
from PIL import ImageEnhance
import os


app = Flask(__name__)


@app.route("/")
def index():
    return 'HOME PAGE DUDE.'

@app.route("/upload", methods=['POST'])
def upload():

    image_file = request.data
    print(image_file)
    print(type(image_file))
    with open('test_cases/temp.jpg', 'wb') as f:
        f.write(image_file)
    f.close()

    response = app.response_class(
        response=json.dumps('received ur img! thx.'),
        status=200,
        mimetype='html/text'
    )

    parser('')
    return response

if __name__ == '__main__':
    app.run()
