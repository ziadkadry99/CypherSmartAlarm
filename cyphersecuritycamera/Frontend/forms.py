from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField
from wtforms import IntegerField
from wtforms import BooleanField
from wtforms.validators import DataRequired
from wtforms.validators import NumberRange
from cyphersecuritycamera.Databases.settings import settings as settingsManager
from cyphersecuritycamera.Logging.Logger import Logger

logger = Logger()
SettingsManager = settingsManager()

class CurSettings(object):
    duplicate_interval_second = int(SettingsManager.find_setting_by_name('duplicate_interval_second'))
    detection_interval_second = int(SettingsManager.find_setting_by_name('detection_interval_second'))
    drawbox = int(SettingsManager.find_setting_by_name('draw_box_on_feed'))
    def update_settings(self):
        self.duplicate_interval_second = int(SettingsManager.find_setting_by_name('duplicate_interval_second'))
        self.detection_interval_second = int(SettingsManager.find_setting_by_name('detection_interval_second'))
        self.drawbox = int(SettingsManager.find_setting_by_name('draw_box_on_feed'))


class SettingsForm(FlaskForm):
    duplicate_interval_second = IntegerField('Duplicate interval in Seconds', validators=[DataRequired('Please make sure you enter a number'), NumberRange(1, 5000)])
    detection_interval_second = IntegerField('Face Detection Interval ', validators=[DataRequired('Please make sure you enter a number'), NumberRange(1, 5000)])
    cameras = ['test1', 'test2']
    drawbox = BooleanField('Draw Box around faces in live stream')
    #camera_src = SelectField('Camera Source', choices=cameras, validators=[DataRequired()])
    save = SubmitField('Submit')


class ChangeEncodingNameForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired('Please enter a name')])

    save = SubmitField('Submit')

class CurEncodingName(object):
    name = ''
    id = ''
    def set_name_id(self, name, id):
        self.name = name
        self.id = id
