import  logging
from datetime import datetime


class Logger:
    def __init__(self, log_file_name=None):
        if not log_file_name:
            log_file_name = 'LOG_' + str(datetime.now().strftime('%Y-%m-%d %H-%M-%S')) + '.log'
        logging.getLogger('socketio').setLevel(logging.WARNING)
        logging.getLogger('werkzeug').setLevel(logging.WARNING)
        logging.getLogger('engineio').setLevel(logging.WARNING)
        logging.basicConfig(filename= 'cyphersecuritycamera/Logging/Logs/' + log_file_name, filemode='w', format='[%(asctime)s] %(levelname)s: %(message)s', level=logging.NOTSET)

    def time_now_str(self):
        return str(datetime.now().strftime('%Y-%m-%d %H-%M-%S'))

    def info(self, message):
        logging.info(message)

    def debug(self, message):
        logging.debug(message)

    def warning(self, message):
        logging.warning(message)

    def error(self, message):
        logging.error(message)

    def warning(self, message):
        logging.warning(message)

