import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext
import datetime
import uuid

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = dict_factory

    return g.db

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def insert_into(table, **kwargs):
	sql = 'INSERT INTO {} ({}) VALUES ({})'.format(
		table,
		','.join(kwargs.keys()),
		','.join('?' for v in kwargs.values())
		)
	print(sql)
	print (kwargs.values())
	get_db().cursor().execute(sql, kwargs.values())
	get_db().commit()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

	now = datetime.datetime.now()
	client_id = 3
	title = "Get the scooter on 7th avenue and move to 9th avenue"
	description = "$5 to move it please"
	location = "37.7899 122.3969"
	price = 5.00


	insert_into('gig',
		gid= str(uuid.uuid4()),
		cid=client_id,
		title=title,
		description=description,
		location=location,
		price=price,
		timeout_ts=now,
		status='Queued',
		)

	insert_into('gig',
		gid= str(uuid.uuid4()),
		cid=0,
		title="Mow my lawn",
		description="please, I am going out of town and my lawn as become a huge disaster",
		location="38.7899 123.3969",
		price=30.00,
		timeout_ts=now,
		status='Queued',
		)


	insert_into('gig',
		gid= str(uuid.uuid4()),
		cid=0,
		title="Pizza Delivery",
		description="Get these hot pizzas to our customers!",
		location=location,
		price=price,
		timeout_ts=now,
		status='Queued',
		)

	insert_into('gig',
		gid= str(uuid.uuid4()),
		cid=0,
		title="Clean the kitchen",
		description="Need someone to clean my kitchen! Willing to pay extra. ",
		location=location,
		price=price,
		timeout_ts=now,
		status='Queued',
		)


	insert_into('gig',
		gid= str(uuid.uuid4()),
		cid=0,
		title="Need someone to shovel",
		description="Hurt my back recently and would love someones help",
		location=location,
		price=price,
		timeout_ts=now,
		status='Queued',
		)


	insert_into('gig',
		gid= str(uuid.uuid4()),
		cid=1,
		title="Come to the office and assemble 50 tables",
		description="Come alone or birng a friend",
		location=location,
		price=150.00,
		timeout_ts=now,
		status='Queued',
		)
@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)