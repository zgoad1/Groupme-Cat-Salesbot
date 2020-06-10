import os
from urllib.request import Request, urlopen
from urllib.parse import urlencode


#
# Send a message
#
def send_message(msg, atts = []):
	url = 'https://api.groupme.com/v3/bots/post'

	data = {
		'bot_id'		: os.getenv('GROUPME_BOT_ID'),
		'text'			: msg,
		'attachments'	: atts
	}

	print("\nSending message: \n{}".format(data).replace(', ', ',\n'))

	request = Request(url, urlencode(data).encode())
	json = urlopen(request).read().decode()
