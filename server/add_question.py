
def get_question_id(db, question):
	query = 'SELECT question_id FROM questions WHERE text="{0}"'.format(question)
	result = db.select(query)
	return result[0][0]

def add_to_questions_table(db, question_name):
	question = question_name.strip()
	query = 'INSERT INTO questions (`text`) VALUES ("{0}")'.format(question)
	db.query(query)
	return get_question_id(db, question)

def alter_answers_table(db, question_id):
	query = "ALTER TABLE `answers` ADD `q{0}` FLOAT NOT NULL DEFAULT '0.5'".format(question_id)
	db.query(query)

def main(db, sessions, param):
	question_id = add_to_questions_table(db, param)
	alter_answers_table(db, question_id)
	return "Answer Added"