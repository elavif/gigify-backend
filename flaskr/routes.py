from flask import request, jsonify
import uuid
import datetime

def register_routes(app):
	# Place all the endpoints here!

	@app.route('/heyyy')
	def greeting():
		return "What's cooking good lookin'? ;)";


	@app.route('/create_gig', methods=('POST',))
	def create_gig():
		now = datetime.datetime.now()
		token = request.form['client_secret_token']
		title = request.form['title']
		description = request.form['description']
		location = request.form['location']
		price = float(request.form['price'])
		ts_timeout = request.form['timeout_timestamp']
		ts_submit = request.form['']

		gig_id = uuid.uuid4()

		# Submit shit to DB


		response = {
			'gig_id' : gig_id,
		}

		return jsonify(response)

	@app.route('/poll_gig', methods=('POST',))
	def poll_gig():
		pass