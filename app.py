import os
import cv2
import numpy as np
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/')
def upload_form():
    return render_template('upload.html')


@app.route('/', methods=['POST'])
def upload_image():
    operation_selection = request.form['image_type_selection']
    image_file = request.files['file']
    filename = secure_filename(image_file.filename)
    reading_file_data = image_file.read()
    image_array = np.fromstring(reading_file_data, dtype='uint8')

    decode_array_to_img = cv2.imdecode(image_array, cv2.IMREAD_UNCHANGED)
    if operation_selection == 'gray': #Conditions to check user input:
        file_data = make_grayscale(decode_array_to_img) #If the condition becomes true then file_data holds the function which will get executed which is nothing but the converted image.
    elif operation_selection == 'sketch':
        file_data = image_sketch(decode_array_to_img)
    elif operation_selection == 'oil': 
        file_data = oil_effect(decode_array_to_img)
    elif operation_selection == 'rgb':
        file_data = rgb_effect(decode_array_to_img)
# Code start from below
    elif operation_selection == 'water':
        file_data = water_color_effect(decode_array_to_img) #decode_array_to_img variable holds the decoded image pixels which we want to convert
    elif operation_selection == 'invert':
        file_data = invert(decode_array_to_img) #268
    elif operation_selection == 'hdr':
        file_data = HDR(decode_array_to_img) #268
# Code ends 

    else:
        print('No image')

    with open(os.path.join('static/', filename),
                  'wb') as f:
        f.write(file_data)

    return render_template('upload.html', filename=filename)

def make_grayscale(decode_array_to_img):

    converted_gray_img = cv2.cvtColor(decode_array_to_img, cv2.COLOR_RGB2GRAY)
    status, output_image = cv2.imencode('.PNG', converted_gray_img)

    return output_image

def image_sketch(decode_array_to_img):

    converted_gray_img = cv2.cvtColor(decode_array_to_img, cv2.COLOR_BGR2GRAY)
    sharping_gray_img = cv2.bitwise_not(converted_gray_img)
    blur_img = cv2.GaussianBlur(sharping_gray_img, (111, 111), 0)
    sharping_blur_img = cv2.bitwise_not(blur_img)
    sketch_img = cv2.divide(converted_gray_img, sharping_blur_img, scale=256.0)
    status, output_img = cv2.imencode('.PNG', sketch_img)

    return output_img

def oil_effect(decode_array_to_img): #267.  applying oil painting effects on uploaded image.
    oil_effect_img = cv2.xphoto.oilPainting(decode_array_to_img, 7, 1)
    status, output_img = cv2.imencode('.PNG', oil_effect_img)

    return output_img

def rgb_effect(decode_array_to_img): #changing the color pixels of the original image into RGB format.
    rgb_effect_img = cv2.cvtColor(decode_array_to_img, cv2.COLOR_RGB2BGR)
    status, output_img = cv2.imencode('.PNG', rgb_effect_img)

    return output_img
# Codes starts from below
def water_color_effect(decode_array_to_img): #To achieve Water Paint effect we need to add 3 times more color pixel value as of original color pixel value
    water_effect = cv2.stylization(decode_array_to_img, sigma_s=60, sigma_r=0.6) #stylization function of the cv2 library will be used to convert the uploaded image into an Water paint image.sigma_s is nothing but smoothness which applies to water color effects.sigma_r is an adjustment color combination in water color effect so which can see the image as water paint.
    status, output_img = cv2.imencode('.PNG', water_effect) #encode the converted Water effect image so that the image will be at its original format which means its original height and width
#status is the parameter which gives the output as boolean value i.e True or False. If the image gets successfully converted then the output will be True or else the output value will be False.
    return output_img #return the converted image as output which will be displayed on webportal.

def invert(decode_array_to_img):#Inverted image is nothing but the reverse of the colors of image, where red color is reversed to cyan, green reversed to magenta and blue reversed to yellow, and vice versa.
    invert_effect = cv2.bitwise_not(decode_array_to_img) #This function is used to convert the color of an image from one type to another type
    status, output_img = cv2.imencode('.PNG', invert_effect)

    return output_img

def HDR(decode_array_to_img): # HDR effect is nothing but enhancing detailing of the image.HDR is nothing but High dynamic range which highly used in photography and videography
    hdr_effect = cv2.detailEnhance(decode_array_to_img, sigma_s=12, sigma_r=0.15) #This function is used to add details and enhance the quality of the image. sigma_s is nothing but smoothness which applies on HDR color effects. sigma_r is an adjustment color combination in HDR color effect so which can see the image as HDR effects.
    status, output_img = cv2.imencode('.PNG', hdr_effect)

    return output_img
# Code ends


@app.route('/display/<filename>')
def display_image(filename):

    return redirect(url_for('static', filename=filename))



if __name__ == "__main__":
    app.run()
