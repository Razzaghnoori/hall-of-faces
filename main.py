import face_recognition
import MySQLdb
from os import getenv

class MatchFinder():
    def __init__(self, categories=None):
        database_name = 'halloffaces'
        self.conn = MySQLdb.connect(host=getenv('FACES_DB_HOST', 'bravos'),
                                    database=getenv('FACES_DB_NAME', database_name),
                                    user=getenv('FACES_DB_USER', 'valar_morghulis'),
                                    passwd=getenv('FACES_DB_PASS', 'valar_dohaeris'))
        self.cur = self.conn.cursor()

        command = "SELECT * FROM {}".format(database_name)
        where_statement = ''
        if categories is not None:
            placeholders = "({})".format(', '.join(['%s'] * len(categories)))
            where_statement = " WHERE categories IN {}".format(placeholders)
        command += where_statement
        self.cur.execute(command, categories)

    def find(self, img_path):
        target_img = face_recognition.load_image_file(img_path)
        target_encoding = face_recognition.face_encodings(target_img)[0]
        min_dist = float('inf')

        for row in self.cur:
            encoding = row[3]
            distance = face_recognition.face_distance(target_encoding, encoding)
            if distance < min_dist:
                most_similar_row = row
                min_dist = distance
        return most_similar_row
