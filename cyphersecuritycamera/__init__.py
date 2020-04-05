from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

# This will be randomly generated on the first run
app.config['SECRET_KEY'] = '54baa255ddef02f329ea43d607786387'


app.config['THUMBNAIL_MEDIA_ROOT'] = '/Databases/TicketImages'
app.config['THUMBNAIL_MEDIA_URL'] = '/TicketImages/'

from cyphersecuritycamera import routes