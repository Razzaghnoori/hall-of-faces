import MySQLdb
import os
from uuid import uuid4

def fill_database(path):
	conn = MySQLdb.connect(host="localhost" ,user="root" ,passwd="1234" ,db="faceland")
	cur = conn.cursor()
	dirs_names = os.listdir(path)
	
	for file_name in dirs_names:
		personID = str(uuid4())
		name = str(file_name)
		sql_insert_query = 'INSERT INTO people (id, name, category) VALUES (%s, %s, "actor")'
		cur.execute(sql_insert_query , (personID,name,))
		conn.commit()
		dirs_images = os.listdir(path + "/" + name)
		for file_image in dirs_images:
			name_image = str(file_image)
			image_path = path+ "/"+name+"/"+ name_image
			if(image_path[len(image_path)-1] == 'g'):
				sql_insert_query_ = 'INSERT INTO images (id, pathphoto) VALUES (%s, %s)'
				cur.execute(sql_insert_query_ , (personID,image_path,))
				conn.commit()

fill_database("../images/thumbnails_features_deduped_sample")
