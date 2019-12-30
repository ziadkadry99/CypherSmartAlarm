import datetime
from Visuals_Processing import image_utils
from Databases.Database_Coms import DatabaseComs
import datetime

# time between tickets for the same match | Will be added to settings
Database_Coms = DatabaseComs()

class MatchesHistory:
    duplicate_interval_second = 60
    duplicate_interval_datetime = datetime.timedelta(seconds=duplicate_interval_second)
    last_ticket_time = datetime.datetime.now() - duplicate_interval_datetime
    last_ticket_id = -1
    logger = None

    def __init__(self, _logger):
        self.logger = _logger


    def store_ticket(self, id, time, image_obj, cur_time=False):
        if datetime.datetime.now() - self.last_ticket_time < self.duplicate_interval_datetime and self.last_ticket_id == id:
            return
        if cur_time:
            time = datetime.datetime.now()
        self.last_ticket_time = datetime.datetime.now()
        last_ticket_id = id
        Database_Coms.exceute_query(''' INSERT INTO detection_history(id,time_date,image)
                      VALUES(?,?,?) ''', (str(id), time, image_obj))
        self.logger.info('Ticket stored in match history')
        rows = Database_Coms.exceute_query(''' SELECT * FROM detection_history WHERE id=? ''',
                                           (id,), retRows=True)
        for entry in rows:

            print(entry)

    def delete_ticket(self, ticket_num):
        Database_Coms.exceute_query('DELETE FROM detection_history WHERE ticket=?', (ticket_num,))


    def find_tickets_with_id(self, id):
        return Database_Coms.exceute_query('SELECT * FROM detection_history WHERE id=?', (id,), retRows=True)


    def find_tickets_with_ticket_num(self, ticket_num):
        return Database_Coms.exceute_query('SELECT * FROM detection_history WHERE ticket=?', (ticket_num,), retRows=True)




