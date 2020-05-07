import time
import cv2
import os
import threading
from flask import render_template, Response, send_file, redirect, url_for, flash
from cyphersecuritycamera import app
from cyphersecuritycamera import socketio
from cyphersecuritycamera.Databases.Matches_History import MatchesHistory
from cyphersecuritycamera.Databases.face_encodings_database import FaceEncodingsDatabase
from cyphersecuritycamera.Databases.Database_Coms import DatabaseComs
from cyphersecuritycamera.Databases.settings import settings as settingsManager
from flask_thumbnails import Thumbnail
from cyphersecuritycamera.Frontend.forms import SettingsForm
from cyphersecuritycamera.Frontend.forms import CurSettings
from cyphersecuritycamera.Frontend.forms import ChangeEncodingNameForm
from cyphersecuritycamera.Frontend.forms import CurEncodingName
from cyphersecuritycamera.Camera.VideoController import Video_Controller
from cyphersecuritycamera.Detectors.noise_detector import Noise_Detector

thumb = Thumbnail(app)



DatabaseComs = DatabaseComs()
SettingsManager = settingsManager()
DatabaseComs.init_db_tables()
SettingsManager.init_settings_table()

archive_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'archive')

# Setup detectors
nd = Noise_Detector()
nd.start()

# md = Motion_Detector(do_display=False)
# md.start()

vc = Video_Controller()

matches_db = MatchesHistory()
face_encodings_db = FaceEncodingsDatabase()


@app.route('/home')
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/live')
def live():
	return render_template('live.html')

@app.route('/videostream')
def videostream():
	def gen_video():
		while True:
			frame = vc.get_processed_frame()
			(flag, encodedImage) = cv2.imencode(".jpg", frame)
			if encodedImage is not None:
				yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
					   bytearray(encodedImage.tobytes()) + b'\r\n')

	return Response(
		gen_video(),
		mimetype='multipart/x-mixed-replace; boundary=frame'
	)

@app.route('/archive')
def archive():
	return render_template('archive.html')

@app.route('/settings', methods=['GET', 'POST'])
def settings():
	curSettings = CurSettings()
	curSettings.update_settings()
	form = SettingsForm(obj=curSettings)

	if form.validate_on_submit():

		SettingsManager.change_setting(str(form.duplicate_interval_second.data), 1)
		SettingsManager.change_setting(str(form.detection_interval_second.data), 2)
		SettingsManager.change_setting(str(int(form.drawbox.data)), 6)
		flash(f'Changes saved!', 'success')

	return render_template('settings.html', title='Settings', form=form)

@app.route('/matcheshistory')
def matcheshistory():
	return render_template('matcheshistory.html')

@app.route('/encodings')
def encodings():
	return render_template('encodings.html')

@app.route('/archive/<string:filename>')
def archive_item(filename):
	name, extension = os.path.splitext(filename)
	type = get_type(filename)
	return render_template('record.html', filename=filename, type=type)

@app.route('/archive/delete/<string:filename>')
def archive_delete(filename):
	os.remove(archive_path + "/" + filename)
	return redirect(url_for('archive'))

@app.route('/archive/play/<string:filename>')
def archive_play(filename):
	return send_file('archive/' + filename)

@app.route('/thumbnails/<string:filename>')
def get_thumbnail(filename):
	return send_file('Databases/TicketImages/' + filename + '.png')

@app.route('/thumbnails/delete/<string:ticket_id>')
def delete_thumbnail(ticket_id):
	matches_db.delete_ticket(ticket_id)
	os.remove("cyphersecuritycamera/Databases/TicketImages/" + ticket_id + '.png')
	return redirect(url_for('matcheshistory'))

@app.route('/encoding/<string:filename>')
def get_endcoding_thumbnail(filename):
	return send_file('Databases/encodingsImages/' + filename + '.png')

@app.route('/encoding/delete/<string:encoding_id>')
def delete_encoding(encoding_id):
	face_encodings_db.delete_encoding_by_id(int(encoding_id))
	os.remove("cyphersecuritycamera/Databases/encodingsImages/" + encoding_id + '.png')
	return redirect(url_for('encodings'))


@app.route('/encoding/update/<string:encoding_id>', methods=['GET', 'POST'])
def change_encoding_name(encoding_id):
	name = face_encodings_db.get_name_by_id(int(encoding_id))
	curName = CurEncodingName()
	curName.set_name_id(name, encoding_id)
	form = ChangeEncodingNameForm(obj=curName)
	form.name.label = encoding_id
	if form.validate_on_submit():
		face_encodings_db.change_name_by_id(encoding_id, form.name.data)
		flash(f'Changes saved!', 'success')
		return redirect(url_for('encodings'))
	return render_template('changeencoding.html', title='Encodings', form=form)


@app.route('/thumbnails/logo/get')
def get_logo():
	return send_file('static\Images\Logo.png')

@socketio.on('connect')
def connect():
	print('Client connected')

@socketio.on('disconnect')
def disconnect():
	print('Client disconnected')

class Stream_Thread(threading.Thread):
	def __init__(self):
		self.delay = 1
		super(Stream_Thread, self).__init__()

	def run(self):
		while True:
			frame = vc.get_processed_frame()
			sound = nd.get_chunk()
			socketio.emit('sound', {'chunk': sound})
			time.sleep(0.05)

t = Stream_Thread()
t.start()

def get_type(filename):
	name, extension = os.path.splitext(filename)
	return 'video' if extension == '.mp4' else 'audio'

def get_records():
	records = []

	for filename in sorted(os.listdir(archive_path), reverse=True):
		if not filename.startswith('.'):
			type = get_type(filename)
			size = byte_to_mb(os.path.getsize(archive_path + "/" + filename))
			record = {"filename": filename, 'size': size, 'type': type}
			records.append(record)

	return records

def get_encodings():
	encodings = []

	for encoding in face_encodings_db.get_all_encodings():
		matches_db.get_image_by_id(encoding[0])
		encoding_d = {"id": encoding[0], "name": encoding[1]}
		encodings.append(encoding_d)
	return encodings[::-1]

def get_match_tickets():
	tickets = []

	for ticket in matches_db.get_all_tickets():
		name = face_encodings_db.get_name_by_id(int(ticket[1]))
		matches_db.get_image_by_id(ticket[0])
		ticket_d = {"id": ticket[0], "name": name , "time_date": ticket[2].split('.')[0]}
		tickets.append(ticket_d)
	return tickets[::-1]



def byte_to_mb(byte):
	mb = "{:.2f}".format(byte / 1024 / 1024)
	return str(mb) + " MB"

app.jinja_env.globals.update(get_records=get_records)
app.jinja_env.globals.update(get_match_tickets=get_match_tickets)
app.jinja_env.globals.update(get_encodings=get_encodings)