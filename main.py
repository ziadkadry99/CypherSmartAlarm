# This file is currently for testing purposes

from Databases.face_encodings_database import FaceEncodingsDatabase as fed
from Camera import Match_Faces_From_Feed as webcamThingy
from Databases.Database_Coms import  DatabaseComs
from Logging.Logger import Logger


logger = Logger()
Database_Coms_obj = DatabaseComs()
fed_obj = fed()


Database_Coms_obj.init_db_tables()
fed_obj.store_new_encoding("Test_Images/ziad.jpg", "Ziad")

fed_obj.load_database()
fed_obj.debug_print_names()


# fed.debug_print_names()
match_face_from_feed = webcamThingy.MatchFaceFromFeed()

match_face_from_feed.get_face_matches()

#Database_Coms.init_db_tables()




