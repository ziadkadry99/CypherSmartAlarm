

from cyphersecuritycamera import socketio
from cyphersecuritycamera import app






if __name__ == '__main__':
	socketio.run(app, log_output=False, host='0.0.0.0', port=5000, debug=False, use_reloader=False)
