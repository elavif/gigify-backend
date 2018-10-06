from flask import request, jsonify
import uuid
import datetime
import db

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
			
			# TODO update balances

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











