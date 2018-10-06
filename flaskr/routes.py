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
				status='QUEUED',
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

		except(ZeroDivisionError):
			response = {
				'success': False
			}
			return jsonify(response)












