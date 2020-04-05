from cyphersecuritycamera.Databases.Database_Coms import DatabaseComs
from cyphersecuritycamera.Logging.Logger import Logger
Database_Coms = DatabaseComs()

class settings:

    logger = Logger()

    def __init__(self):
        self.init_settings_table()

    def create_setting(self, name, value):
        res = self.find_setting_by_name(name)
        if not res or len(res) == 0:
            Database_Coms.exceute_query(''' INSERT INTO settings(name, value)
                          VALUES(?,?) ''', (name, value))
            self.logger.info('setting ' + name + ' with ID ' + str(id) + ' has been created')
        else:
            self.logger.error('Setting ' + name + ' already exists')

    def change_setting(self, value, id = -1, name = None):
        if id and id != -1:

            Database_Coms.exceute_query(''' UPDATE settings
                            SET value = ?
                            WHERE id = ? ''', (str(value), str(id)))


            self.logger.info('Updated setting with id: ' + str(id) + ' to value: ' + value)

        elif name:

            Database_Coms.exceute_query(''' UPDATE settings
                                        SET value = ?
                                        WHERE name = ?; ''', (value, name,))
            print(''' UPDATE settings
                                        SET value = ?
                                        WHERE name = ?; ''', (value, name,))
            self.logger.info('Updated setting with name: ' + name + ' to value: ' + value)
        else:
            self.logger.error('''Couldn't change setting, id|name not provided''')

    def delete_setting(self, id):
        Database_Coms.exceute_query('DELETE FROM settings WHERE ticket=?', (id,))

    def find_setting_by_id(self, id):
        return Database_Coms.exceute_query('SELECT * FROM settings WHERE id=?', (id,), retRows=True)

    def find_setting_by_name(self, name, retVal=True):
        rows = Database_Coms.exceute_query('SELECT * FROM settings WHERE name=?', (name,), retRows=True)
        if rows:

            if retVal:

                return rows[0][2]
            else:

                return rows[0]
        else:
            return None

    def init_settings_table(self):
        # Default values in settings
        # duplicate_interval_second: wait period between storing match tickets of the same face. id = 1
        # motion_detection_upperbound id = 2
        # motion_detection_lowerbound id = 3
        # auto_store_new_face id = 4
        # camera_src = 0 id = 5
        # draw_box_on_feed = 1 if = 6

        self.create_setting('duplicate_interval_second', '60')
        self.create_setting('detection_interval_second', '120')
        self.create_setting('motion_detection_upperbound', '0')
        self.create_setting('motion_detection_lowerbound', '0')
        self.create_setting('camera_src', '0')
        self.create_setting('draw_box_on_feed', '1')
        self.logger.info('Default settings initialized')





