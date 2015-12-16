import session
import json

SESSIONS_COUNTER = 0

def get_first_question(db):
	select_query = 'SELECT text FROM questions WHERE question_id=1'
	result = db.select(select_query)
	return result[0][0]

def add_session(sessions):
	global SESSIONS_COUNTER
	new_session = session.Session()
	new_session.questions_asked[1] = 0
	sessions[str(SESSIONS_COUNTER)] = new_session
	SESSIONS_COUNTER+=1
	return str(SESSIONS_COUNTER-1)

def main(db, sessions):
	'''
	@param session: the current sessions
	'''

	current_session = add_session(sessions)
	return json.dumps({'key':current_session, 'question_id': 1, 'question':get_first_question(db)})
