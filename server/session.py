STARTING_SELECT_STRING = 'SELECT * FROM answers WHERE item_id>0'

class Session(object):

	def __init__(self):
		self.current_select_string = STARTING_SELECT_STRING
		self.questions_asked = {}
		self.is_over = False