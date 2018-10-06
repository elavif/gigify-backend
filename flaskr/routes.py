from flask import request, jsonify, make_response
import uuid
import datetime
from . import db, payment, s3exp, gigdetails
import os

def register_routes(app):
	# Place all the endpoints here!

	@app.route('/heyyy')
	def greeting():
		return "What's cooking good lookin'? ;)";


	@app.route('/create_gig', methods=('POST',))
	def create_gig():
		try:
			now = datetime.datetime.now()
			token = request.form['client_secret_token']
			client_id = int(request.form['client_id'])
			title = request.form['title']
			description = request.form['description']
			location = request.form['location']
			price = float(request.form['price'])
			ts_timeout = request.form['timeout_timestamp']

			gig_id = str(uuid.uuid4())


			db.insert_into('gig',
				gid=gig_id,
				cid=client_id,
				title=title,
				description=description,
				location=location,
				price=price,
				timeout_ts=now,
				status='Queued',
				)

			response = {
				'success': True,
				'gig_id' : gig_id,
			}

			return jsonify(response)

		except:
			response = {
				'success': False,
			}
			return jsonify(response)

	@app.route('/poll_gig', methods=('POST',))
	def poll_gig():
		try:
			gig_id = str(request.form['gig_id'])
			token = request.form['client_secret_token']
			cursor = db.get_db().cursor()
			cursor.execute("SELECT * FROM gig WHERE gid=?", (gig_id,))
			result_dict = cursor.fetchone()
			print (result_dict)
			response = {
				'success': True,
				'gig': result_dict,
			}


			return jsonify(response)

		except:
			response = {
				'success': False
			}
			return jsonify(response)

	@app.route('/accept_gig', methods=('POST',))
	def accept_gig():
		try:
			now = datetime.datetime.now()
			gig_id = str(request.form['gig_id'])
			worker_id = str(request.form['worker_id'])
			cursor = db.get_db().cursor()
			cursor.execute("UPDATE gig SET wid=?, accepted_ts=?, status='In Progress' WHERE gid=?", (worker_id, now, gig_id))
			db.get_db().commit()

			response = {
				'success': True
			}
			return jsonify(response)

		except:
			response = {
				'success': False
			}
			return jsonify(response)

	@app.route('/complete_gig', methods=('POST',))
	def complete_gig():
		try:
			now = datetime.datetime.now()
			gig_id = str(request.form['gig_id'])
			cursor = db.get_db().cursor()
			cursor.execute("UPDATE gig SET completed_ts=?, status='Complete' WHERE gid=?", (now, gig_id))
			db.get_db().commit()

			payment.pay_completed_gig(gig_id)

			response = {
				'success': True
			}
			return jsonify(response)

		except ZeroDivisionError:
			response = {
				'success': False
			}
			return jsonify(response)

	@app.route('/all_gigs', methods=('GET',))
	def get_all_gigs():
		try:
			cursor = db.get_db().cursor()
			cursor.execute("SELECT * FROM gig")
			results = cursor.fetchall()
			response = {
				'success': True,
				'gigs': results,
			}

			return jsonify(response)

		except:
			response = {
				'success': False
			}
			return jsonify(response)


	@app.route('/all_clients', methods=('GET',))
	def get_all_clients():
		try:
			cursor = db.get_db().cursor()
			cursor.execute("SELECT * FROM client")
			results = cursor.fetchall()
			response = {
				'success': True,
				'clients': results,
			}

			return jsonify(response)

		except:
			response = {
				'success': False
			}
			return jsonify(response)

	@app.route('/all_workers', methods=('GET',))
	def get_all_workers():
		try:
			cursor = db.get_db().cursor()
			cursor.execute("SELECT * FROM worker")
			results = cursor.fetchall()
			response = {
				'success': True,
				'workers': results,
			}

			return jsonify(response)

		except:
			response = {
				'success': False
			}
			return jsonify(response)

	@app.route('/get_all_client_jobs', methods=('POST',))
	def get_all_client_jobs():
		try:
			client_id = str(request.form['client_id'])
			try:
				status = str(request.form['status'])
				cursor = db.get_db().cursor()
				cursor.execute("SELECT * FROM gig WHERE cid=? and status=?", (client_id, status))
			except KeyError:
    			# no status do something else
				cursor = db.get_db().cursor()
    			cursor.execute("SELECT * FROM gig WHERE cid=?", (client_id,))
			results = cursor.fetchall()
			response = {
				'success': True,
				'gigs': results,
			}

			return jsonify(response)

		except:
			response = {
				'success': False
			}
			return jsonify(response)



	@app.route('/get_all_worker_jobs', methods=('GET',))
	def get_all_worker_jobs():
		try:
			client_id = str(request.form['worker_id'])
			try:
				status = str(request.form['status'])
				cursor = db.get_db().cursor()
				cursor.execute("SELECT * FROM gig WHERE wid=? and status=?", (worker_id, status))
			except KeyError:
    			# no status do something else
				cursor = db.get_db().cursor()
    			cursor.execute("SELECT * FROM gig WHERE wid=?", (worker_id,))
			results = cursor.fetchall()
			response = {
				'success': True,
				'gigs': results,
			}

			return jsonify(response)

		except:
			response = {
				'success': False
			}
			return jsonify(response)

	@app.route('/worker_balance', methods=('POST',))
	def get_worker_balance():
		try:			
			worker_id = str(request.form['worker_id'])
			cursor = db.get_db().cursor()
			cursor.execute("SELECT balance, todaybal  FROM worker WHERE id=?", (worker_id))
			result = cursor.fetchone()
			response = {
				'success': True,
				'result': result
			}
			return jsonify(response)
		except ZeroDivisionError:
			response = {
				'success': False
			}
			return jsonify(response)


	@app.route('/client_balance', methods=('POST',))
	def get_client_balance():
		try:			
			client_id = str(request.form['client_id'])
			cursor = db.get_db().cursor()
			cursor.execute("SELECT balance FROM client WHERE id=?", (client_id))
			result = cursor.fetchone()
			response = {
				'success': True,
				'result': result
			}
			return jsonify(response)
		except ZeroDivisionError:
			response = {
				'success': False
			}
			return jsonify(response)

	@app.route('/add_worker_comment', methods=('POST',))
	def add_worker_comment():
		worker_id = str(request.form['worker_id'])
		gig_id = str(request.form['gig_id'])
		comment_text = str(request.form['comment_text'])

		gigdetails.add_worker_comment(gig_id, worker_id, comment_text)

		response = {
			'success': True
		}
		return jsonify(response)

	@app.route('/add_worker_picture_comment', methods=('POST',))
	def add_worker_picture_comment():
		worker_id = str(request.form['worker_id'])
		gig_id = str(request.form['gig_id'])
		file=request.files['image']
		image_id = str(uuid.uuid4()) + '.'+ file.filename.split(".")[-1]
		f = os.path.join(app.root_path, 'images', image_id)
		file.save(f)

		image_url = 'http://localhost:5000/images/' +image_id

		gigdetails.add_worker_picture(gig_id, worker_id, image_url)

		response = {
				'success': True,
				'image_url': image_url
			}
		return jsonify(response)



	@app.route('/add_client_comment', methods=('POST',))
	def add_client_comment():
		client_id = str(request.form['client_id'])
		gig_id = str(request.form['gig_id'])
		comment_text = str(request.form['comment_text'])

		gigdetails.add_client_comment(gig_id, client_id, comment_text)

		response = {
			'success': True
		}
		return jsonify(response)



	@app.route('/images/<path:path>')
	def images(path):
		fullpath = os.path.join(app.root_path, 'images', path)
		resp = make_response(open(fullpath).read())
		resp.content_type = "image/jpeg"
		return resp		


	@app.route('/s3exp')
	def route_to_s3module():
		return s3exp.get_page()

	@app.route('/commentexp')
	def route_to_commentexppage():
		return s3exp.comment_page()


	'''
	# Merged with add_worker_picture, don't use.
	@app.route('/image_upload', methods=('POST',))
	def image_upload():
		file=request.files['image']
		image_id = str(uuid.uuid4())
		f = os.path.join(app.root_path, 'images', image_id)
		file.save(f)
		response = {
				'success': True,
				'image_id': image_id
			}
		return jsonify(response)
	'''

	'''@app.route('/add_worker_picture', methods=('POST',))
	def add_worker_picture():
		worker_id = str(request.form['worker_id'])
		gig_id = str(request.form['gig_id'])
		img_url = str(request.form['img_url'])

		gigdetails.add_worker_picture(gig_id, worker_id, img_url)

		response = {
			'success': True
		}
		return jsonify(response)'''
