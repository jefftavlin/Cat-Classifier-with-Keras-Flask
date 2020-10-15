from flask import Flask, escape, request, render_template, url_for,redirect
from flask import send_from_directory
from werkzeug.utils import secure_filename
import os
from tensorflow.keras.models import load_model
import glob
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
import shutil
import pandas as pd
import numpy as np

upload_folder = 'C:\\Users\\jeffr\\Python\\Projects\\Deep Learning\\Cat Classifier\\upload'
deep_image = 'C:\\Users\\jeffr\\Python\\Projects\\Deep Learning\\Cat Classifier\\static\\deep.png'
upload_image = 'C:\\Users\\jeffr\\Python\\Projects\\Deep Learning\\Cat Classifier\\upload\\deep.png'
static_folder = 'C:\\Users\\jeffr\\Python\\Projects\\Deep Learning\\Cat Classifier\\static'

model_path = 'C:\\Users\\jeffr\\Python\\Projects\\Deep Learning\\Cat Classifier\\model\\cats_dogsv2.h5'
model = load_model(model_path)

try:
	os.remove(deep_image)
	os.remove(upload_image)
except FileNotFoundError:
	pass

app = Flask(__name__) #special variable in python

def predict(uploaded_file):
	img  = load_img(uploaded_file, target_size=(150,150))
	img = img_to_array(img)/255.0
	img = np.expand_dims(img, axis=0)
	prediction = model.predict(img)[0]
	output = {'Cat:': prediction[0], 'Dog': prediction[1]}
	return output

@app.route('/') # add functionality to existing functions. Decorator. Home page
def home():
    return render_template('home.html') # h1 header tags

@app.route('/', methods=['GET','POST'])
def upload_file():
	if request.method == 'POST':
		for uploaded_file in request.files.getlist('file'):
		    uploaded_file = request.files['file']
		    if uploaded_file.filename != '':
		    	uploaded_file.save(uploaded_file.filename)
		    	shutil.move(uploaded_file.filename, 'deep.png')
		    	shutil.copy('deep.png',static_folder)
		    	shutil.copy('deep.png',upload_folder)
		    return redirect(url_for('home'))

@app.route('/upload')
def upload():
	output = predict(upload_image)
	lst = list(output.values())
	if lst[0] > lst[1]:
		label_output = 'Cat'
	else:
		label_output ='Dog'
	return render_template('upload.html', label = label_output, data = output)

if __name__ == '__main__':
    app.run(debug = True,threaded = False)