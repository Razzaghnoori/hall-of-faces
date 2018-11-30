import face_recognition
import MySQLdb
import numpy as np
from os import getenv

class MatchFinder():
    def __init__(self, categories=None):
        database_name = 'hall_of_faces'
        self.conn = MySQLdb.connect(host=getenv('FACES_DB_HOST', 'bravos'),
                                    database=getenv('FACES_DB_NAME', database_name),
                                    user=getenv('FACES_DB_USER', 'valar_morghulis'),
                                    passwd=getenv('FACES_DB_PASS', 'valar_dohaeris'))
        self.cur = self.conn.cursor()

        command = "SELECT * FROM people"
        where_statement = ''
        if categories is not None:
            placeholders = "({})".format(', '.join(['%s'] * len(categories)))
            where_statement = " WHERE category IN {}".format(placeholders)
        command += where_statement
        self.cur.execute(command, categories)
        self.related_people = self.cur.fetchall()

    def find(self, img_path):
        target_img = face_recognition.load_image_file(img_path)
        target_encoding = face_recognition.face_encodings(target_img)

        if len(target_encoding) == 0:
            return 'Unknown', None

        target_encoding = target_encoding[0]
        min_dist = float('inf')

        for row in self.related_people:
            query = "SELECT path, encoding from images where id = %s"
            self.cur.execute(query, (row[0],))

            for img in self.cur:
                if img[1] is None:
                    continue
                encoding = np.loads(img[1])
                distance = face_recognition.face_distance(target_encoding, [encoding])
                if distance < min_dist:
                    most_similar_img_path = img[0]
                    most_similar_name = row[2]
                    min_dist = distance

        return most_similar_name, most_similar_img_path


def get_encoding(image_path, dumped=True):
    img = face_recognition.load_image_file(image_path)
    encoding = face_recognition.face_encodings(img)

    if len(encoding) > 0:
        encoding = encoding[0]
    else:
        return None

    if dumped:
        encoding = np.ndarray.dumps(encoding)

    return encoding
