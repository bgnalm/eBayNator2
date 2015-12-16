import json
import math

UNKNOWN_KEY_MESSAGE = 'your key is unknown'
WRONG_DATA_MESSAGE = ' the sent message is wrong'
NO_ITEM_FOUND_MESSAGE = 'no item is fitting the description'
MULTIPLE_ITEMS_FOUND_MESSAGE = 'multiple items fit the description'
ERROR_JSON_STRUCTURE = 'the json structure is wrong'
SESSION_ALREADY_OVER = 'your session is over'

ANSWERS = {
	'yes' : 1,
	'probably' : 0.75,
	'dont know' : 0.5,
	'probably not' : 0.25,
	'no' : 0
}

LIMITS = {
	'yes_min' : 0.59,
	'prob_min' : 0.26,
	'prob_not_max' : 0.74,
	'no_max' : 0.41
}

def get_question_text(db, question_number):
	query = 'SELECT text FROM questions WHERE question_id={0}'.format(question_number)
	return db.select(query)[0][0]

def get_item_name(db, item_id):
	query = 'SELECT name FROM items WHERE id={0}'.format(item_id)
	return db.select(query)[0][0]

def get_next_question_id(results, used_questions):
	number_of_questions = len(results[0]) - 1
	sums = [0] * number_of_questions
	sq_sums = [0] * number_of_questions

	for row in results:
		for value in range(1, number_of_questions+1):
			sums[value-1] += row[value]
			sq_sums[value-1] += row[value]**2

	variance = []
	max_variance = 0
	max_variance_index = 0
	for question in range(number_of_questions):
		mean = sums[question]/number_of_questions
		current_variance = (sq_sums[question]/ number_of_questions) - (mean ** 2)
		variance.append(current_variance)
		if (max_variance < current_variance) and (question+1 not in used_questions):
			max_variance = current_variance
			max_variance_index = question+1

	return max_variance_index

def get_real_question_id(db, question_id):
	return int(db._cursor.description[question_id][0][1:])

def find_closest_item(session, results):
	minimum_distance = 100000
	minimum_distance_id = 0

	for row in results:
		current_distance = 0
		for answer in session.questions_asked:
			current_distance += math.fabs(session.questions_asked[answer] - row[answer])

		if current_distance < minimum_distance:
			minimum_distance = current_distance
			minimum_distance_id = row[0]

	return minimum_distance_id

def generate_next_question(db, session, data, results):
	if len(session.questions_asked)+1 == len(results[0]):
		session.is_over = True
		best_guess = find_closest_item(session, results)
		return json.dumps({'key' : data['key'], 'result': get_item_name(db, best_guess)})

	next_question_id = get_next_question_id(results, session.questions_asked.keys())
	if next_question_id == 0:
		session.is_over = True
		return json.dumps({'key' : data['key'], 'result': get_item_name(db, results[0][0])})

	update_asked_questions(session, data, next_question_id)
	real_next_question = get_real_question_id(db, next_question_id)
	next_question_text = get_question_text(db, real_next_question)
	return json.dumps({'key':data['key'], 'question_id':real_next_question, 'question':next_question_text})

def generate_result(db, session, data):
	results = db.select(session.current_select_string)
	if db.get_rows() == 0:
		session.is_over = True
		return json.dumps({'key': data['key'], 'error': NO_ITEM_FOUND_MESSAGE})

	if db.get_rows() == 1:
		session.is_over = True
		return json.dumps({'key' : data['key'], 'result': get_item_name(db, results[0][0])})

	else:
		return generate_next_question(db, session, data, results)

def check_key(sessions, data):
	if 'key' not in data:
		return False

	if data['key'] not in sessions:
		return False

	return True

def check_question_params(data):
	if 'answer' not in data:
		return False

	if data['answer'] not in ANSWERS:
		return False

	if 'question_id' not in data:
		return False

	return True

def update_asked_questions(session, data, question_id):
	answer = data['answer']
	session.questions_asked[question_id] = ANSWERS[answer]

def update_select_query(session, data):
	string_added = ''
	if data['answer'] == 'yes':
		string_added = ' AND q{0}>{1}'.format(data['question_id'], LIMITS['yes_min'])

	elif data['answer'] == 'no':
		string_added = ' AND q{0}<{1}'.format(data['question_id'], LIMITS['no_max'])

	elif data['answer'] == 'probably':
		string_added = ' AND q{0}>{1}'.format(data['question_id'], LIMITS['prob_min'])

	elif data['answer'] == 'probably not':
		string_added = ' AND q{0}<{1}'.format(data['question_id'], LIMITS['prob_not_max'])

	session.current_select_string += string_added

def main(db, sessions, param):
	data = None
	try:
		data = json.loads(param)

	except:
		return ERROR_JSON_STRUCTURE
	if not check_key(sessions, data):
		return UNKNOWN_KEY_MESSAGE

	if not check_question_params(data):
		return WRONG_DATA_MESSAGE

	current_session = sessions[data['key']]
	if current_session.is_over:
		return SESSION_ALREADY_OVER

	update_asked_questions(current_session, data, data['question_id'])
	update_select_query(current_session, data)
	return generate_result(db, current_session, data)








		