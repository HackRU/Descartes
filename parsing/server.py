import cv2
import numpy as np
from flask import Flask, request, json, send_from_directory
from PIL import ImageEnhance
import os

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


@app.route("/img/<num>", methods=['GET'])
def img(num):
    return send_from_directory('dump', 'img-{}.jpg'.format(num))


if __name__ == '__main__':
    app.run()
