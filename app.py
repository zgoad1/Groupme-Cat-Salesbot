import os
import database
import message_lib
import time
from message_sending import send_message
from flask import Flask, request


app = Flask(__name__)


#
# Upon receiving a message in the group, formulate a reply
# and send it.
#
@app.route('/', methods=['POST'])
def webhook():
	global conn
	global cursor

	data = request.get_json()
	print("Received message:\n{}".format(data).replace(', ', ',\n'))

	# Don't reply to self or system
	if data['name'] != os.getenv('GROUPME_BOT_NAME') and data['name'].lower() != 'groupme':
		conn = database.open_connection()		# Connect to database
		database.update_day()					# Update date & do date-based event stuff
		message_lib.parse_message(data)			# Read message & update database
		msg, atts = message_lib.get_reply(data)	# Formulate a reply
		print("Message to send: {}\nAttachments: {}".format(msg, atts))
		if(msg != None and msg != ""):			# Check that our reply isn't empty
			time.sleep(0.5)						# Wait a second so we don't confuse Groupme
			send_message(msg, atts)				# Send our reply
		database.close_connection()				# Close database connection

	return "ok", 200	# HTTP response
