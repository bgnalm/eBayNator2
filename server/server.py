import BaseHTTPServer
import session
import time
import db_conn
import select
import cgi

import start
import question
import result
import add_question

PORT = 8008

GET_PAGES = {
	'/start' :  start.main,
}

POST_PAGES = {
	'/next_question' : question.main,
	'/result' : result.main,
	'/add_question' : add_question.main
}

SESSIONS = {}

db = db_conn.DB_Conn()

class EbayNatorServer(BaseHTTPServer.BaseHTTPRequestHandler):

	def do_HEAD(s):
		s.send_response(200)
		s.send_header('Content-type', r'text/html')
		s.end_headers()

	def do_GET(s):
		if s.path not in GET_PAGES:
			s.send_response(404)
			s.end_headers()
			s.wfile.write('404 Not found')
			return

		s.send_response(200)
		s.end_headers()
		s.wfile.write(GET_PAGES[s.path](db, SESSIONS))

	def do_POST(s):
		if s.path not in POST_PAGES:
			s.send_response(404)
			s.end_headers()
			s.wfile.write('404 Not found')
			return

		s.send_response(200)
		s.end_headers()
		length = int(s.headers['Content-Length'])
  		post_data = s.rfile.read(length)
		s.wfile.write(POST_PAGES[s.path](db, SESSIONS, post_data))

def main():
	server = BaseHTTPServer.HTTPServer
	httpd = server(('0.0.0.0', PORT), EbayNatorServer)
	print 'started at {0} in port {1}'.format(time.asctime(), PORT)
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass

	db.close()
	httpd.server_close()
	print 'ended at {0}'.format(time.asctime())

main()

