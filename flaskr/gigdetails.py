import db
import datetime


def add_worker_comment(gig_id, worker_id, comment_text):
	cursor = db.get_db().cursor()
	cursor.execute("SELECT details FROM gig WHERE gid=?", (gig_id,))
	cur_details = cursor.fetchone()['details']

	cursor.execute("SELECT name from worker WHERE id=?", (worker_id,))
	worker_name = cursor.fetchone()['name']

	now = datetime.datetime.now()
	cur_details += """
	<div class="commentcontainer darker">
	  <b>{}:</b>	
	  <p>{}</p>
	  <span class="time-left">{}</span>
	</div>
	""".format(worker_name, comment_text, str(now))

	cursor.execute("UPDATE gig SET details=? WHERE gid=?", (cur_details, gig_id))
	db.get_db().commit()

def add_client_comment(gig_id, client_id, comment_text):
	cursor = db.get_db().cursor()
	cursor.execute("SELECT details FROM gig WHERE gid=?", (gig_id,))
	cur_details = cursor.fetchone()['details']
	
	cursor.execute("SELECT name from client WHERE id=?", (client_id,))
	client_name = cursor.fetchone()['name']

	now = datetime.datetime.now()
	cur_details += """
	<div class="commentcontainer">
	  <b>{}:</b>
	  <p>{}</p>
	  <span class="time-left">{}</span>
	</div>
	""".format(client_name, comment_text, str(now))

	cursor.execute("UPDATE gig SET details=? WHERE gid=?", (cur_details, gig_id))
	db.get_db().commit()


def add_worker_picture(gig_id, worker_id, img_url):
	cursor = db.get_db().cursor()
	cursor.execute("SELECT details FROM gig WHERE gid=?", (gig_id,))
	cur_details = cursor.fetchone()['details']

	cursor.execute("SELECT name from worker WHERE id=?", (worker_id,))
	worker_name = cursor.fetchone()['name']

	now = datetime.datetime.now()
	cur_details += """
	<div class="commentcontainer darker">
	  <b>{} uploaded a photo:</b><br>	
	  <img src=\"{}\"><br>
	  <span class="time-left">{}</span>
	</div>
	""".format(worker_name, img_url, str(now))

	cursor.execute("UPDATE gig SET details=? WHERE gid=?", (cur_details, gig_id))
	db.get_db().commit()





