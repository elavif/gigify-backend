import db

def pay_completed_gig(gig_id):
	print (gig_id)
	cursor = db.get_db().cursor()
	cursor.execute("SELECT client.balance as cbal, worker.balance as wbal, worker.todaybal, price, cid, wid FROM gig INNER JOIN client ON gig.cid=client.id INNER JOIN worker on gig.wid=worker.id WHERE gid=?", (gig_id,))
	entry_res = cursor.fetchone()

	print(entry_res)

	price = entry_res['price']
	cid = entry_res['cid']
	wid = entry_res['wid']
	client_bal = entry_res['cbal'] + price
	worker_bal = entry_res['wbal'] + price
	worker_todaybal = entry_res['todaybal'] + price

	cursor.execute("UPDATE client SET balance=? WHERE id=?", (client_bal, cid))
	cursor.execute("UPDATE worker SET balance=?, todaybal=? WHERE id=?", (worker_bal, worker_todaybal, wid))

	db.get_db().commit()