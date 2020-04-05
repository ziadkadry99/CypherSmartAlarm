from cyphersecuritycamera.Databases.Database_Coms import DatabaseComs
from cyphersecuritycamera.Databases.settings import settings
import datetime
import cv2
from cyphersecuritycamera.Logging.Logger import Logger
Database_Coms = DatabaseComs()

class MatchesHistory:


    logger = Logger()

    def __init__(self):
        self.Settings = settings()
        self.duplicate_interval_second = int(self.Settings.find_setting_by_name('detection_interval_second')) / 60
        self.duplicate_interval_datetime = datetime.timedelta(seconds=self.duplicate_interval_second)
        self.last_ticket_time = datetime.datetime.now() - self.duplicate_interval_datetime
        self.last_ticket_id = -1


    def store_ticket(self, id, time, image_obj, cur_time=False):
        if datetime.datetime.now() - self.last_ticket_time < self.duplicate_interval_datetime and self.last_ticket_id == id:
            return
        if cur_time:
            time = datetime.datetime.now()
        self.last_ticket_time = datetime.datetime.now()
        last_ticket_id = id

        Database_Coms.exceute_query(''' INSERT INTO detection_history(id,time_date)
                      VALUES(?,?) ''', (str(id), time,))
        self.logger.info('Ticket stored in match history')
        rows = Database_Coms.exceute_query(''' SELECT * FROM detection_history WHERE ticket = (SELECT MAX(ticket) FROM detection_history)''',
                                            retRows=True)
        new_ticket_id = rows[0][0]
        cv2.imwrite('cyphersecuritycamera/Databases/TicketImages/'+ str(new_ticket_id) + '.png', image_obj)



    def delete_ticket(self, ticket_num):
        Database_Coms.exceute_query('DELETE FROM detection_history WHERE ticket=?', (ticket_num,))


    def find_tickets_with_id(self, id):
        return Database_Coms.exceute_query('SELECT * FROM detection_history WHERE id=?', (id,), retRows=True)


    def find_tickets_with_ticket_num(self, ticket_num):
        return Database_Coms.exceute_query('SELECT * FROM detection_history WHERE ticket=?', (ticket_num,), retRows=True)

    def get_image_by_id(self, id):
        return cv2.imread('Databases/TicketImages/'+ str(id) + '.png')

    def get_all_tickets(self):
        return Database_Coms.exceute_query('SELECT * FROM detection_history',  retRows=True)


