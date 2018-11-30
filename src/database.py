import MySQLdb
import api
import constants
from os import listdir, getenv
from os.path import join, isfile, exists
from uuid import uuid4

def fill_database(path, category='Celebrity'):
    conn = MySQLdb.connect(host=getenv('FACES_DB_HOST', 'localhost'),
                           database=getenv('FACES_DB_NAME', 'hall_of_faces'),
                           user=getenv('FACES_DB_USER', 'valar_morghulis'),
                           passwd=getenv('FACES_DB_PASS', 'valar_dohaeris'))

    cur = conn.cursor()

    for name in listdir(path):
        if isfile(name):
            continue
        id_ = str(uuid4())
        query = 'INSERT INTO people (id, name, category) VALUES (%s, %s, %s)'
        cur.execute(query , (id_, name, category))
        for file_ in listdir(join(path, name)):
            image_path = join(path, name, file_)
            extension = file_.split('.')[-1]
            if exists(image_path) and isfile(image_path) and extension in constants.allowed_image_types:
                encoding = api.get_encoding(image_path)
                query = 'INSERT INTO images (id, path, encoding) VALUES (%s, %s, %s)'
                cur.execute(query , (id_, image_path, encoding))
        conn.commit()

fill_database("../images/thumbnails_features_deduped_sample")
