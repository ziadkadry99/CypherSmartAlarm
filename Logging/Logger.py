import  logging
from datetime import datetime


class Logger:
    def __init__(self, log_file_name=None):
        if not log_file_name:
            log_file_name = 'LOG_' + str(datetime.now().strftime('%Y-%m-%d %H-%M-%S')) + '.log'
        print(log_file_name)
        logging.basicConfig(filename= 'Logs/' + log_file_name, filemode='w', format='%(name)s - %(levelname)s - %(message)s')
        logging.warning('This will get logged to a file')
