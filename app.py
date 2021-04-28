
import cv2 #for image processing
import flask

from flask import Flask
from flask import request, jsonify
import numpy as np
import base64
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

def cartoonify(img):
    if img is None:
        print("Can not find any image. Choose appropriate file")
        sys.exit()
    
    # read the image
    img = cv2.imdecode(img, cv2.IMREAD_UNCHANGED)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    

    gray_img= cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    smooth_gray_img = cv2.medianBlur(gray_img, 5)

    edge_img = cv2.adaptiveThreshold(smooth_gray_img, 255, 
        cv2.ADAPTIVE_THRESH_MEAN_C, 
        cv2.THRESH_BINARY, 9, 9)

    color_img = cv2.bilateralFilter(img, 9, 300, 300)

    #masking edged image with our "BEAUTIFY" image
    cartoon_img = cv2.bitwise_and(color_img, color_img, mask=edge_img)
    cv2.imshow('image',cartoon_img)
    cv2.waitKey(0)
    return cartoon_img


@app.route('/', methods=['POST', 'GET'])
def index():
    imgstr = request.args.get('image')
    imgstr = imgstr.replace(' ', '+')
    imgdata = base64.b64decode(imgstr, '-_')
    
    # img = np.fromstring(request.args.get('image'), np.uint8)
    cartoon_img = cartoonify(np.fromstring(imgdata, np.uint8))

    retval, cartoon_img = cv2.imencode('.jpg', cartoon_img)
    return_image = base64.b64encode(cartoon_img)
    return_image = return_image.decode()

    
    # response = flask.make_response(str(cartoon_img))
    # response.headers.set('Content-Type', '')
    # response.headers.set(
    #     'Content-Disposition', 'attachment', filename='%s.jpg' )
    return json.dumps({'image': str(return_image)})
    
    


if __name__ == "__main__":
    app.run(debug=True, port=80)
