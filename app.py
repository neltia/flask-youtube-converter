from flask import Flask
from flask import render_template
from flask import request
from flask import send_file

try:
	from werkzeug.utils import secure_filename
except:
	from werkzeug import secure_filename

from selenium import webdriver
from pytube import YouTube
import glob
import os
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import lxml
import shutil

app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(error):
	app.logger.error(error)
	return render_template('page_not_found.html'), 404

@app.route('/')
@app.route('/page')
def input_page():
	return render_template('home.html')

@app.route('/fileDown', methods = ['GET', 'POST'])
def down_file():
	if request.method == 'POST':
		video_url = request.form['urlname']
		yt = YouTube(video_url)
		yt.streams.filter(only_audio=True).first().download()

		req = requests.get(video_url)
		soup = BeautifulSoup(req.text, 'html.parser')
		title = str(soup.select('div.watch-main-col')[0].meta.get('content'))

		files = glob.glob("*.mp4")
		for x in files:
			if not os.path.isdir(x):
				filename = os.path.splitext(x)
				try:
					tmp = title + "_" + datetime.today().strftime("%y-%m-%d") + '.mp3'
					os.rename(x,tmp)
					shutil.move("./" + tmp, "./uploads/" + tmp)
					
					return send_file("./uploads/" + tmp,
						attachment_filename = tmp,
						as_attachment=True)
				except Exception as e:
					print(e)
					pass
	else:
		return render_template('page_not_found.html')

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug = True)