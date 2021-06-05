from flask import Flask,request, url_for, redirect, render_template,jsonify
import pickle
import numpy as np
import tensorflow_hub as hub
from flask import Flask, render_template, request
from time import sleep
from datetime import date
from tensorflow.keras.models import load_model

app = Flask(__name__)


 
@app.route('/')
def Home():
    return render_template("index.html")
	
@app.route('/index.html')
def Home_():
    return render_template("index.html")

@app.route('/classify.html')
def Classify():
	return render_template("classify.html")

@app.route('/home',methods=['POST','GET','PUT'])
def predict():
	if request.method == 'PUT'or request.method =="POST":
		f = request.files['file']
		f.save('Test'+'//'+"upload.png")
		sleep(2.1)
	model = load_model('model.h5')
	import tensorflow as tf
	from tensorflow.keras.preprocessing import image
	from tensorflow.keras.optimizers import RMSprop
	from tensorflow.keras.preprocessing.image import ImageDataGenerator
	import cv2
	import matplotlib.pyplot as plt
	import os
	import numpy as np
	import pickle
	
	dir_path = 'Test'
	today = date.today()
	for i in os.listdir(dir_path):
		img = image.load_img(dir_path+'//'+ i,target_size=(500,500),color_mode='grayscale')    
		X = image.img_to_array(img)
		X = X/255
		X = np.expand_dims(X,axis = 0)
		val = model.predict(X)
		p = val[0][0]
		p = p*100
		if val<0.5:
			if request.method == 'PUT':
				return jsonify(output="Normal")
			else:
				return render_template('Result.html',pred='Normal',acc=round((1-p)*100,2),dd=today)
			
		else:
			if request.method == 'PUT':
				return jsonify(output="tuberculosis")
			else:
				return render_template('Result.html',pred='TuberCulosis',acc=round(p,2),dd=today)
			
      

if __name__ == '__main__':
    app.run(debug=True,host='127.0.0.1',port=80)
   # app.run(debug=True)
    