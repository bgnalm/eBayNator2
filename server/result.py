import json

WRONG_DATA_MESSAGE = 'the data is wrong'
ERROR_JSON_STRUCTURE = 'json structure is wrong'
UNKNOWN_KEY_MESSAGE = 'your key is unknown'

ALPHA = 0.1

def add_item_to_item_table(db, item_name):
	query = 'INSERT INTO items (`name`) VALUES ("{0}")'.format(item_name)
	db.query(query)
	return db.last_insert_id()

def add_item_to_answers_table(db, session, item_id):
	prefix = 'INSERT INTO answers (item_id'
	postfix = ' VALUES ({0}'.format(item_id)

	for question in session.questions_asked:
		prefix += ',q{0}'.format(question)
		postfix += ',{0}'.format(session.questions_asked[question])

	prefix += ')'
	postfix += ')'

	query = prefix + postfix
	db.query(query)

def add_new_item(db, session, item_name):
	add_item_to_item_table(db, item_name)
	item_id = get_item_id_by_name(db, item_name)
	add_item_to_answers_table(db, session, item_id)

def get_item_by_name(db, item_name):
	query = 'SELECT id, times_played FROM items WHERE name="{0}"'.format(item_name)
	result = db.select(query)
	if db.get_rows() == 0:
		return -1,0

	return result[0][0], result[0][1]

def get_item_id_by_name(db, item_name):
	query = 'SELECT id FROM items WHERE name="{0}"'.format(item_name)
	result = db.select(query)
	if db.get_rows() == 0:
		return -1

	return result[0][0]

def get_item_by_item_id(db, item_id):
	query = 'SELECT * from answers WHERE item_id={0}'.format(item_id)
	return db.select(query)[0]

def update_average(db, session, item_id):
	row_updated = get_item_by_item_id(db, item_id)
	query = 'UPDATE answers SET '
	for question in session.questions_asked:
		new_average = ((1-ALPHA) * row_updated[question]) + ALPHA * session.questions_asked[question]
		query += 'q{0}={1},'.format(question, new_average)

	query = query[:-1] + ' WHERE item_id={0}'.format(item_id)
	db.query(query)

def update_times_played(db, item_id, times_played):
	query = 'UPDATE items SET times_played={0} WHERE id={1}'.format(times_played, item_id)
	db.query(query)

def check_key(sessions, data):
	if 'key' not in data:
		return False

	if data['key'] not in sessions:
		return False

	return True

def check_result_params(data):
	if 'result' not in data:
		return False

	return True

def main(db, sessions, param):
	data = None
	try:
		data = json.loads(param)

	except Exception ,e:
		print str(e)
		return ERROR_JSON_STRUCTURE

	if not check_key(sessions, data):
		return UNKNOWN_KEY_MESSAGE

	if not check_result_params(data):
		return WRONG_DATA_MESSAGE

	current_session = sessions[data['key']]
	item_id, times_played = get_item_by_name(db, data['result'])
	if -1 != item_id:
		update_average(db, current_session, item_id)
		update_times_played(db, item_id, times_played+1)

	else:
		add_new_item(db, current_session, data['result'])

	return json.dumps({'key':data['key'], 'status':'over'})

